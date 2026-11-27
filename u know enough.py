# U KNOW ENOUGH?

# Quiz game of general knowledge with three levels (Easy, Medium
# and Hard). The questions are loaded from text files, 10 random questions
# are asked per level, and the player earns points for correct answers and
# for streaks. The player needs 60% to pass a level and unlock the next
# one. Every result is saved in a history file, and the player can check
# the game history and a Top 5 ranking.

#Hope you like it teacher, i gave it all :) 

import math
import random
from datetime import datetime

LETTERS = "ABCD"
PASS_PERCENTAGE = 60
POINTS_PER_QUESTION = 10
STREAK_LENGTH = 3
STREAK_BONUS = 5
QUESTIONS_PER_LEVEL = 10
SEPARATOR = "|"
HISTORY_FILE = "history.txt"

LEVEL_NAMES = ["EASY", "MEDIUM", "HARD"]
LEVEL_FILES = [
    "easyquestions.txt",
    "mediumquestions.txt",
    "hardquestions.txt",
]

# FILES
# Functionality: Reads one question file and builds a matrix of questions.
# Input: filename (string), the name of the text file to read.
# Process: Opens the file and reads it line by line. Splits each line by
#   "|", removes extra spaces and keeps only the lines with exactly 5
#   parts (titles and blank lines are skipped). If the file does not
#   exist, it prints an error message.
# Output: Matrix (list of lists). Each row = [question, correct answer,
#   wrong answer 1, wrong answer 2, wrong answer 3].
def load_questions(filename):
    questions = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(SEPARATOR)
                row = []
                for part in parts:
                    row.append(part.strip())
                if len(row) == 5:
                    questions.append(row)
    except FileNotFoundError:
        print("Error: the file", filename, "was not found.")

    return questions


# Functionality: Loads the questions of the three levels.
# Input: None.
# Process: Calls load_questions() once for each level file (easy, medium
#   and hard) and stores each matrix in a list.
# Output: List with the 3 matrices, or an empty list if any file is
#   missing or has no questions.
def load_all_levels():
    all_levels = []

    for filename in LEVEL_FILES:
        questions = load_questions(filename)
        if len(questions) == 0:
            return []
        all_levels.append(questions)

    return all_levels


# Functionality: Loads the saved results from the history file.
# Input: None.
# Process: Reads history.txt line by line and splits each line by "|".
#   Skips damaged lines (wrong number of parts or non-numeric values).
#   If the file does not exist yet, the history stays empty.
# Output: Matrix with the saved results. Each row = [date, player, level,
#   correct answers, score, percentage, result].
def load_history():
    history = []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            for line in file:
                row = line.strip().split(SEPARATOR)
                if (len(row) == 7 and row[3].isdigit()
                        and row[4].isdigit() and row[5].isdigit()):
                    history.append(row)
    except FileNotFoundError:
        pass    # first time playing: there is no history yet

    return history


# Functionality: Saves one result in the history file.
# Input: row (list of strings), the result of one level.
# Process: Joins the parts of the row with "|" and adds the line at the
#   end of history.txt (mode "a" keeps the previous results).
# Output: None (the file is updated).
def save_result(row):
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(SEPARATOR.join(row) + "\n")


# MENU AND INSTRUCTIONS
# Functionality: Shows the main menu.
# Input: None.
# Process: Prints the five options of the menu.
# Output: None (prints on the screen).
def show_menu():
    print("\n-------------------------")
    print("      U KNOW ENOUGH?")
    print("-------------------------")
    print("1. Play")
    print("2. Instructions")
    print("3. Game history")
    print("4. Top 5 ranking")
    print("5. Exit")


