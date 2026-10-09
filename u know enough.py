# U KNOW ENOUGH?

def show_menu():
    print("\n-------------------------")
    print("      U KNOW ENOUGH?")
    print("-------------------------")
    print("1. Play")
    print("2. Instructions")
    print("3. Exit")

def show_instructions():
    print("\n-------------------------")
    print("      INSTRUCTIONS")
    print("-------------------------")
    print("You will answer 10 questions.")
    print("Each question has four options: A, B, C or D.")
    print("Each correct answer gives you 10 points.")
    print("You need at least 60% to pass the level.")

def ask_question(question, option_a, option_b, option_c, option_d):

    print("\n" + question)
    print("A)", option_a)
    print("B)", option_b)
    print("C)", option_c)
    print("D)", option_d)

    answer = input("Your answer: ").upper()

    while answer != "A" and answer != "B" and answer != "C" and answer != "D":
        print("Invalid answer.")
        answer = input("Please enter A, B, C or D: ").upper()

    return answer

def check_answer(player_answer, correct_answer):
    
    if player_answer==correct_answer:
        print("Correct")
        return True
    else:
        print("Incorrect!")
        print("The correct answer was:", correct_answer)
        return False



def calculate_percentage(correct_answers, total_questions):

    percentage = (correct_answers / total_questions) * 100

    return percentage

def play_easy_level():

    correct_answers = 0
    score = 0

    print("\n-------------------------")
    print("       EASY LEVEL")
    print("-------------------------")


    # Question 1
    answer = ask_question(
        "What is the capital of France?",
        "Madrid",
        "Paris",
        "Rome",
        "Berlin"
    )

    if check_answer(answer, "B"):
        correct_answers = correct_answers + 1
        score = score + 10


    # Question 2
    answer = ask_question(
        "What planet is known as the Red Planet?",
        "Venus",
        "Mars",
        "Jupiter",
        "Saturn"
    )

    if check_answer(answer, "B"):
        correct_answers = correct_answers + 1
        score = score + 10


    # Question 3
    answer = ask_question(
        "How many continents are there?",
        "5",
        "6",
        "7",
        "8"
    )

    if check_answer(answer, "C"):
        correct_answers = correct_answers + 1
        score = score + 10


    # Question 4
    answer = ask_question(
        "Which animal is the largest mammal?",
        "Elephant",
        "Blue whale",
        "Giraffe",
        "Shark"
    )

    if check_answer(answer, "B"):
        correct_answers = correct_answers + 1
        score = score + 10


    # Question 5
    answer = ask_question(
        "What is 8 x 7?",
        "48",
        "54",
        "56",
        "64"
    )

    if check_answer(answer, "C"):
        correct_answers = correct_answers + 1
        score = score + 10


    # Question 6
    answer = ask_question(
        "Which ocean is the largest?",
        "Atlantic Ocean",
        "Indian Ocean",
        "Pacific Ocean",
        "Arctic Ocean"
    )

    if check_answer(answer, "C"):
        correct_answers = correct_answers + 1
        score = score + 10


    # Question 7
    answer = ask_question(
        "Which country is famous for the pyramids of Giza?",
        "Mexico",
        "Egypt",
        "India",
        "Greece"
    )

    if check_answer(answer, "B"):
        correct_answers = correct_answers + 1
        score = score + 10


    # Question 8
    answer = ask_question(
        "How many days are there in a normal year?",
        "360",
        "364",
        "365",
        "366"
    )

    if check_answer(answer, "C"):
        correct_answers = correct_answers + 1
        score = score + 10


    # Question 9
    answer = ask_question(
        "Which gas do humans need to breathe?",
        "Carbon dioxide",
        "Oxygen",
        "Hydrogen",
        "Nitrogen"
    )

    if check_answer(answer, "B"):
        correct_answers = correct_answers + 1
        score = score + 10


    # Question 10
    answer = ask_question(
        "Which programming language are we using for this project?",
        "Java",
        "C++",
        "Python",
        "Swift"
    )

    if check_answer(answer, "C"):
        correct_answers = correct_answers + 1
        score = score + 10


    return correct_answers, score


# Algorithm:
# Calculate incorrect answers.
# Calculate the player's percentage.
# Display correct answers, incorrect answers,
# total score and percentage.
# Determine if the player passed the level.
def show_results(correct_answers, score):

    total_questions = 10

    incorrect_answers = total_questions - correct_answers

    percentage = calculate_percentage(
        correct_answers,
        total_questions
    )

    print("\n-------------------------")
    print("        RESULTS")
    print("-------------------------")

    print("Correct answers:", correct_answers)
    print("Incorrect answers:", incorrect_answers)
    print("Score:", score, "points")
    print("Percentage:", percentage, "%")

    if percentage >= 60:
        print("You passed the Easy Level!")

    else:
        print("You did not pass the Easy Level.")
        print("You need at least 60% to pass.")


# Algorithm:
# Show the main menu repeatedly.
# Ask the player to select an option.
# If the player selects Play, start the Easy Level.
# If the player selects Instructions, show the rules.
# If the player selects Exit, finish the program.
def main():

    option = 0

    while option != 3:

        show_menu()

        option = int(input("Select an option: "))

        if option == 1:

            correct_answers, score = play_easy_level()

            show_results(correct_answers, score)

        elif option == 2:

            show_instructions()

        elif option == 3:

            print("\nThanks for playing U know enough?")

        else:

            print("\nInvalid option. Please select 1, 2 or 3.")


main()
