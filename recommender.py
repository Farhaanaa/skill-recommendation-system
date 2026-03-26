import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# ─────────────────────────────────────────────
#  LOAD DATASET
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "projects.csv")

df = pd.DataFrame()  # global, loaded once


def load_dataset():
    global df
    df = pd.read_csv(DATASET_PATH)
    # Combine all text columns into a single searchable string per project
    df["combined"] = (
        df["title"].fillna("") + " " +
        df["domain"].fillna("") + " " +
        df["required_skills"].fillna("") + " " +
        df["tools"].fillna("") + " " +
        df["difficulty"].fillna("") + " " +
        df["description"].fillna("") + " " +
        df["career_alignment"].fillna("") + " " +
        df["tags"].fillna("")
    )
    df["combined"] = df["combined"].str.lower()
    return df


# Load once at import time
load_dataset()


# ─────────────────────────────────────────────
#  BUILD USER PROFILE STRING
# ─────────────────────────────────────────────
def build_user_profile(
    interests="",
    qualification="",
    course="",
    career="",
    career_goal="",
    skills="",
    certifications="",
    tools_known="",
    what_they_know=""
):
    """
    Combine all user inputs into a single weighted text string.
    Skills + interests are repeated to boost their influence in TF-IDF.
    """
    profile_parts = [
        interests,        # e.g. "machine learning, data science"
        interests,        # repeated → higher TF-IDF weight
        skills,           # e.g. "python, pandas, sklearn"
        skills,           # repeated
        career_goal,      # e.g. "Data Scientist"
        career_goal,      # repeated
        career,
        qualification,
        course,
        certifications,
        tools_known,
        what_they_know,
    ]
    profile = " ".join([p for p in profile_parts if p]).lower()
    # Normalise: replace commas with spaces so tokeniser treats each skill separately
    profile = profile.replace(",", " ").replace(";", " ")
    return profile


# ─────────────────────────────────────────────
#  DIFFICULTY MAPPING
# ─────────────────────────────────────────────
DIFFICULTY_RANK = {"beginner": 1, "intermediate": 2, "advanced": 3}

def infer_user_level(skills: str, what_they_know: str, certifications: str) -> str:
    """
    Heuristic: count how many meaningful skills the user has.
    Returns 'Beginner' | 'Intermediate' | 'Advanced'
    """
    combined = f"{skills} {what_they_know} {certifications}".lower()
    tokens = [t.strip() for t in combined.replace(",", " ").split() if len(t.strip()) > 2]
    unique = set(tokens)
    count = len(unique)
    if count <= 5:
        return "Beginner"
    elif count <= 14:
        return "Intermediate"
    else:
        return "Advanced"


def difficulty_score(project_difficulty: str, user_level: str) -> float:
    """
    Returns a bonus/penalty score (-0.1 to +0.1) based on
    how well the project difficulty matches user level.
    Slightly stretch → small penalty; completely mismatched → bigger penalty.
    """
    pd_rank = DIFFICULTY_RANK.get(project_difficulty.lower(), 2)
    ul_rank = DIFFICULTY_RANK.get(user_level.lower(), 1)
    diff = pd_rank - ul_rank
    if diff == 0:
        return 0.10   # perfect match bonus
    elif diff == 1:
        return 0.03   # one step above → mild stretch, acceptable
    elif diff == -1:
        return 0.05   # one step below → easy win
    else:
        return -0.08  # two steps away → penalise


# ─────────────────────────────────────────────
#  SKILL GAP DETECTION
# ─────────────────────────────────────────────
def detect_skill_gaps(user_skills_raw: str, project_required_skills: str):
    """
    Compare user skills vs project required skills.
    Returns dict with matched and missing lists.
    """
    user_set = set(
        s.strip().lower()
        for s in user_skills_raw.replace(",", " ").split()
        if s.strip()
    )
    required_list = [s.strip().lower() for s in project_required_skills.split(",") if s.strip()]
    
    matched = [s for s in required_list if s in user_set]
    missing = [s for s in required_list if s not in user_set]

    total = len(required_list) if required_list else 1
    match_pct = round(len(matched) / total * 100)

    return {
        "matched": matched,
        "missing": missing,
        "match_pct": match_pct,
    }


