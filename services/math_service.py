import random

def generate_math_problem(difficulty):
    if difficulty == 1:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operator = random.choice(['+', '-'])
    elif difficulty == 2:
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        operator = random.choice(['+', '-', '*'])
    else:
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
        operator = random.choice(['+', '-', '*', '/'])

    if operator == '+':
        answer = num1 + num2
        question = f"{num1} + {num2}"
    elif operator == '-':
        answer = num1 - num2
        question = f"{num1} - {num2}"
    elif operator == '*':
        answer = num1 * num2
        question = f"{num1} × {num2}"
    else:
        num1 = num1 * num2  # Ensure division results in a whole number
        answer = num2
        question = f"{num1} ÷ {num2}"

    return {
        'question': question,
        'answer': str(answer),
        'explanation': f"The answer is {answer}. {get_explanation(num1, num2, operator, answer)}"
    }

def get_explanation(num1, num2, operator, answer):
    if operator == '+':
        return f"We add {num1} and {num2} to get {answer}."
    elif operator == '-':
        return f"We subtract {num2} from {num1} to get {answer}."
    elif operator == '*':
        return f"We multiply {num1} by {num2} to get {answer}."
    else:
        return f"We divide {num1} by {num2} to get {answer}."
