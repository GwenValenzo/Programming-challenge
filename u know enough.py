"""U KNOW ENOUGH? - A quiz game with three levels."""

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
# Opens one question file and reads it line by line, splits each line by "|" and removes extra spaces from every part.
# Returns the matrix of questions (a list of lists).
def load_questions(filename):
    """Read a question file and return a matrix of questions.

    Each valid line has 5 parts separated by "|":
    question, correct answer, wrong 1, wrong 2, wrong 3.
    Lines that do not have 5 parts (titles, blank lines) are skipped.
    """
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


# Calls load_questions() once for each level file (easy, medium, hard).
# Returns a list with the 3 matrices of questions.
# If any file is missing or empty, returns an empty list.
def load_all_levels():
    """Load the question file of every level.

    Returns a list of matrices (one per level), or an empty list
    if any of the files is missing or has no questions.
    """
    all_levels = []

    for filename in LEVEL_FILES:
        questions = load_questions(filename)
        if len(questions) == 0:
            return []
        all_levels.append(questions)

    return all_levels


# Reads history.txt ,if it exists, and builds a matrix with the old results.
# Skips damaged lines
# If the file does not exist, returns an empty history.
def load_history():
    """Read the saved results from the history file into a matrix.

    Each row = [date, player, level, correct, score, percentage, result]
    """
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


# Joins one result row with "|" and adds it at the end of history.txt.
# Mode "a" (append) keeps the previous results.
def save_result(row):
    """Add one result row at the end of the history file."""
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(SEPARATOR.join(row) + "\n")


# MENU AND INSTRUCTIONS

# Prints the main menu options on the screen.
def show_menu():
    """Display the main menu."""
    print("\n-------------------------")
    print("      U KNOW ENOUGH?")
    print("-------------------------")
    print("1. Play")
    print("2. Instructions")
    print("3. Game history")
    print("4. Top 5 ranking")
    print("5. Exit")


# Prints the rules: levels, points, streak bonus and the passing score.
def show_instructions():
    """Display the rules of the game."""
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

# Asks for a menu option and repeats the question until the player, types a whole number between minimum and maximum.
# Returns the option as an integer.
def read_menu_option(minimum, maximum):
    """Ask for a whole number between minimum and maximum."""
    option = input("Select an option: ").strip()

    while (not option.isdigit() or int(option) < minimum
           or int(option) > maximum):
        print("Invalid option. Please enter a number from",
              minimum, "to", str(maximum) + ".")
        option = input("Select an option: ").strip()

    return int(option)


# Asks for the player's name and repeats until it has 2 to 15 characters, and only letters/spaces.
# Returns the name with the first letter of each word in capitals.
def read_player_name():
    """Ask for a name with only letters and spaces (2 to 15 characters)."""
    name = input("\nEnter your name: ").strip()

    while (len(name) < 2 or len(name) > 15
           or not name.replace(" ", "").isalpha()):
        print("Invalid name. Use only letters (2 to 15 characters).")
        name = input("Enter your name: ").strip()

    return name.title()


# Shows a message and repeats until the player types Y or N.
# Returns True if the player typed Y, False if N.
def read_yes_no(message):
    """Ask a yes/no question. Return True for Y and False for N."""
    answer = input(message).strip().upper()

    while answer != "Y" and answer != "N":
        print("Invalid answer. Please enter Y or N.")
        answer = input(message).strip().upper()

    return answer == "Y"


# QUESTIONS
# Prints the question number, the question and its options (A, B, C, D).
# Asks for an answer and repeats until it is exactly A, B, C or D.
# And returns the chosen letter in capitals.
def ask_question(number, total, question, options):
    """Show a question with its options and return a valid letter."""
    print("\nQuestion " + str(number) + "/" + str(total))
    print(question)

    for i in range(len(options)):
        print(LETTERS[i] + ")", options[i])

    answer = input("Your answer: ").strip().upper()

    while len(answer) != 1 or answer not in LETTERS:
        print("Invalid answer.")
        answer = input("Please enter A, B, C or D: ").strip().upper()

    return answer


