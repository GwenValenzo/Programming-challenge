# U KNOW ENOUGH?

import random

LETTERS = "ABCD"
PASS_PERCENTAGE = 60
POINTS_PER_QUESTION = 10
TOTAL_QUESTIONS = 10

LEVEL_NAMES = ["EASY", "MEDIUM", "HARD"]

easy_questions = [
    ["What is the capital of France?", "Paris", "Madrid", "Rome", "Berlin"],
    ["What planet is known as the Red Planet?", "Mars", "Venus", "Jupiter", "Saturn"],
    ["How many continents are there?", "7", "5", "6", "8"],
    ["Which animal is the largest mammal?", "Blue whale", "Elephant", "Giraffe", "Shark"],
    ["What is 8 x 7?", "56", "48", "54", "64"],
    ["Which ocean is the largest?", "Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"],
    ["Which country is famous for the pyramids of Giza?", "Egypt", "Mexico", "India", "Greece"],
    ["How many days are there in a normal year?", "365", "360", "364", "366"],
    ["Which gas do humans need to breathe?", "Oxygen", "Carbon dioxide", "Hydrogen", "Nitrogen"],
    ["Which programming language are we using for this project?", "Python", "Java", "C++", "Swift"],
]

medium_questions = [
    ["What is the chemical symbol for gold?", "Au", "Ag", "Gd", "Go"],
    ["Who painted the Mona Lisa?", "Leonardo da Vinci", "Michelangelo", "Raphael", "Picasso"],
    ["Which is the largest country by area?", "Russia", "Canada", "China", "United States"],
    ["How many bones does an adult human have?", "206", "106", "256", "306"],
    ["What is the square root of 144?", "12", "10", "14", "16"],
    ["What is the capital of Japan?", "Tokyo", "Seoul", "Beijing", "Bangkok"],
    ["What is the hardest natural substance?", "Diamond", "Gold", "Iron", "Quartz"],
    ["In what year did World War II end?", "1945", "1918", "1939", "1950"],
    ["Which language has the most native speakers?", "Mandarin Chinese", "English", "Spanish", "Hindi"],
    ["Which Python keyword is used to define a function?", "def", "func", "define", "function"],
]

hard_questions = [
    ["What is the capital of Australia?", "Canberra", "Sydney", "Melbourne", "Perth"],
    ["What is the approximate speed of light?", "300,000 km/s", "150,000 km/s", "450,000 km/s", "1,000,000 km/s"],
    ["Who wrote Don Quixote?", "Miguel de Cervantes", "Lope de Vega", "Jorge Luis Borges", "Gabriel Garcia Marquez"],
    ["What is the smallest prime number?", "2", "0", "1", "3"],
    ["What is the atomic number of carbon?", "6", "4", "8", "12"],
    ["In what year did the Berlin Wall fall?", "1989", "1987", "1991", "1993"],
    ["What is the binary number 1010 in decimal?", "10", "8", "12", "14"],
    ["Which Python data type is immutable?", "tuple", "list", "dict", "set"],
    ["Who developed the theory of general relativity?", "Albert Einstein", "Isaac Newton", "Galileo Galilei", "Niels Bohr"],
    ["Which organ produces insulin?", "Pancreas", "Liver", "Kidney", "Stomach"],
]

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
