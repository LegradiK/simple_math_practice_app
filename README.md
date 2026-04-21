# MathDrill

A clean, browser-based arithmetic practice app built with Flask, aimed at **preschool and primary school children** to practise their maths skills at home. Questions are presented in a friendly format with instant feedback, streaks, and adjustable difficulty to grow with the child.

---

## Who Is This For?

MathDrill is designed for young learners at home — preschoolers working on basic number bonds, and primary school children building confidence with larger numbers. A parent or teacher can set the difficulty and operation, then hand the device to the child to practise independently.

---

## How to Use

1. **Choose an operation** — tap one of the four buttons: `+` `−` `×` `÷`
2. **Choose a difficulty level** — the options change depending on the operation selected
3. **Choose a layout** — Inline (`5 + 8 = ?`) or Column (stacked format, like written maths)
4. **Type the answer** and press **Check**
5. Instant feedback shows whether the answer was right, along with the full equation
6. Use **Skip** to move to a new question, or **Reset** to clear the scores

---

## Features

- **Four operations** — Addition, Subtraction, Multiplication, Division
- **Age-appropriate number ranges** — tailored per operation (see Difficulty Levels below)
- **Difficulty levels** — Easy through Extra Hard, with a Random mix option
- **Two question layouts** — Inline (`5 + 8 = ?`) or Column (stacked, like school worksheets)
- **Score tracking** — Correct, Wrong, Streak, and Total counters per session
- **Instant feedback** — shows the full formula and correct answer after each attempt
- **Persistent preferences** — layout and difficulty survive score resets

---

## Project Structure

```
math_drill/
├── main.py               # Flask app, routes, question logic
├── templates/
│   └── index.html        # Jinja2 template
├── static/
│   └── style.css         # All styling
└── README.md
```

---

## Setup

**Requirements:** Python 3.8+

```bash
# 1. Clone or download the project
cd math_drill

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install flask

# 4. Run the app
python main.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Difficulty Levels

Difficulty options vary by operation to keep numbers age-appropriate.

**Addition & Subtraction**

| Level      | Numbers involved       |
|------------|------------------------|
| Easy       | 1-digit + 1-digit      |
| Medium     | 1-digit + 2-digit      |
| Hard       | 2-digit + 2-digit      |
| Extra Hard | 3-digit + 3-digit      |
| Random     | All of the above mixed |

**Multiplication**

Only numbers 1–10 are used (e.g. `7 × 8`). One difficulty level covering the full times tables range.

**Division**

| Level | Numbers involved        |
|-------|-------------------------|
| Easy  | 1-digit ÷ 1-digit       |
| Hard  | 2-digit ÷ 1-digit       |

All division questions are guaranteed to produce whole-number answers.

---

## Routes

| Route                    | Description                          |
|--------------------------|--------------------------------------|
| `GET /`                  | Main page, shows current question    |
| `POST /check`            | Submit an answer                     |
| `GET /new`               | Skip to a new question               |
| `GET /type/<calc_type>`  | Switch operation (addition etc.)     |
| `GET /difficulty/<level>`| Change difficulty level              |
| `GET /style/<style>`     | Toggle inline / stacked layout       |
| `GET /reset`             | Reset scores (keeps preferences)     |

---

## Configuration

Create a `data.env` file in the same folder as `main.py`:

```
KEY=your-secret-key-here
```

This is loaded automatically on startup. Keep `data.env` out of version control by adding it to `.gitignore`.

All session state (scores, preferences, current question) is stored in a signed client-side cookie via Flask's session.

---

## Dependencies

| Package        | Purpose                        |
|----------------|--------------------------------|
| Flask          | Web framework                  |
| python-dotenv  | Loads secret key from data.env |

No database required — all state lives in the session.

Install both with:

```bash
pip install flask python-dotenv
```