# ─────────────────────────────────────────────
#  EXPLANATION GENERATOR
# ─────────────────────────────────────────────
def generate_explanation(row, user_profile_data: dict, gap_info: dict) -> str:
    """
    Human-readable explanation of why this project was recommended.
    """
    lines = []

    # Skill match
    if gap_info["matched"]:
        matched_str = ", ".join(gap_info["matched"][:4])
        lines.append(
            f"Your skills in <strong>{matched_str}</strong> directly match "
            f"what this project requires ({gap_info['match_pct']}% skill match)."
        )

    # Career alignment
    career_goal = user_profile_data.get("career_goal", "").strip()
    career_alignment = str(row.get("career_alignment", ""))
    if career_goal and career_goal.lower() in career_alignment.lower():
        lines.append(
            f"This project aligns with your career goal of becoming a "
            f"<strong>{career_goal}</strong>."
        )
    elif career_alignment:
        lines.append(
            f"This project is commonly pursued by <strong>{career_alignment}</strong>."
        )

    # Interests
    interests = user_profile_data.get("interests", "").lower()
    domain = str(row.get("domain", "")).lower()
    tags = str(row.get("tags", "")).lower()
    interest_list = [i.strip() for i in interests.replace(",", " ").split() if i.strip()]
    matched_interests = [i for i in interest_list if i in tags or i in domain]
    if matched_interests:
        lines.append(
            f"Your interest in <strong>{', '.join(matched_interests[:3])}</strong> "
            f"makes this a great fit."
        )

    # Difficulty
    difficulty = str(row.get("difficulty", "Intermediate"))
    lines.append(
        f"The difficulty level is <strong>{difficulty}</strong>, "
        f"which suits your current profile."
    )

    # Missing skills nudge
    if gap_info["missing"]:
        missing_str = ", ".join(gap_info["missing"][:3])
        lines.append(
            f"You'll also get to learn <strong>{missing_str}</strong> "
            f"along the way — great for growth!"
        )

    return " ".join(lines) if lines else "This project is a strong match for your overall profile."


# ─────────────────────────────────────────────
#  CORE RECOMMENDATION FUNCTION
# ─────────────────────────────────────────────
def get_recommendations(
    interests="",
    qualification="",
    course="",
    career="",
    career_goal="",
    skills="",
    certifications="",
    tools_known="",
    what_they_know="",
    top_n=5
):
    """
    Main entry point called from Flask routes.

    Returns a list of dicts, each representing a recommended project:
    {
        title, domain, difficulty, description, career_alignment,
        resources, estimated_days, required_skills,
        matched_skills, missing_skills, match_pct,
        similarity_score, explanation
    }
    """
    if df.empty:
        load_dataset()

    user_profile_data = {
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

    # 1. Build user profile string
    user_profile_str = build_user_profile(**user_profile_data)

    if not user_profile_str.strip():
        return []

    # 2. TF-IDF vectorisation
    corpus = list(df["combined"]) + [user_profile_str]
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),   # unigrams + bigrams (e.g. "machine learning")
        stop_words="english",
        min_df=1,
    )
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # User vector is the last row
    user_vec = tfidf_matrix[-1]
    project_vecs = tfidf_matrix[:-1]

    # 3. Cosine similarity
    similarity_scores = cosine_similarity(user_vec, project_vecs).flatten()

    # 4. Difficulty bonus
    user_level = infer_user_level(skills, what_they_know, certifications)
    adjusted_scores = []
    for i, score in enumerate(similarity_scores):
        bonus = difficulty_score(df.iloc[i]["difficulty"], user_level)
        adjusted_scores.append(score + bonus)

    adjusted_scores = np.array(adjusted_scores)

    # 5. Rank and pick top_n
    top_indices = adjusted_scores.argsort()[::-1][:top_n]

    results = []
    for idx in top_indices:
        row = df.iloc[idx]
        gap = detect_skill_gaps(skills, str(row.get("required_skills", "")))
        explanation = generate_explanation(row, user_profile_data, gap)

        results.append({
            "title": row.get("title", ""),
            "domain": row.get("domain", ""),
            "difficulty": row.get("difficulty", ""),
            "description": row.get("description", ""),
            "career_alignment": row.get("career_alignment", ""),
            "resources": row.get("resources", ""),
            "estimated_days": row.get("estimated_days", ""),
            "required_skills": row.get("required_skills", ""),
            "tools": row.get("tools", ""),
            "tags": row.get("tags", ""),

            # Skill gap info
            "matched_skills": gap["matched"],
            "missing_skills": gap["missing"],
            "match_pct": gap["match_pct"],

            # Scores
            "similarity_score": round(float(adjusted_scores[idx]), 4),
            "user_level": user_level,

            # Explanation
            "explanation": explanation,
        })

    return results