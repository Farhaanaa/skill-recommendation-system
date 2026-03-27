# quiz.py — quiz selection and scoring logic

import random
from quiz_data import QUESTIONS


def select_questions(interests: str, skills: str, n: int = 10) -> list:
    """
    Pick n questions relevant to the user's interests and skills.
    Falls back to random questions from the full bank if not enough matches.
    """
    interest_tokens = set(
        t.strip().lower()
        for t in interests.replace(",", " ").split()
        if t.strip()
    )
    skill_tokens = set(
        t.strip().lower()
        for t in skills.replace(",", " ").split()
        if t.strip()
    )
    combined = interest_tokens | skill_tokens

    # Try to match questions by domain or skill keyword
    relevant, fallback = [], []
    for q in QUESTIONS:
        domain_match = any(t in q["domain"].lower() for t in combined)
        skill_match  = any(t in q["skill"].lower()  for t in combined)
        if domain_match or skill_match:
            relevant.append(q)
        else:
            fallback.append(q)

    # Shuffle both pools
    random.shuffle(relevant)
    random.shuffle(fallback)

    selected = relevant[:n]
    if len(selected) < n:
        selected += fallback[: n - len(selected)]

    return selected[:n]


def score_quiz(questions: list, answers: dict) -> dict:
    """
    Grade submitted answers.
    answers = { str(question_id): "user answer string" }
    Returns score info + per-question breakdown.
    """
    total   = len(questions)
    correct = 0
    breakdown = []

    for q in questions:
        user_ans    = answers.get(str(q["id"]), "").strip()
        is_correct  = user_ans == q["answer"]
        if is_correct:
            correct += 1
        breakdown.append({
            "question":   q["question"],
            "your_answer": user_ans or "Not answered",
            "correct_answer": q["answer"],
            "is_correct": is_correct,
        })

    pct = round(correct / total * 100) if total else 0

    if pct >= 75:
        level = "Advanced"
        message = "Excellent! You have strong domain knowledge."
    elif pct >= 45:
        level = "Intermediate"
        message = "Good foundation — a few gaps to fill."
    else:
        level = "Beginner"
        message = "Great starting point — keep building your skills!"

    return {
        "total":     total,
        "correct":   correct,
        "pct":       pct,
        "level":     level,
        "message":   message,
        "breakdown": breakdown,
    }