import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import check_guess, get_range_for_difficulty


# --- Existing baseline tests (updated to use app.check_guess) ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug fix: inverted hints ---
# Bug: guess > secret showed "Go HIGHER", guess < secret showed "Go LOWER"

def test_hint_says_go_lower_when_guess_too_high():
    outcome, message = check_guess(75, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in hint, got: {message!r}"

def test_hint_says_go_higher_when_guess_too_low():
    outcome, message = check_guess(25, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint, got: {message!r}"


# --- Bug fix: Hard difficulty range was 1-50 (easier than Normal 1-100) ---
# Bug: Hard returned (1, 50), making it trivially easier than Normal (1, 100)

def test_hard_range_is_harder_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard max ({hard_high}) should be greater than Normal max ({normal_high})"
    )

def test_hard_range_is_1_to_1000():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 1000

def test_easy_range_is_1_to_5():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 5


# --- Bug fix: secret cast to str on even attempts ---
# Bug: on even attempt numbers, secret became a string, so int==str always False
# and int vs str comparison could raise or produce wrong ordering.

def test_check_guess_win_with_string_secret():
    # Simulates the broken even-attempt path: secret is a str, guess is int.
    # After the fix in app.py (secret stays int), this path should not occur,
    # but the fallback in check_guess must still correctly detect a win.
    outcome, _ = check_guess(42, "42")
    assert outcome == "Win", (
        f"check_guess should handle int vs str gracefully for a win, got: {outcome!r}"
    )

def test_check_guess_too_high_with_string_secret():
    # Ensures the TypeError fallback in check_guess returns the correct direction.
    outcome, _ = check_guess(99, "42")
    assert outcome == "Too High"

def test_check_guess_too_low_with_string_secret():
    outcome, _ = check_guess(1, "42")
    assert outcome == "Too Low"
