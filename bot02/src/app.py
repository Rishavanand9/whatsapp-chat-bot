from flask import Flask, request
from dotenv import load_dotenv
from PIL import Image
import pytesseract
from helper.twilio_api import send_message
from helper.openai_api import openai_text_completion

app = Flask(__name__)
load_dotenv()

# Set the path to the Tesseract executable (change it to your path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/')
def home():
    return 'All is well...'

@app.route('/getInput', methods=['POST'])
def receive_message():
    try:
        # Extract incoming parameters from Twilio
        sender_id = request.form['From']
        
        # Check if the message contains media (image)
        if 'MediaUrl0' in request.form:
            media_url = request.form['MediaUrl0']
            if media_url:
                # Send Dummy response BEGIN
                send_message(sender_id,'PAYMENT RECIEVED')

            try:
                # Download the image
                image_path = download_image(media_url)

                import pdb;pdb.set_trace()
                
                # Process the image using OCR (Tesseract)
                extracted_text = ocr_image(image_path)
                
                # Example: Convert extracted text to JSON (replace this with your actual logic)
                json_data = convert_to_json(extracted_text)

                result = {
                    'status': 1,
                    'response': json_data
                }

                if result['status'] == 1:
                    send_message(sender_id, result['response'])
            except Exception as image_error:
                print(f"Error processing image: {str(image_error)}")
        else:
            # If it's a text message, process it using OpenAI API
            message = request.form['Body']
            try:
                # result = openai_text_completion(message)
                # if result['status'] == 1:
                send_message(sender_id, 'How may i help today ?')
            except Exception as text_error:
                print(f"Error processing text: {str(text_error)}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    return 'OK', 200

def download_image(image_url):
    # Implement the logic to download the image from the provided URL
    # Return the path to the downloaded image
    # Example: You can use the requests library to download the image
    # and save it to a local file, then return the path to that file
    pass

def ocr_image(image_path):
    # Use Tesseract OCR to extract text from the image
    # Return the extracted text
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

def convert_to_json(text):
    # Implement your logic to convert the extracted text to JSON
    # Replace this example logic with your actual conversion logic
    # Example: You might use a JSON library like json.loads
    # to convert a valid JSON-formatted string to a Python dictionary
    pass

if __name__ == '__main__':
    app.run(debug=True)
