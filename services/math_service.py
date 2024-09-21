from flask_babel import _
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
        question = _("What is %(num1)s plus %(num2)s?") % {'num1': num1, 'num2': num2}
    elif operator == 'minus':
        # Ensure the result is positive
        num1, num2 = max(num1, num2), min(num1, num2)
        answer = num1 - num2
        question = _("What is %(num1)s minus %(num2)s?") % {'num1': num1, 'num2': num2}
    elif operator == 'times':
        answer = num1 * num2
        question = _("What is %(num1)s times %(num2)s?") % {'num1': num1, 'num2': num2}
    else:  # division
        # Ensure the division results in a whole number
        answer = random.randint(1, 10)
        num1 = num2 * answer
        question = _("What is %(num1)s divided by %(num2)s?") % {'num1': num1, 'num2': num2}

    return {
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
