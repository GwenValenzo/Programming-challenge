# U KNOW ENOUGH?

import random

LETTERS = "ABCD"
PASS_PERCENTAGE = 60
POINTS_PER_QUESTION = 10
TOTAL_QUESTIONS = 10

LEVEL_NAMES = ["EASY", "MEDIUM", "HARD"]

easy_questions = []
with open ("easyquestions.txt", "r") as file:
    for linea in file:
        linea = linea.strip()
        if linea == "" or "," not in linea:
            continue                      # skip the title and blank lines
        parts = linea.split(",")
        row = []
        for part in parts:
            row.append(part.strip())
        easy_questions.append(row)

    

medium_questions = []
with open ("mediumquestions.txt", "r") as file:
    for linea in file:
        linea = linea.strip()
        if linea == "" or "," not in linea:
            continue                      # skip the title and blank lines
        parts = linea.split(",")
        row = []
        for part in parts:
            row.append(part.strip())
        medium_questions.append(row)


hard_questions = []
with open ("hardquestions.txt", "r") as file:
    for linea in file:
        linea = linea.strip()
        if linea == "" or "," not in linea:
            continue                      # skip the title and blank lines
        parts = linea.split(",")
        row = []
        for part in parts:
            row.append(part.strip())
        hard_questions.append(row)

all_levels = [easy_questions, medium_questions, hard_questions]


def show_menu():
    print("\n-------------------------")
    print("      U KNOW ENOUGH?")
    print("-------------------------")
    print("1. Play")
    print("2. Instructions")
    print("3. Game history")
    print("4. Exit")


def show_instructions():
    print("\n-------------------------")
    print("      INSTRUCTIONS")
    print("-------------------------")
    print("There are", len(all_levels), "levels:", ", ".join(LEVEL_NAMES) + ".")
    print("Each level has", TOTAL_QUESTIONS, "random questions.")
    print("Each question has four options: A, B, C or D.")
    print("Each correct answer gives you", POINTS_PER_QUESTION, "points.")
    print("You need at least", str(PASS_PERCENTAGE) + "% to pass a level.")
    print("Pass a level to unlock the next one!")


def read_menu_option(minimum, maximum):

    option = input("Select an option: ").strip()

    while not option.isdigit() or int(option) < minimum or int(option) > maximum:
        print("Invalid option. Please enter a number from",
              minimum, "to", maximum + ".")
        option = input("Select an option: ").strip()

    return int(option)


def read_player_name():

    name = input("\nEnter your name: ").strip()

    while (len(name) < 2 or len(name) > 15
           or not name.replace(" ", "").isalpha()):
        print("Invalid name. Use only letters (2 to 15 characters).")
        name = input("Enter your name: ").strip()

    return name.title()


def read_yes_no(message):

    answer = input(message).strip().upper()

    while answer != "Y" and answer != "N":
        print("Invalid answer. Please enter Y or N.")
        answer = input(message).strip().upper()

    return answer == "Y"

def ask_question(number, question, options):

    print("\nQuestion " + str(number) + "/" + str(TOTAL_QUESTIONS))
    print(question)

    for i in range(len(options)):
        print(LETTERS[i] + ")", options[i])

    answer = input("Your answer: ").strip().upper()

    while len(answer) != 1 or answer not in LETTERS:
        print("Invalid answer.")
        answer = input("Please enter A, B, C or D: ").strip().upper()

    return answer


def check_answer(player_answer, correct_letter, correct_text):

    if player_answer == correct_letter:
        print("Correct!")
        return True
    else:
        print("Incorrect!")
        print("The correct answer was:", correct_letter + ")", correct_text)
        return False


def calculate_percentage(correct_answers, total_questions):

    percentage = (correct_answers / total_questions) * 100

    return percentage

def play_level(level_index):

    level_name = LEVEL_NAMES[level_index]
    questions = all_levels[level_index][:]   # copy, so the original is kept
    random.shuffle(questions)

    correct_answers = 0
    score = 0

    print("\n-------------------------")
    print("       " + level_name + " LEVEL")
    print("-------------------------")

    for i in range(len(questions)):

        row = questions[i]
        question = row[0]
        correct_text = row[1]

        options = row[1:]         
        random.shuffle(options)

        correct_letter = LETTERS[options.index(correct_text)]

        answer = ask_question(i + 1, question, options)

        if check_answer(answer, correct_letter, correct_text):
            correct_answers = correct_answers + 1
            score = score + POINTS_PER_QUESTION

    return correct_answers, score


def show_results(level_name, correct_answers, score):

    incorrect_answers = TOTAL_QUESTIONS - correct_answers

    percentage = calculate_percentage(correct_answers, TOTAL_QUESTIONS)

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
    else:
        print("You did not pass the", level_name.capitalize(), "Level.")
        print("You need at least", str(PASS_PERCENTAGE) + "% to pass.")
        return False


def show_history(history):

    print("\n-------------------------")
    print("      GAME HISTORY")
    print("-------------------------")

    if len(history) == 0:
        print("No games played yet.")
        return

    print("PLAYER".ljust(16) + "LEVEL".ljust(9) + "CORRECT".ljust(9)
          + "SCORE".ljust(7) + "%".ljust(6) + "RESULT")
    print("-" * 55)

    for row in history:
        print(str(row[0]).ljust(16)
              + str(row[1]).ljust(9)
              + str(row[2]).ljust(9)
              + str(row[3]).ljust(7)
              + (str(row[4]) + "%").ljust(6)
              + str(row[5]))


def play_game(history):

    player_name = read_player_name()
    print("\nGood luck,", player_name + "!")

    total_score = 0
    level_index = 0
    keep_playing = True

    while keep_playing and level_index < len(all_levels):

        correct_answers, score = play_level(level_index)
        total_score = total_score + score

        level_name = LEVEL_NAMES[level_index]
        passed = show_results(level_name, correct_answers, score)

        percentage = int(calculate_percentage(correct_answers, TOTAL_QUESTIONS))
        result = "PASSED" if passed else "FAILED"
        history.append([player_name, level_name, correct_answers,
                        score, percentage, result])

        if not passed:
            keep_playing = False
        elif level_index == len(all_levels) - 1:
            print("\nCONGRATULATIONS, " + player_name.upper() + "!")
            print("You completed all the levels!")
        else:
            keep_playing = read_yes_no("\nContinue to the next level? (Y/N): ")

        level_index = level_index + 1

    print("\nTotal score of this game:", total_score, "points")


def main():

    history = []    # matrix that grows as the player completes levels
    option = 0

    while option != 4:

        show_menu()

        option = read_menu_option(1, 4)

        if option == 1:
            play_game(history)

        elif option == 2:
            show_instructions()

        elif option == 3:
            show_history(history)

        elif option == 4:
            print("\nThanks for playing U know enough?")


main()
