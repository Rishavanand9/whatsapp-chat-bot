import replicate
import os
from config import REPLICATE_API_TOKEN

# Assuming you've set your Replicate API key in your environment variables
replicate.api_token = os.getenv(REPLICATE_API_TOKEN)

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
print("REPLICATE_API_TOKEN:", REPLICATE_API_TOKEN)

# if REPLICATE_API_TOKEN is None:
#     raise ValueError(
#         "Replicate API token is not set in environment variables.")

# Define your JSON template as a string to improve readability in the prompt
JSON_SYNTAX = '''{
    "transaction_id": "Read transaction ID from the message it may be bank ref id, transaction id, reference no or similar texts",
    "sender_name": "Read sender name",
    "receiver_name": "Read receiver name",
    "sender_number": "Read sender number",
    "receiver_number": "Read receiver number",
    "timestamp": "Read timestamp from the text Format(YYYY-MM-DD HH:MM:SS)",
    "transaction_amount": "Read Transaction Amount from the text"
}'''


def generate_json_from_text(text):
    prompt = f"""Please read the below text carefully and generate a JSON object based on the following structure oNLY RETURBN json and do not return any irrelevant text:
    {JSON_SYNTAX}
    Based on this text:
    {text}
    """

    print(prompt)

    # Replace the model with the name of the model you want to use
    model = "meta/llama-2-13b-chat"

    # Run the model and get the prediction
    prediction = replicate.run(model, input={"prompt": prompt,
                                             "max_new_tokens": 500,
                                             "min_new_tokens": -1,
                                             "temperature": 0.5,
                                             "top_p": 0.01,
                                             "repetition_penalty": 1.15,
                                             "top_k": 50, })
    prediction_string = ''.join(prediction[0:])
    lines = prediction_string.split('\n')
    final_json = '\n'.join(lines[1:])


    print("*"*50)
    # Print the prediction
    print(final_json)
    print("*"*50)
    return final_json

# import openai
# from config import OPEN_AI_API_KEY

# # Setting the API key for authentication
# openai.api_key = OPEN_AI_API_KEY

# # Replace MODEL_NAME_HERE with the model you have access to, e.g., "text-davinci-003" or "gpt-3.5-turbo"
# MODEL_NAME = "gpt-3.5-turbo-16k-0613"

# JSON_SYNTAX = {
#     "transaction_id": "Read transaction ID from the message it may be bank ref id, transaction id, reference no or similar texts",
#     "sender_name": "Read sender name",
#     "receiver_name": "Read receiver name",
#     "sender_number": "Read sender number",
#     "receiver_number": "Read receiver number",
#     "timestamp": "Read timestamp from the text Format(YYYY-MM-DD HH:MM:SS)",
#     "transaction_amount": "Read Transaction Amount from the text"
# }

# def generate_json_from_text(text):
#     prompt = f"""I want to read the below text carefully and convert it into the following JSON format:

#     Syntax::
#       {JSON_SYNTAX}

#     Replace all values in the above syntax with the observed value in the given text

#     "{text}"
# """
#     print("-----------------Model List--------------------")
#     try:
#       models = openai.Model.list()
#       for model in models.data:
#         print(model.id)
#     except Exception as e:
#       print(f"Error fetching models: {e}")
#     print("-------------------------------------")
#     # return None

#     response = openai.ChatCompletion.create(
#         model=MODEL_NAME,
#         messages=[{"role": "user", "content": prompt}],
#     )
    
#     return response.choices[0].message['content'] if response.choices else None



# # from transformers import AutoModelForCausalLM, AutoTokenizer
# # # import torch

# # # Initialize the tokenizer and model from the Transformers library
# # MODEL_NAME = "llava_llama"  # Replace with the actual model name
# # tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# # model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# # def generate_json_from_text(text):
# #     # Define your JSON structure and the prompt as before
# #     JSON_SYNTAX = {
# #         "transaction_id": "Read transaction ID from the message it may be bank ref id, transaction id, reference no or similar texts",
# #         "sender_name": "Read sender name",
# #         "receiver_name": "Read receiver name",
# #         "sender_number": "Read sender number",
# #         "receiver_number": "Read receiver number",
# #         "timestamp": "Read timestamp from the text Format(YYYY-MM-DD HH:MM:SS)",
# #         "transaction_amount": "Read Transaction Amount from the text"
# #     }

# #     prompt = f"""I want to read the below text carefully and convert it into the following JSON format:

# #     Syntax::
# #       {JSON_SYNTAX}

# #     Replace all values in the above syntax with the observed value in the given text

# #     "{text}"
# # """

# #     # Tokenize the prompt
# #     input_ids = tokenizer.encode(prompt, return_tensors='pt')

# #     # Generate a response
# #     output = model.generate(input_ids, max_length=512, num_return_sequences=1)

# #     # Decode the generated tokens to text
# #     generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    
# #     return generated_text

# # # # Example use
# # # text_example = "The transaction was completed on 2023-03-10 at 2:45 PM. The sender, John Doe, sent $100 to Jane Doe. The transaction ID is ABC123."
# # # generated_json = generate_json_from_text(text_example)
# # # print(generated_json)

