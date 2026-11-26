# U know enough?

Learning and reviewing general knowledge can be repetitive when information is only studied by reading, when it can be way more interacting getting general knowledge acquired, while receiving immediate feedback about their answers.
For this reason, my project will create a quiz game in which the player can answer questions, earn points, advance through different difficulty levels, and see their final results.

My project is going to be an interactive game of general knowledge questions, called U know enough?. Which is an interactive general knowledge game with three levels: Easy, Medium and Hard. The questions of each level are stored in a text file, with 15 multiple choice questions per level and four possible answers (A, B, C or D) for each one. Every time a level starts, the program randomly selects 10 questions, and the order of the answers is also shuffled. 

Each correct answer gives 10 points, and every 3 correct answers in a row give 5 bonus points. To pass a level, the player must get at least 60% correct (6 out of 10). Passing a level unlocks the next one. After every level, the result is saved in a history file, so the player can later check the game history and a Top 5 ranking. I think this will be an interesting game because it challenges the player to learn and show their knowledge. 

Each correct answer gives 10 points, and every 3 correct answers in a row give 5 bonus points. To pass a level, the player must get at least 60% correct (6 out of 10). Passing a level unlocks the next one. After every level, the result is saved in a history file, so the player can later check the game history and a Top 5 ranking. I think this will be an interesting game because it challenges the player to learn and show their knowledge. 

**Algorithm** 
1. Start the program, load the questions from the text files and load the saved history.
2. Show the main menu: Play, Instructions, Game history, Top 5 ranking and Exit.
3. Ask for an option. If it is not a valid number, ask again.
4. If the player chooses Instructions, show the rules.
5. If the player chooses Game history, show the saved results and the average score.
6.If the player chooses Top 5 ranking, sort the results by score and show the best 5
7.If the player chooses Play, ask for their name (only letters, 2 to 15 characters).
8.Start with the Easy level and pick 10 random questions from it.
9.For each question, show it with the four options A, B, C and D in random order. 10.Ask for an answer, and if it is not A, B, C or D, ask again.
11. If the answer is correct, show "Correct!" and add 10 points. Every 3 correct answers in a row give 5 extra points.
12.If the answer is wrong, show "Incorrect!" and the correct answer. The streak starts again.
13. After the 10 questions, show the correct answers, incorrect answers, score and percentage. Save the result in the history file.
14.If the player got 60% or more, they pass and can continue to the next level (go back to step 8). If they pass the Hard level, show a congratulations message.
15. If the player got less than 60%, the game ends.
16.Show the total score of the game and go back to the menu.
17. If the player chooses Exit, say goodbye and close the program.

