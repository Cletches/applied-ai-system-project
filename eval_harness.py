"""
Evaluation harness for game logic functions.
Runs predefined test cases, prints pass/fail per case, confidence per group, and a final summary.
Exits with code 1 if any case fails.
"""

import sys
from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score

# ---------------------------------------------------------------------------
# Test case definitions
# ---------------------------------------------------------------------------

CHECK_GUESS_CASES = [
    # (label, guess, secret, expected_outcome, expected_message_contains)
    ("exact match int",           50,  50,   "Win",      "Correct"),
    ("guess too high",            60,  50,   "Too High", "LOWER"),
    ("guess too low",             40,  50,   "Too Low",  "HIGHER"),
    ("guess 1 above secret",      51,  50,   "Too High", "LOWER"),
    ("guess 1 below secret",      49,  50,   "Too Low",  "HIGHER"),
    ("boundary low exact",        1,   1,    "Win",      "Correct"),
    ("boundary high exact",       1000,1000, "Win",      "Correct"),
    ("int vs str secret win",     42,  "42", "Win",      "Correct"),
    ("int vs str secret too high",99,  "42", "Too High", "LOWER"),
    ("int vs str secret too low", 1,   "42", "Too Low",  "HIGHER"),
]

PARSE_GUESS_CASES = [
    # (label, raw_input, expected_ok, expected_value, expected_error_contains)
    ("valid integer",        "42",    True,  42,   None),
    ("valid integer 1",      "1",     True,  1,    None),
    ("valid integer large",  "999",   True,  999,  None),
    ("float truncated",      "3.9",   True,  3,    None),
    ("float exact",          "7.0",   True,  7,    None),
    ("negative integer",     "-1",    True,  -1,   None),
    ("empty string",         "",      False, None, "Enter a guess"),
    ("None input",           None,    False, None, "Enter a guess"),
    ("letters only",         "abc",   False, None, "not a number"),
    ("mixed alphanumeric",   "12abc", False, None, "not a number"),
    ("whitespace only",      "   ",   False, None, "not a number"),
]

GET_RANGE_CASES = [
    # (label, difficulty, expected_low, expected_high)
    ("easy range low",          "Easy",   1,   5),
    ("easy range high",         "Easy",   1,   5),
    ("normal range",            "Normal", 1,   100),
    ("hard range",              "Hard",   1,   1000),
    ("hard harder than normal", "Hard",   None, None),   # special: checks ordering
    ("unknown falls back",      "Expert", 1,   100),
]

UPDATE_SCORE_CASES = [
    # (label, current_score, outcome, attempt_number, expected_score)
    ("win attempt 1 full points",   0,   "Win",      1,  80),   # 100 - 10*(1+1) = 80
    ("win attempt 5 lower points",  0,   "Win",      5,  40),   # 100 - 10*(5+1) = 40
    ("win attempt 9 floor",         0,   "Win",      9,  10),   # 100-100=0 -> floor 10
    ("win attempt 10 floor",        0,   "Win",      10, 10),   # negative -> floor 10
    ("too high even attempt bonus", 50,  "Too High", 2,  55),   # +5
    ("too high odd attempt penalty",50,  "Too High", 3,  45),   # -5
    ("too low penalty",             50,  "Too Low",  1,  45),   # -5
    ("unknown outcome no change",   50,  "Wrong",    1,  50),
    ("score accumulates wins",      80,  "Win",      1,  160),  # 80 + 80
]

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

RESET  = "\033[0m"
GREEN  = "\033[32m"
RED    = "\033[31m"
BOLD   = "\033[1m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"


def _tag(passed: bool) -> str:
    return f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"


def run_check_guess(cases):
    results = []
    for label, guess, secret, exp_outcome, exp_msg_contains in cases:
        outcome, message = check_guess(guess, secret)
        passed = (outcome == exp_outcome) and (exp_msg_contains in message)
        results.append((passed, label, f"guess={guess} secret={secret}",
                        f"outcome={exp_outcome!r} msg contains {exp_msg_contains!r}",
                        f"outcome={outcome!r} msg={message!r}"))
    return results


