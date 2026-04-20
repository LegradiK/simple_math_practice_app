import random
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "change-me-in-production"

# ── Digit ranges ─────────────────────────────────────────
ONE_DIGIT   = (1, 9)
TWO_DIGIT   = (10, 99)
THREE_DIGIT = (100, 999)

LEVELS = ("easy", "medium", "hard", "extra_hard", "random")
STYLES = ("inline", "stacked")

DIGIT_CONFIGS = {
    "easy":       [(ONE_DIGIT, ONE_DIGIT)],
    "medium":     [(ONE_DIGIT, TWO_DIGIT), (TWO_DIGIT, ONE_DIGIT)],
    "hard":       [(TWO_DIGIT, TWO_DIGIT)],
    "extra_hard": [(THREE_DIGIT, THREE_DIGIT)],
    "random": [
        (ONE_DIGIT,   ONE_DIGIT),
        (ONE_DIGIT,   TWO_DIGIT),
        (TWO_DIGIT,   ONE_DIGIT),
        (TWO_DIGIT,   TWO_DIGIT),
        (THREE_DIGIT, THREE_DIGIT),
    ],
}

SUBLABEL = {
    "easy":       "1-digit + 1-digit",
    "medium":     "1-digit + 2-digit",
    "hard":       "2-digit + 2-digit",
    "extra_hard": "3-digit + 3-digit",
    "random":     "mixed",
}

# ── Question generator ───────────────────────────────────
def new_question(difficulty="easy"):
    pairs = DIGIT_CONFIGS[difficulty]
    a_range, b_range = random.choice(pairs)
    a = random.randint(*a_range)
    b = random.randint(*b_range)
    return {
        "num1": a,
        "op": "+",
        "num2": b,
        "answer": a + b,
        "sublabel": SUBLABEL[difficulty],
    }

# ── Session init ─────────────────────────────────────────
def init_session():
    session.setdefault("correct", 0)
    session.setdefault("wrong", 0)
    session.setdefault("streak", 0)
    session.setdefault("total", 0)
    session.setdefault("difficulty", "easy")
    session.setdefault("eq_style", "inline")   # ← new
    if "question" not in session:
        session["question"] = new_question(session["difficulty"])

# ── Routes ───────────────────────────────────────────────
@app.route("/")
def index():
    init_session()
    q = session["question"]
    return render_template(
        "index.html",
        num1=q["num1"], op=q["op"], num2=q["num2"],
        sublabel=q.get("sublabel", ""),
        correct=session["correct"],
        wrong=session["wrong"],
        streak=session["streak"],
        total=session["total"],
        difficulty=session["difficulty"],
        eq_style=session["eq_style"],           # ← new
    )

@app.route("/check", methods=["POST"])
def check_answer():
    init_session()
    q = session["question"]
    try:
        user_answer = int(request.form["answer"])
    except (ValueError, KeyError):
        flash("Please enter a whole number.", "info")
        return redirect(url_for("index"))

    session["total"] += 1

    if user_answer == q["answer"]:
        session["correct"] += 1
        session["streak"]  += 1
        flash(f"✓ Correct!  {q['num1']} + {q['num2']} = {q['answer']}", "success")
    else:
        session["wrong"]  += 1
        session["streak"]  = 0
        flash(f"✗ Not quite — the answer was {q['answer']}.", "error")

    session["question"] = new_question(session["difficulty"])
    session.modified = True
    return redirect(url_for("index"))

@app.route("/new")
def new_question_route():
    init_session()
    session["question"] = new_question(session["difficulty"])
    session.modified = True
    return redirect(url_for("index"))

@app.route("/difficulty/<level>")
def set_difficulty(level):
    if level in LEVELS:
        session["difficulty"] = level
        session["question"] = new_question(level)
        session.modified = True
    return redirect(url_for("index"))

@app.route("/style/<style>")           # ← new route
def set_style(style):
    if style in STYLES:
        session["eq_style"] = style
        session.modified = True
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    for key in ("correct", "wrong", "streak", "total", "question"):
        session.pop(key, None)
    # keep eq_style preference across resets
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)