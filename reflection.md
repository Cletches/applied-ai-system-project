# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  The game just asked me to guess a number and predicts whether it was right or wrong. It had some levels to choose from as well.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  So the hard level was easier than the normal and also the number I guessed if bigger than the secret number will still say go higher. The info message "Guess a number between 1 and 100" was hardcoded

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  Claude Code

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  I found a couple of bug and made the AI found some bugs as well which I saw also needed to be fixed

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I knew what the issue was. So after the fix, I tested with lots of cases and it passed.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  So when I switch between levels, the info message was hardcoded and did not change. So after fixing, I switched between all levels and made sure info message changed evertime

- Did AI help you design or understand any tests? How?
  yes in my 2nd bug. the issue was hints were reversed: if guess > secrete, it would still say go higher. I fix it with AI and it developed some test cases which worked. I also tried to run the app and test which also works so it prompts user to go lower when guess > score.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  The secret number kept changing because Streamlit reruns the entire script from top to bottom every time the user interacts with the page. Without session state, random.randint()` was called fresh on every rerun, generating a new secret each time the user clicked a button or typed a guess.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Imagine every time you click a button on a website, the whole page reloads from scratch and forgets everything. That's Streamlit — every interaction triggers a full rerun of your Python script. Session state is like a sticky notepad that survives those reruns, so you can write values down (like the secret number or the attempt count) and they'll still be there the next time the script runs.

- What change did you make that finally gave the game a stable secret number?
  I wrapped the secret generation in an if "secret" not in st.session_state check, so it only generates a new random number the very first time the page loads. After that, the secret is stored in session state and reused on every subsequent rerun. I also added a check for when the difficulty changes, so the secret resets to a value within the new range.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
- This could be a testing habit, a prompting strategy, or a way you used Git.
  Finding bugs on my own before allowing the AI to find. I was able to find some bugs the AI could not notice

- What is one thing you would do differently next time you work with AI on a coding task?
  I would try and understand the code first before prompting
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  I sometime overestimate the abilities of AI , I will say have a human in the loop is always needed for better results

Challenge 5: AI Model Comparison:
I realized all the models wrote code fixes for me without they seeing the original code, which can cause issues. Comparing the responses, only one model's fix fit directly into my code however, I still need to be cautious since the model guessed a right response without seeing the original code

## 6. What are the limitations or biases in your system?

Test cases are predefined and work. Maybe additional test cases could help improve it

## 7. Could your AI be misused, and how would you prevent that?

Yes. The model can say there are no bugs but when I tested some features I found some bugs. So it is always better to manually test the product to prevent unexpected issues.

## 8. What surprised you while testing your AI's reliability?

It wrote good test cases that I could not think of at the moment but missed some few test cases as well. So it is important to always think about the problem and not let the model do all the thinking

## 9. describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.

As previously stated, it was good in debugging and writing test cases. Where the flaw was is when it missed basic test cases. I manually tested them and realised there were still some issues. It if very important to test the product and features always.