# Functionality: Shows the rules of the game.
# Input: None.
# Process: Prints the levels, the points, the streak bonus and the
#   percentage needed to pass a level.
# Output: None (prints on the screen).
def show_instructions():
    print("\n-------------------------")
    print("      INSTRUCTIONS")
    print("-------------------------")
    print("There are", len(LEVEL_NAMES), "levels:",
          ", ".join(LEVEL_NAMES) + ".")
    print("Each level has", QUESTIONS_PER_LEVEL, "random questions.")
    print("Each question has four options: A, B, C or D.")
    print("Each correct answer gives you", POINTS_PER_QUESTION, "points.")
    print("Every", STREAK_LENGTH, "correct answers in a row give you",
          STREAK_BONUS, "extra points.")
    print("You need at least", str(PASS_PERCENTAGE) + "% to pass a level.")
    print("Pass a level to unlock the next one!")


# INPUT VALIDATION
# Functionality: Reads a valid menu option.
# Input: minimum and maximum (integers), the range of valid options.
# Process: Asks for an option and repeats the question until the player
#   types a whole number inside the range.
# Output: The chosen option (integer).
def read_menu_option(minimum, maximum):
    option = input("Select an option: ").strip()

    while (not option.isdigit() or int(option) < minimum
           or int(option) > maximum):
        print("Invalid option. Please enter a number from",
              minimum, "to", str(maximum) + ".")
        option = input("Select an option: ").strip()

    return int(option)


# Functionality: Reads a valid player name.
# Input: None (the name is typed by the player).
# Process: Asks for the name and repeats until it has 2 to 15 characters
#   and only letters and spaces.
# Output: The name (string) with a capital letter in each word.
def read_player_name():
    name = input("\nEnter your name: ").strip()

    while (len(name) < 2 or len(name) > 15
           or not name.replace(" ", "").isalpha()):
        print("Invalid name. Use only letters (2 to 15 characters).")
        name = input("Enter your name: ").strip()

    return name.title()


# Functionality: Reads a Y/N answer.
# Input: message (string), the question shown to the player.
# Process: Shows the message and repeats until the player types Y or N.
# Output: True if the player typed Y, False if the player typed N.
def read_yes_no(message):
    answer = input(message).strip().upper()

    while answer != "Y" and answer != "N":
        print("Invalid answer. Please enter Y or N.")
        answer = input(message).strip().upper()

    return answer == "Y"


# QUESTIONS
# Functionality: Shows one question and reads the answer.
# Input: number (int), total (int), question (string) and options (list
#   with the 4 answers).
# Process: Prints the question number, the question and the options A, B,
#   C and D. Asks for an answer and repeats until it is A, B, C or D.
# Output: The chosen letter (string) in capital letters.
def ask_question(number, total, question, options):
    print("\nQuestion " + str(number) + "/" + str(total))
    print(question)

    for i in range(len(options)):
        print(LETTERS[i] + ")", options[i])

    answer = input("Your answer: ").strip().upper()

    while len(answer) != 1 or answer not in LETTERS:
        print("Invalid answer.")
        answer = input("Please enter A, B, C or D: ").strip().upper()

    return answer


# Functionality: Checks if the player's answer is correct.
# Input: player_answer (letter), correct_letter (letter) and correct_text
#   (string, the text of the right answer).
# Process: Compares both letters and prints "Correct!" or "Incorrect!"
#   (showing the right answer when the player fails).
# Output: True if the answer was correct, False if not.
def check_answer(player_answer, correct_letter, correct_text):
    if player_answer == correct_letter:
        print("Correct!")
        return True

    print("Incorrect!")
    print("The correct answer was:", correct_letter + ")", correct_text)
    return False


# Functionality: Calculates the percentage of correct answers.
# Input: correct_answers (int) and total_questions (int).
# Process: Divides the correct answers by the total and multiplies by 100.
# Output: The percentage (float).
def calculate_percentage(correct_answers, total_questions):
    return (correct_answers / total_questions) * 100


