import os
import logging
from logging.handlers import RotatingFileHandler
from openai import OpenAI

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
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def generate_math_problem(difficulty):
    if not openai_client:
        logger.warning("API key not set. Using placeholder problem.")
        return {
            'question': f"Sample question (difficulty: {difficulty})",
            'answer': "Sample answer",
            'explanation': "API key not set. This is a placeholder."
        }

    prompt = f"Generate a math problem for children with difficulty level {difficulty}. Include the question, answer, and a brief explanation."
    
    try:
        logger.info(f"Sending request to OpenAI API. Prompt: {prompt}")
        completion = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        
        content = completion.choices[0].message.content
        logger.info(f"Received response from OpenAI API: {content}")

        if not content:
            raise ValueError("OpenAI returned an empty response.")
        
        # Parse the response and extract question, answer, and explanation
        lines = content.split('\n')
        question = lines[0].strip()
        answer = lines[1].strip().split(': ')[-1]
        explanation = '\n'.join(lines[2:]).strip()
        
        return {
            'question': question,
            'answer': answer,
            'explanation': explanation
        }
    except Exception as e:
        logger.error(f"Error generating math problem: {str(e)}")
        return {
            'question': f"Error generating question (difficulty: {difficulty})",
            'answer': "N/A",
            'explanation': "An error occurred while generating the problem."
        }