# Compares the player's letter with the correct letter.
# Prints "Correct!" or "Incorrect!" (showing the right answer).
# Returns True if the answer was correct, False if not.
def check_answer(player_answer, correct_letter, correct_text):
    """Compare the answer with the correct one. Return True if correct."""
    if player_answer == correct_letter:
        print("Correct!")
        return True

    print("Incorrect!")
    print("The correct answer was:", correct_letter + ")", correct_text)
    return False


# Divides the correct answers by the total questions and multiplies by 100.
# Returns the percentage.
def calculate_percentage(correct_answers, total_questions):
    """Return the percentage of correct answers."""
    return (correct_answers / total_questions) * 100


# Picks random questions from the level matrix (random.sample).
# For each question: shuffles the options, finds the correct letter, asks the question and checks the answer.
# Adds 10 points per correct answer, +5 bonus every 3 correct in a row, and resets the streak when the player fails.
# Returns the correct answers, the score and how many questions were asked.
def play_level(level_name, questions):
    """Play one level and return (correct answers, score, total asked).

    random.sample picks the questions of this game without repeating.
    enumerate gives the question number together with each question.
    Every STREAK_LENGTH correct answers in a row give a bonus.
    """
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
# Calculates incorrect answers and the percentage of the level.
# Prints correct/incorrect answers, score and percentage.
# If the player failed, shows how many correct answers were needed.
# Returns True if the player passed 60% or more, False if not.
def show_results(level_name, correct_answers, score, total_questions):
    """Display the results of a level. Return True if the player passed.

    math.ceil rounds up, so we can tell how many correct answers
    were needed to pass the level.
    """
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
# Takes one history row and returns its score as an integer.
def get_score(row):
    """Return the score of a history row as a number (sorting key)."""
    return int(row[4])


# Adds the score of every row in the history and divides by the number of rows.
# Returns the average score.
def calculate_average_score(history):
    """Return the average score of all the rows in the history."""
    total = 0

    for row in history:
        total = total + get_score(row)

    return total / len(history)


# Prints one history row as a line of the table, with aligned columns.
def print_history_row(row):
    """Print one history row as a table line."""
    print(row[0].ljust(18) + row[1].ljust(16) + row[2].ljust(9)
          + row[3].ljust(9) + row[4].ljust(7)
          + (row[5] + "%").ljust(6) + row[6])


# Prints the column titles of the table and a separator line.
def print_table_header():
    """Print the header of the history table."""
    print("DATE".ljust(18) + "PLAYER".ljust(16) + "LEVEL".ljust(9)
          + "CORRECT".ljust(9) + "SCORE".ljust(7) + "%".ljust(6)
          + "RESULT")
    print("-" * 70)


# Prints all the saved results as a table, plus the average score.
# If there are no results yet, shows a message instead.
def show_history(history):
    """Display every saved result and the average score."""
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


# Sorts the history from the highest to the lowest score (sorted).
# Prints the 5 best results with their position (1 to 5).
# If there are no results yet, shows a message instead.
def show_ranking(history):
    """Display the 5 best results, sorted by score."""
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

# Asks for the player's name and plays the levels in order.
# After each level: shows the results, adds a row to the history matrix and saves it in history.txt.
# If the player passes, asks whether to continue to the next level.
# The game ends when the player fails, stops, or finishes all levels.
def play_game(all_levels, history):
    """Play the levels in order until the player fails or quits.

    After each level the result is added to the history matrix
    and saved in the history file.
    """
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


# Loads the question files and the saved history.
# Shows the menu again and again until the player chooses Exit.
# Option 1 plays, 2 shows instructions, 3 history, 4 ranking, 5 exits.
def main():
    """Load the data and show the main menu until the player exits."""
    all_levels = load_all_levels()

    if len(all_levels) == 0:
        print("The question files could not be loaded. Closing the game.")
        return

    history = load_history()
    option = 0

    while option != 5:
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


if __name__ == "__main__":
    main()