# Functionality: Plays one level of the game.
# Input: level_name (string) and questions (matrix of the level).
# Process: Picks random questions with random.sample. For each one it
#   shuffles the options, finds the correct letter, asks the question and
#   checks the answer. Each correct answer adds 10 points, and every 3
#   correct answers in a row add 5 bonus points. A wrong answer resets
#   the streak.
# Output: correct answers (int), score (int) and total questions asked
#   (int).
def play_level(level_name, questions):
    # https://docs.python.org/3/library/random.html#random.sample
    amount = min(QUESTIONS_PER_LEVEL, len(questions))
    selected = random.sample(questions, amount)

    correct_answers = 0
    score = 0
    streak = 0

    print("\n-------------------------")
    print("       " + level_name + " LEVEL")
    print("-------------------------")

    # https://docs.python.org/3/library/functions.html#enumerate
    for number, row in enumerate(selected, start=1):
        question = row[0]
        correct_text = row[1]

        options = row[1:]    # slicing creates a new list
        random.shuffle(options)
        correct_letter = LETTERS[options.index(correct_text)]

        answer = ask_question(number, amount, question, options)

        if check_answer(answer, correct_letter, correct_text):
            correct_answers = correct_answers + 1
            score = score + POINTS_PER_QUESTION
            streak = streak + 1

            if streak % STREAK_LENGTH == 0:
                score = score + STREAK_BONUS
                print("Streak bonus! +" + str(STREAK_BONUS), "points")
        else:
            streak = 0

    return correct_answers, score, amount


# RESULTS
# Functionality: Shows the results of a level.
# Input: level_name (string), correct_answers (int), score (int) and
#   total_questions (int).
# Process: Calculates the incorrect answers and the percentage, and
#   prints the results. If the player failed, it uses math.ceil to show
#   how many correct answers were needed.
# Output: True if the player passed (60% or more), False if not.
def show_results(level_name, correct_answers, score, total_questions):
    incorrect_answers = total_questions - correct_answers
    percentage = calculate_percentage(correct_answers, total_questions)

    print("\n-------------------------")
    print("        RESULTS")
    print("-------------------------")

    print("Level:", level_name)
    print("Correct answers:", correct_answers)
    print("Incorrect answers:", incorrect_answers)
    print("Score:", score, "points")
    print("Percentage:", f"{percentage:.0f}%")

    if percentage >= PASS_PERCENTAGE:
        print("You passed the", level_name.capitalize(), "Level!")
        return True

    # https://docs.python.org/3/library/math.html#math.ceil
    needed = math.ceil(total_questions * PASS_PERCENTAGE / 100)
    missing = needed - correct_answers

    print("You did not pass the", level_name.capitalize(), "Level.")
    print("You needed", needed, "correct answers to pass.")
    print("You were", missing, "correct answer(s) away.")
    return False


# HISTORY AND RANKING
# Each row = [date, player, level, correct, score, percentage, result]
# Functionality: Gets the score of a history row.
# Input: row (list), one row of the history.
# Process: Converts the score (position 4 of the row) to an integer.
# Output: The score (int). It is used as the sorting key in the ranking.
def get_score(row):
    return int(row[4])


# Functionality: Calculates the average score of the history.
# Input: history (matrix with the saved results).
# Process: Adds the score of every row and divides by the number of rows.
# Output: The average score (float).
def calculate_average_score(history):
    total = 0

    for row in history:
        total = total + get_score(row)

    return total / len(history)


# Functionality: Prints one result as a line of the table.
# Input: row (list), one row of the history.
# Process: Prints each part of the row in a column of fixed width.
# Output: None (prints on the screen).
def print_history_row(row):
    print(row[0].ljust(18) + row[1].ljust(16) + row[2].ljust(9)
          + row[3].ljust(9) + row[4].ljust(7)
          + (row[5] + "%").ljust(6) + row[6])


