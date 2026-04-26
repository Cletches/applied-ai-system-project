# Name of project

This is a Game Glitch Investigator project is a guessing game where the users guess between 3 levels, easy, medium and hard. when the users guesses the game right, they win the game. Each Challenge is meant to be more difficult than the other.

# Game Glitch Investigator: The Impossible Guesser

A Streamlit number-guessing game that was intentionally shipped with bugs. The project demonstrates how to find, fix, test, and evaluate game logic — and how to build a scored evaluation harness that goes beyond basic unit tests.

---

## Architecture Overview

The system has four layers that data flows through from input to output:

```
Player Input / Test Data
        ↓
app.py  (Streamlit UI — session state, rendering)
        ↓
logic_utils.py  (pure game logic — no UI dependencies)
        ↓
Output: Game UI hint + score  OR  Eval report with confidence %
        ↓
Human reviews result and fixes any failures
```

- **app.py** handles the UI, session state, and difficulty settings. It imports all logic from `logic_utils.py`.
- **logic_utils.py** contains the four pure functions: `get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`. No Streamlit imports — fully testable in isolation.
- **eval_harness.py** is a data-driven evaluation script that runs 36 predefined cases, reports pass/fail per case, confidence % per function group, and a final score. Exits with code 1 on any failure for CI compatibility.
- **tests/test_game_logic.py** is the pytest suite covering the same functions with named assertion-level tests.

See `system_diagram.mmd` for the full Mermaid flowchart.

---

## Setup Instructions

**1. Clone the repo and enter the directory**

```bash
git clone <repo-url>
cd applied-ai-system-project
```

**2. Create and activate a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the game**

```bash
python -m streamlit run app.py
```

Opens at http://localhost:8501

**5. Run the eval harness**

```bash
python eval_harness.py
```

**6. Run the pytest suite**

```bash
pytest tests/ -v
```

---

## Sample Interactions

### Example 1 — Correct guess on Easy difficulty

```
Difficulty: Easy  (range 1–5, 4 attempts)
Secret number: 3

Guess: 5  →  "📉 Go LOWER!"
Guess: 2  →  "📈 Go HIGHER!"
Guess: 3  →  "🎉 Correct! You won! Final score: 70"
```

### Example 2 — Running out of attempts on Hard

```
Difficulty: Hard  (range 1–1000, 2 attempts)
Secret number: 847

Guess: 500  →  "📈 Go HIGHER!"
Guess: 200  →  "📈 Go HIGHER!"
→  "Out of attempts! The secret was 847. Score: -10"
```

### Example 3 — Eval harness output (terminal)

```
check_guess      |  confidence: 100.0%  (10/10)
  PASS  exact match int
  PASS  guess too high
  PASS  guess too low
  PASS  int vs str secret win
  ...

parse_guess      |  confidence: 100.0%  (11/11)
  PASS  valid integer
  PASS  float truncated
  PASS  empty string
  ...

Results: 36/36 passed (100.0%)
All cases passed.
```

### Example 4 — Invalid input handling

```
Guess: "abc"  →  "That is not a number."
Guess: ""     →  "Enter a guess."
Guess: "3.9"  →  parsed as 3  (float truncated to int)
```

---

## Design Decisions

**Why separate logic_utils.py from app.py?**
Streamlit reruns the entire script on every user interaction. Mixing game logic with UI code makes functions impossible to test cleanly — importing `app.py` in a test triggers all the Streamlit rendering. Keeping logic in `logic_utils.py` means tests run in milliseconds with no UI side effects.

**Why a custom eval harness instead of just pytest?**
Pytest is great for assertion-level unit tests, but it doesn't produce a scored report. The eval harness defines test cases as data rows (not functions), aggregates results into confidence scores per function group, and prints a summary percentage. This directly satisfies the "Test Harness or Evaluation Script" rubric — measurable output quality across the full input space.

**Why data-driven test cases?**
Defining inputs as a table (label, input, expected output) rather than individual test functions makes it trivial to add new cases without writing boilerplate. It also makes the coverage visible at a glance — you can see exactly which inputs are exercised for each function.

**Trade-offs made:**

- `attempt_limit_map` stays in `app.py` rather than `logic_utils.py` — it's UI config, not core logic. The trade-off is it can't be unit tested without importing Streamlit.
- The eval harness uses ANSI color codes, which won't render in some terminals or CI logs — the output still reads correctly as plain text.
- Score flooring at 10 points (never goes below 10 on a win) is a game design choice, not a bug — though it looks like one without context.

---

## Testing Summary

**What worked well:**

- Separating `logic_utils.py` made all four functions independently testable with zero setup.
- The eval harness caught that the hint direction bug (`Too High` → Go HIGHER) was silently affecting even the string-comparison fallback path — a case pytest alone would have missed without an explicit test.
- Data-driven cases made it easy to add boundary tests (guess = 1, guess = 1000, float input) that revealed edge cases quickly.

**What didn't work initially:**

- The original `app.py` cast the secret to a string on every even attempt number (`if attempts % 2 == 0: secret = str(secret)`), which made winning impossible on those turns. This was subtle — the game appeared to work, just refused to register wins intermittently.
- Hard difficulty was set to range 1–50, making it easier than Normal (1–100). The range ordering invariant test (`hard_high > normal_high`) was the clearest way to document and catch this class of bug.
- The info message was hardcoded to "1–100 / 10 attempts" regardless of difficulty, meaning the UI actively misled the player.

**What I learned:**

- Streamlit reruns the full script on every interaction — any variable not stored in `st.session_state` resets on every button click. This is the most common source of Streamlit bugs.
- A human in the loop is necessary even with AI-generated code. AI tools found several bugs, but also missed some that were only visible by running the app and playing it manually.
- Writing test cases as data first (before writing the assertions) helps clarify what the function is actually supposed to do, which surfaces ambiguity in the spec before it becomes a bug.

# What this project taught you about AI and problem-solving.

- This project taught me that AI makes mistakes and being techinal is still important to figure out where mistakes are and fix them.

---

## Demo

![Fixed winning game](Screenshot%202026-03-05%20at%202.08.29%E2%80%AFPM.png)

## Loom Demo

https://www.loom.com/share/11a4c34882b94d25b4d0adef0a8dff75
