def menu():
    print("\n--- U KNOW ENOUGH? ---")
    print("1. Play")
    print("2. Instructions")
    print("3. Exit")
def instructions():
    print("\nINSTRUCTIONS")
    print("Answer the questions by choosing A, B, C or D.")
    print("Each correct answer gives you one point.")
    print("You need at least 3 correct answers to pass the level.")
    
def ask_question(question, option_a, option_b, option_c, option_d):
    print("\n", question)
    print("A)", option_a)
    print("B)", option_b)
    print("C)", option_c)
    print("D)", option_d)

    answer = input("Your answer: ")

    return answer
answer = ask_question(
    "What is the capital of France?",
    "Madrid",
    "Paris",
    "Rome",
    "Berlin")
def check_answer(answer, correct_answer):

    if answer.upper() == correct_answer:
        print("Correct!")
        return True

    else:
        print("Incorrect!")
        print("The correct answer was:", correct_answer)
        return False
    
check_answer(answer, "B")