# Functionality: Prints the header of the history table.
# Input: None.
# Process: Prints the column titles and a separator line.
# Output: None (prints on the screen).
def print_table_header():
    print("DATE".ljust(18) + "PLAYER".ljust(16) + "LEVEL".ljust(9)
          + "CORRECT".ljust(9) + "SCORE".ljust(7) + "%".ljust(6)
          + "RESULT")
    print("-" * 70)


# Functionality: Shows all the saved results.
# Input: history (matrix with the saved results).
# Process: Prints every row as a table and then the average score. If
#   the history is empty, it shows a message.
# Output: None (prints on the screen).
def show_history(history):
    print("\n-------------------------")
    print("      GAME HISTORY")
    print("-------------------------")

    if len(history) == 0:
        print("No games played yet.")
        return

    print_table_header()

    for row in history:
        print_history_row(row)

    average = calculate_average_score(history)
    print("\nAverage score per level:", f"{average:.1f}", "points")


# Functionality: Shows the 5 best results.
# Input: history (matrix with the saved results).
# Process: Sorts the history from the highest to the lowest score with
#   sorted() and prints the first 5 rows with their position. If the
#   history is empty, it shows a message.
# Output: None (prints on the screen).
def show_ranking(history):
    print("\n-------------------------")
    print("      TOP 5 RANKING")
    print("-------------------------")

    if len(history) == 0:
        print("No games played yet.")
        return

    # https://docs.python.org/3/library/functions.html#sorted
    ranking = sorted(history, key=get_score, reverse=True)

    print_table_header()

    for position, row in enumerate(ranking[:5], start=1):
        print(str(position) + ".", end=" ")
        print_history_row(row)


# GAME FLOW
# Functionality: Runs a complete game (one player, up to three levels).
# Input: all_levels (list of matrices) and history (matrix of results).
# Process: Asks for the player's name and plays the levels in order. After
#   each level it shows the results, adds a row to the history and saves
#   it in the file. If the player passes, it asks whether to continue.
#   The game ends when the player fails, stops or finishes all levels.
# Output: None (the history is updated and the total score is printed).
def play_game(all_levels, history):
    player_name = read_player_name()
    print("\nGood luck,", player_name + "!")

    total_score = 0
    level_index = 0
    keep_playing = True

    while keep_playing and level_index < len(all_levels):
        level_name = LEVEL_NAMES[level_index]

        correct_answers, score, total = play_level(
            level_name, all_levels[level_index])
        total_score = total_score + score

        passed = show_results(level_name, correct_answers, score, total)

        # datetime.strftime formats the date as text (see README for link)
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        percentage = int(calculate_percentage(correct_answers, total))
        result = "PASSED" if passed else "FAILED"

        row = [date, player_name, level_name, str(correct_answers),
               str(score), str(percentage), result]
        history.append(row)
        save_result(row)

        if not passed:
            keep_playing = False
        elif level_index == len(all_levels) - 1:
            print("\nCONGRATULATIONS, " + player_name.upper() + "!")
            print("You completed all the levels!")
        else:
            keep_playing = read_yes_no(
                "\nContinue to the next level? (Y/N): ")

        level_index = level_index + 1

    print("\nTotal score of this game:", total_score, "points")


# Functionality: Main program of the game.
# Input: None (the options are typed by the player).
# Process: Loads the question files and the saved history. Then it shows
#   the menu again and again (while True) until the player chooses Exit:
#   1 plays, 2 shows the instructions, 3 the history, 4 the ranking.
# Output: None (the program closes when the player chooses Exit).
def main():
    all_levels = load_all_levels()

    if len(all_levels) == 0:
        print("The question files could not be loaded. Closing the game.")
        return

    history = load_history()

    while True:
        show_menu()
        option = read_menu_option(1, 5)

        if option == 1:
            play_game(all_levels, history)
        elif option == 2:
            show_instructions()
        elif option == 3:
            show_history(history)
        elif option == 4:
            show_ranking(history)
        elif option == 5:
            print("\nThanks for playing U know enough?")
            break


if __name__ == "__main__":
    main()
