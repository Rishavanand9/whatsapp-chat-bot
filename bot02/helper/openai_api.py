import os
import openai
from dotenv import load_dotenv
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def openai_text_completion(prompt: str) -> dict:
    '''
    Call Openai API for text completion

    Parameters:
        - prompt: user query (str)

    Returns:
        - dict
    '''
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Make sure to use the correct model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f'Human: {prompt}'},
            ],
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=['Human:', 'AI:']
        )
        return {
            'status': 1,
            'response': response['choices'][0]['text']
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'status': 0,
            'response': ''
        }

# Example usage:
prompt_text = "Can you help me with..."
result = openai_text_completion(prompt_text)
print(result)
