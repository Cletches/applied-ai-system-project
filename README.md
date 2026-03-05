# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: _"How do I keep a variable from resetting in Streamlit when I click a button?"_
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
      It is a guessing game where we guess to get a specific number. There are 3 levels, easy hard and normal. The game also gives hint to go lower or higher depnding on the user's input

- [ ] Detail which bugs you found.
      I found that the hard level was not the hardest level so I fixed that. Also the info message was hardcoded so it dod not reflect when levels were switched. I also saw that it was difficult to get the right guess since the boundaries of each level were not a true reflection of where the secret number was

- [ ] Explain what fixes you applied.
      I fixed the hardcoded info message. I also fixed the levels making the hard level have a higher range of number compared to easy and normal, and also normal being higher than easy. I also fixed the boundaries range so the secret number was inbound of the level range at all times

## 📸 Demo

![Fixed winning game](Screenshot%202026-03-05%20at%202.08.29%E2%80%AFPM.png)

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
