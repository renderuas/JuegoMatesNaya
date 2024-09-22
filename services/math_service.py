from flask_babel import _
import random

problem_counter = 0

def generate_math_problem(difficulty):
    global problem_counter
    problem_counter += 1

    if difficulty == 1:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operator = random.choice(['plus', 'minus', 'times'])
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
        text_question = _("What is %(num1)s plus %(num2)s?") % {'num1': num1, 'num2': num2}
        numerical_question = f"{num1} + {num2} = ?"
    elif operator == 'minus':
        # Ensure the result is positive
        num1, num2 = max(num1, num2), min(num1, num2)
        answer = num1 - num2
        text_question = _("What is %(num1)s minus %(num2)s?") % {'num1': num1, 'num2': num2}
        numerical_question = f"{num1} - {num2} = ?"
    elif operator == 'times':
        answer = num1 * num2
        text_question = _("What is %(num1)s times %(num2)s?") % {'num1': num1, 'num2': num2}
        numerical_question = f"{num1} × {num2} = ?"
    else:  # division
        # Ensure the division results in a whole number
        answer = random.randint(1, 10)
        num1 = num2 * answer
        text_question = _("What is %(num1)s divided by %(num2)s?") % {'num1': num1, 'num2': num2}
        numerical_question = f"{num1} ÷ {num2} = ?"

    # Alternate between text and numerical questions every two problems
    if problem_counter % 4 < 2:
        question = text_question
    else:
        question = numerical_question

    return {
        'text_question': text_question,
        'numerical_question': numerical_question,
        'question': question,
        'answer': str(answer),
        'explanation': get_explanation(num1, num2, operator, answer)
    }

def get_explanation(num1, num2, operator, answer):
    if operator == 'plus':
        return _("Great job! When we add %(num1)s and %(num2)s together, we get %(answer)s. Keep up the good work!") % {'num1': num1, 'num2': num2, 'answer': answer}
    elif operator == 'minus':
        return _("Awesome! When we take away %(num2)s from %(num1)s, we're left with %(answer)s. You're doing great!") % {'num1': num1, 'num2': num2, 'answer': answer}
    elif operator == 'times':
        return _("Fantastic! When we multiply %(num1)s by %(num2)s, we get %(answer)s. You're becoming a math superstar!") % {'num1': num1, 'num2': num2, 'answer': answer}
    else:
        return _("Amazing! When we split %(num1)s into %(num2)s equal groups, we get %(answer)s in each group. You're really good at this!") % {'num1': num1, 'num2': num2, 'answer': answer}
