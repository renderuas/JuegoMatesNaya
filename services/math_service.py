import random

def generate_math_problem(difficulty):
    if difficulty == 1:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operator = random.choice(['plus', 'minus'])
    elif difficulty == 2:
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        operator = random.choice(['plus', 'minus', 'times'])
    else:
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
        operator = random.choice(['plus', 'minus', 'times', 'divided by'])

    if operator == 'plus':
        answer = num1 + num2
        question = f"What is {num1} plus {num2}?"
    elif operator == 'minus':
        answer = num1 - num2
        question = f"What is {num1} minus {num2}?"
    elif operator == 'times':
        answer = num1 * num2
        question = f"What is {num1} times {num2}?"
    else:
        num1 = num1 * num2  # Ensure division results in a whole number
        answer = num2
        question = f"What is {num1} divided by {num2}?"

    return {
        'question': question,
        'answer': str(answer),
        'explanation': get_explanation(num1, num2, operator, answer)
    }

def get_explanation(num1, num2, operator, answer):
    if operator == 'plus':
        return f"Great job! When we add {num1} and {num2} together, we get {answer}. Keep up the good work!"
    elif operator == 'minus':
        return f"Awesome! When we take away {num2} from {num1}, we're left with {answer}. You're doing great!"
    elif operator == 'times':
        return f"Fantastic! When we multiply {num1} by {num2}, we get {answer}. You're becoming a math superstar!"
    else:
        return f"Amazing! When we split {num1} into {num2} equal groups, we get {answer} in each group. You're really good at this!"
