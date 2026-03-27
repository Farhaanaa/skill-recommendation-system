from flask import Flask, render_template, request, redirect, url_for, flash,session
from config import Config
from models import db, User, UserProfile, Bookmark, Feedback
from recommender import get_recommendations
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from quiz import select_questions, score_quiz
import json
# ─────────────────────────────────────────────
#  APP INIT
# ─────────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to continue."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


# ─────────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ─────────────────────────────────────────────
#  SIGNUP
# ─────────────────────────────────────────────
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not email or not password:
            flash("All fields are required.", "error")
            return render_template("signup.html")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return render_template("signup.html")

        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "error")
            return render_template("signup.html")

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


# ─────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        user     = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        login_user(user)
        flash(f"Welcome back, {user.username}!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ─────────────────────────────────────────────
#  LOGOUT
# ─────────────────────────────────────────────
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))


# ─────────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────────
@app.route("/dashboard")
@login_required
def dashboard():
    profile   = UserProfile.query.filter_by(user_id=current_user.id)\
                                  .order_by(UserProfile.created_at.desc()).first()
    bookmarks = Bookmark.query.filter_by(user_id=current_user.id)\
                               .order_by(Bookmark.saved_at.desc()).all()

    return render_template(
        "dashboard.html",
        profile=profile,
        bookmarks=bookmarks,
        bookmark_count=len(bookmarks),
        profile_complete=profile is not None,
    )


# ─────────────────────────────────────────────
#  PROFILE FORM → RECOMMENDATIONS
# ─────────────────────────────────────────────
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        interests      = request.form.get("interests", "")
        qualification  = request.form.get("qualification", "")
        course         = request.form.get("course", "")
        career         = request.form.get("career", "")
        career_goal    = request.form.get("career_goal", "")
        skills         = request.form.get("skills", "")
        certifications = request.form.get("certifications", "")
        tools_known    = request.form.get("tools_known", "")
        what_they_know = request.form.get("what_they_know", "")

        # Save to DB
        new_profile = UserProfile(
            user_id=current_user.id,
            interests=interests,
            qualification=qualification,
            course=course,
            career=career,
            career_goal=career_goal,
            skills=skills,
            certifications=certifications,
            tools_known=tools_known,
            what_they_know=what_they_know,
        )
        db.session.add(new_profile)
        db.session.commit()

        # Run ML engine
        recommendations = get_recommendations(
            interests=interests,
            qualification=qualification,
            course=course,
            career=career,
            career_goal=career_goal,
            skills=skills,
            certifications=certifications,
            tools_known=tools_known,
            what_they_know=what_they_know,
            top_n=5,
        )

        return render_template(
            "results.html",
            recommendations=recommendations,
            profile={
                "interests": interests,
                "qualification": qualification,
                "course": course,
                "career": career,
                "career_goal": career_goal,
                "skills": skills,
                "certifications": certifications,
                "tools_known": tools_known,
                "what_they_know": what_they_know,
            }
        )

    existing = UserProfile.query.filter_by(user_id=current_user.id)\
                                 .order_by(UserProfile.created_at.desc()).first()
    return render_template("profile.html", existing=existing)


# ─────────────────────────────────────────────
#  BOOKMARK
# ─────────────────────────────────────────────
@app.route("/bookmark", methods=["POST"])
@login_required
def bookmark():
    project_title  = request.form.get("project_title", "")
    project_domain = request.form.get("project_domain", "")

    exists = Bookmark.query.filter_by(
        user_id=current_user.id,
        project_title=project_title
    ).first()

    if not exists:
        db.session.add(Bookmark(
            user_id=current_user.id,
            project_title=project_title,
            project_domain=project_domain,
        ))
        db.session.commit()
        flash(f"'{project_title}' saved to bookmarks!", "success")
    else:
        flash("Already bookmarked.", "info")

    return redirect(url_for("dashboard"))


# ─────────────────────────────────────────────
#  REMOVE BOOKMARK
# ─────────────────────────────────────────────
@app.route("/bookmark/remove/<int:bookmark_id>", methods=["POST"])
@login_required
def remove_bookmark(bookmark_id):
    bm = Bookmark.query.get_or_404(bookmark_id)
    if bm.user_id != current_user.id:
        flash("Not authorised.", "error")
        return redirect(url_for("dashboard"))
    db.session.delete(bm)
    db.session.commit()
    flash("Bookmark removed.", "success")
    return redirect(url_for("dashboard"))


# ─────────────────────────────────────────────
#  FEEDBACK
# ─────────────────────────────────────────────
@app.route("/feedback", methods=["POST"])
@login_required
def feedback():
    db.session.add(Feedback(
        user_id=current_user.id,
        project_title=request.form.get("project_title", ""),
        liked=request.form.get("liked") == "true",
    ))
    db.session.commit()
    flash("Thanks for your feedback!", "success")
    return redirect(url_for("dashboard"))

# ─────────────────────────────────────────────
#  QUIZ — START
# ─────────────────────────────────────────────
@app.route("/quiz")
@login_required
def quiz_start():
    # Pull latest profile to personalise questions
    profile = UserProfile.query.filter_by(user_id=current_user.id)\
                                .order_by(UserProfile.created_at.desc()).first()

    interests = profile.interests if profile else ""
    skills    = profile.skills    if profile else ""

    questions = select_questions(interests, skills, n=10)

    # Store question ids in session so we can grade later
    session["quiz_ids"] = [q["id"] for q in questions]

    return render_template("quiz.html", questions=questions)


# ─────────────────────────────────────────────
#  QUIZ — SUBMIT
# ─────────────────────────────────────────────
@app.route("/quiz/submit", methods=["POST"])
@login_required
def quiz_submit():
    from quiz_data import QUESTIONS

    quiz_ids  = session.get("quiz_ids", [])
    questions = [q for q in QUESTIONS if q["id"] in quiz_ids]

    # Collect answers from form: field name = "ans_{question_id}"
    answers = {}
    for q in questions:
        answers[str(q["id"])] = request.form.get(f"ans_{q['id']}", "").strip()

    result = score_quiz(questions, answers)

    # Store quiz level in session — used to annotate recommendations
    session["quiz_level"] = result["level"]

    return render_template("quiz_result.html", result=result)


# ─────────────────────────────────────────────
#  QUIZ — RETAKE
# ─────────────────────────────────────────────
@app.route("/quiz/retake")
@login_required
def quiz_retake():
    session.pop("quiz_ids",  None)
    session.pop("quiz_level", None)
    return redirect(url_for("quiz_start"))
# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)