def run_parse_guess(cases):
    results = []
    for label, raw, exp_ok, exp_val, exp_err in cases:
        ok, val, err = parse_guess(raw)
        if exp_ok:
            passed = ok and (val == exp_val)
        else:
            passed = (not ok) and (err is not None) and (exp_err in err)
        results.append((passed, label, f"raw={raw!r}",
                        f"ok={exp_ok} val={exp_val} err_contains={exp_err!r}",
                        f"ok={ok} val={val} err={err!r}"))
    return results


def run_get_range(cases):
    results = []
    _, normal_high = get_range_for_difficulty("Normal")
    for label, difficulty, exp_low, exp_high in cases:
        if label == "hard harder than normal":
            _, hard_high = get_range_for_difficulty("Hard")
            passed = hard_high > normal_high
            results.append((passed, label, "Hard.high > Normal.high",
                            f"Hard.high > {normal_high}",
                            f"Hard.high={hard_high}"))
        else:
            low, high = get_range_for_difficulty(difficulty)
            passed = (low == exp_low) and (high == exp_high)
            results.append((passed, label, f"difficulty={difficulty!r}",
                            f"({exp_low}, {exp_high})",
                            f"({low}, {high})"))
    return results


def run_update_score(cases):
    results = []
    for label, current, outcome, attempt, expected in cases:
        actual = update_score(current, outcome, attempt)
        passed = actual == expected
        results.append((passed, label,
                        f"score={current} outcome={outcome!r} attempt={attempt}",
                        f"expected={expected}",
                        f"actual={actual}"))
    return results


def print_group(title: str, results: list):
    passed_count = sum(1 for r in results if r[0])
    total = len(results)
    confidence = 100 * passed_count / total if total else 0

    print(f"\n{BOLD}{CYAN}{'─'*60}{RESET}")
    print(f"{BOLD}{CYAN}{title}{RESET}  |  confidence: {confidence:.1f}%  ({passed_count}/{total})")
    print(f"{CYAN}{'─'*60}{RESET}")

    for passed, label, inputs, expected, actual in results:
        tag = _tag(passed)
        print(f"  {tag}  {label}")
        if not passed:
            print(f"        input:    {inputs}")
            print(f"        expected: {expected}")
            print(f"        actual:   {actual}")

    return passed_count, total


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"\n{BOLD}{'='*60}")
    print("  GAME LOGIC EVALUATION HARNESS")
    print(f"{'='*60}{RESET}")

    groups = [
        ("check_guess",            run_check_guess(CHECK_GUESS_CASES)),
        ("parse_guess",            run_parse_guess(PARSE_GUESS_CASES)),
        ("get_range_for_difficulty", run_get_range(GET_RANGE_CASES)),
        ("update_score",           run_update_score(UPDATE_SCORE_CASES)),
    ]

    total_passed = 0
    total_cases  = 0
    all_failures = []

    for title, results in groups:
        p, t = print_group(title, results)
        total_passed += p
        total_cases  += t
        for r in results:
            if not r[0]:
                all_failures.append((title, r[1], r[2], r[3], r[4]))

    overall_pct = 100 * total_passed / total_cases if total_cases else 0

    print(f"\n{BOLD}{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}{RESET}")
    print(f"  Total:   {total_cases} cases")
    print(f"  Passed:  {GREEN}{total_passed}{RESET}")
    print(f"  Failed:  {RED}{total_cases - total_passed}{RESET}")
    print(f"  Score:   {BOLD}{overall_pct:.1f}%{RESET}")

    if all_failures:
        print(f"\n{RED}{BOLD}  FAILED CASES:{RESET}")
        for func, label, inputs, expected, actual in all_failures:
            print(f"  [{func}] {label}")
            print(f"    input:    {inputs}")
            print(f"    expected: {expected}")
            print(f"    actual:   {actual}")
        print()
        sys.exit(1)
    else:
        print(f"\n{GREEN}{BOLD}  All cases passed.{RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
