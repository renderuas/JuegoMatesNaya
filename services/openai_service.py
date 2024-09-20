import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY is not set. Some features may not work.")
    openai_client = None
else:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

def generate_math_problem(difficulty):
    if not openai_client:
        return {
            'question': f"Sample question (difficulty: {difficulty})",
            'answer': "Sample answer",
            'explanation': "API key not set. This is a placeholder."
        }

    prompt = f"Generate a math problem for children with difficulty level {difficulty}. Include the question, answer, and a brief explanation."
    
    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        
        content = completion.choices[0].message.content
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
        print(f"Error generating math problem: {str(e)}")
        return {
            'question': f"Error generating question (difficulty: {difficulty})",
            'answer': "N/A",
            'explanation': "An error occurred while generating the problem."
        }
