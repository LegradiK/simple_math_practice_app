import random
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv

load_dotenv("data.env")

app = Flask(__name__)
app.secret_key = os.getenv("KEY")

ONE_DIGIT   = (1, 9)
TWO_DIGIT   = (10, 99)
THREE_DIGIT = (100, 999)

CALC_TYPES = ("addition", "subtraction", "multiplication", "division")
LEVELS = ("easy", "medium", "hard", "extra_hard", "random")
STYLES = ("inline", "stacked")

DIGIT_CONFIGS = {
    "easy":       [(ONE_DIGIT, ONE_DIGIT)],
    "medium":     [(ONE_DIGIT, TWO_DIGIT), (TWO_DIGIT, ONE_DIGIT)],
    "hard":       [(TWO_DIGIT, TWO_DIGIT)],
    "extra_hard": [(THREE_DIGIT, THREE_DIGIT)],
    "random": [
        (ONE_DIGIT,  ONE_DIGIT),
        (ONE_DIGIT,  TWO_DIGIT),
        (TWO_DIGIT,  ONE_DIGIT),
        (TWO_DIGIT,  TWO_DIGIT),
        (THREE_DIGIT, THREE_DIGIT),
    ],
}

OP_SYMBOL = {
    "addition":       "+",
    "subtraction":    "−",
    "multiplication": "×",
    "division":       "÷",
}

def new_question(difficulty="easy", calc_type="addition"):
    pairs = DIGIT_CONFIGS[difficulty]
    a_range, b_range = random.choice(pairs)
    a = random.randint(*a_range)
    b = random.randint(*b_range)

    if calc_type == "subtraction":
        if a < b:
            a, b = b, a          # keep result positive
        op, answer = "−", a - b
    elif calc_type == "multiplication":
        # clamp to single/two digit to keep numbers sane
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op, answer = "×", a * b
    elif calc_type == "division":
        b = random.randint(*ONE_DIGIT)
        answer = random.randint(*ONE_DIGIT)
        a = b * answer           # guarantee whole-number result
        op, answer = "÷", answer
    else:
        op, answer = "+", a + b

    return {"num1": a, "op": op, "num2": b, "answer": answer}


def init_session():
    session.setdefault("correct", 0)
    session.setdefault("wrong", 0)
    session.setdefault("streak", 0)
    session.setdefault("total", 0)
    session.setdefault("difficulty", "easy")
    session.setdefault("calc_type", "addition")
    session.setdefault("eq_style", "inline")
    if "question" not in session:
        session["question"] = new_question(session["difficulty"], session["calc_type"])


@app.route("/")
def index():
    init_session()
    q = session["question"]
    return render_template(
        "index.html",
        num1=q["num1"], op=q["op"], num2=q["num2"],
        correct=session["correct"],
        wrong=session["wrong"],
        streak=session["streak"],
        total=session["total"],
        difficulty=session["difficulty"],
        calc_type=session["calc_type"],
        eq_style=session["eq_style"],
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
        flash(f"✓ Correct!  {q['num1']} {q['op']} {q['num2']} = {q['answer']}", "success")
    else:
        session["wrong"]  += 1
        session["streak"]  = 0
        flash(f"✗ Not quite : {q['num1']} {q['op']} {q['num2']} = {q['answer']}, you answered {user_answer}.", "error")

    session["question"] = new_question(session["difficulty"], session["calc_type"])
    session.modified = True
    return redirect(url_for("index"))


@app.route("/new")
def new_question_route():
    init_session()
    session["question"] = new_question(session["difficulty"], session["calc_type"])
    session.modified = True
    return redirect(url_for("index"))


# ── Two separate routes — no more shared broken signature ──

@app.route("/type/<calc_type>")
def set_type(calc_type):
    if calc_type in CALC_TYPES:
        session["calc_type"] = calc_type
        session["question"] = new_question(session.get("difficulty", "easy"), calc_type)
        session.modified = True
    return redirect(url_for("index"))


@app.route("/difficulty/<level>")
def set_difficulty(level):
    if level in LEVELS:
        session["difficulty"] = level
        session["question"] = new_question(level, session.get("calc_type", "addition"))
        session.modified = True
    return redirect(url_for("index"))


@app.route("/style/<style>")
def set_style(style):
    if style in STYLES:
        session["eq_style"] = style
        session.modified = True
    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    for key in ("correct", "wrong", "streak", "total", "question"):
        session.pop(key, None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)