import os
import logging
from logging.handlers import RotatingFileHandler
from openai import OpenAI
import random
from flask_babel import _

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY is not set. Some features may not work.")
    openai_client = None
else:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Set up logging
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'openai_api.log')
handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger('openai_api')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

problem_counter = 0

def generate_math_problem(difficulty):
    global problem_counter
    problem_counter += 1

    if problem_counter % 4 < 2:
        # Generate story-based problem using OpenAI API
        problem = generate_story_problem_with_openai(difficulty)
    else:
        # Generate simple arithmetic problem
        problem = generate_simple_arithmetic_problem(difficulty)

    return problem

def generate_story_problem_with_openai(difficulty):
    logger.info(f"Generating story-based math problem with difficulty: {difficulty}")
    if not openai_client:
        logger.warning("API key not set. Using placeholder problem.")
        return {
            'question': f"Pregunta de ejemplo (dificultad: {difficulty})",
            'answer': "42",
            'explanation': "La clave API no está configurada. Esto es un marcador de posición."
        }

    prompt = f"Generate a math problem in Spanish for children with difficulty level {difficulty}. The problem should be a short story involving two arithmetic operations, similar to this example: 'Si María tiene 5 manzanas y su mamá le da 2 manzanas más, ¿cuántas manzanas tiene María ahora?' Include the question in Spanish, answer, and a brief explanation in Spanish. Format the response as follows:\nPregunta: [question]\nRespuesta: [answer]\nExplicación: [explanation]"
    
    try:
        logger.info(f"Sending request to OpenAI API. Prompt: {prompt}")
        completion = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        
        content = completion.choices[0].message.content
        logger.info(f"Received response from OpenAI API: {content}")

        if not content:
            raise ValueError("OpenAI returned an empty response.")
        
        # Parse the response and extract question, answer, and explanation
        lines = content.split('\n')
        question = next((line.split(':', 1)[1].strip() for line in lines if line.lower().startswith('pregunta:')), '')
        answer = next((line.split(':', 1)[1].strip() for line in lines if line.lower().startswith('respuesta:')), '')
        explanation = '\n'.join(line.split(':', 1)[1].strip() for line in lines if line.lower().startswith('explicación:'))

        # Extract only the number from the answer
        answer = ''.join(filter(str.isdigit, answer))
        
        logger.debug(f"Parsed response - Question: {question}, Answer: {answer}, Explanation: {explanation}")
        
        return {
            'question': question,
            'answer': answer,
            'explanation': explanation
        }
    except Exception as e:
        logger.error(f"Error generating story-based math problem: {str(e)}", exc_info=True)
        return {
            'question': f"Error al generar la pregunta (dificultad: {difficulty})",
            'answer': "0",
            'explanation': "Ocurrió un error al generar el problema."
        }

def generate_simple_arithmetic_problem(difficulty):
    logger.info(f"Generating simple arithmetic problem with difficulty: {difficulty}")
    
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
        question = f"{num1} + {num2} = ?"
        explanation = _("Great job! When we add %(num1)s and %(num2)s together, we get %(answer)s. Keep up the good work!") % {'num1': num1, 'num2': num2, 'answer': answer}
    elif operator == 'minus':
        num1, num2 = max(num1, num2), min(num1, num2)
        answer = num1 - num2
        question = f"{num1} - {num2} = ?"
        explanation = _("Awesome! When we take away %(num2)s from %(num1)s, we're left with %(answer)s. You're doing great!") % {'num1': num1, 'num2': num2, 'answer': answer}
    elif operator == 'times':
        answer = num1 * num2
        question = f"{num1} × {num2} = ?"
        explanation = _("Fantastic! When we multiply %(num1)s by %(num2)s, we get %(answer)s. You're becoming a math superstar!") % {'num1': num1, 'num2': num2, 'answer': answer}
    else:  # division
        answer = random.randint(1, 10)
        num1 = num2 * answer
        question = f"{num1} ÷ {num2} = ?"
        explanation = _("Amazing! When we split %(num1)s into %(num2)s equal groups, we get %(answer)s in each group. You're really good at this!") % {'num1': num1, 'num2': num2, 'answer': answer}

    return {
        'question': question,
        'answer': str(answer),
        'explanation': explanation
    }
