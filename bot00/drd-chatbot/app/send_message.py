import json
import re
import numpy as np
import requests
from app.chatbot_logic import generate_json_from_text
from app.parse_text_to_json import parse_text
from config import DATABASE_URL, WASSI_CONTENT_HEADER, WASSI_API_URL, WASSI_SEND_MESSAGE_URL
import pytesseract
import cv2
import psycopg2
import psycopg2.extras
# import matplotlib.pyplot as plt


def get_image_data(image_link):
    url = WASSI_API_URL + image_link
    try:
        response = requests.get(url, headers=WASSI_CONTENT_HEADER)
        response.raise_for_status()  # Check for HTTP error status
        return response.content  # Return binary content
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    

def detect_amount_in_image(image_data, message):
    try:
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # # Use matplotlib to display the image
        # plt.figure(figsize=(10, 6))  # Optional: Adjust figure size
        # plt.imshow(img, cmap='gray')  # cmap='gray' to display grayscale images
        # plt.title('Adaptive Threshold')
        # plt.axis('off')  # Hide axes ticks
        # plt.show()

        text = pytesseract.image_to_string(img, lang='eng')
        print("."*250)
        print('Detected text: ----------------------------->', text)
        print("."*250)
        thanks_msg = "Thanks !! Your Payment has been recieved Successfully --------->>>>>><<<<<<<------"
        json_text = generate_json_from_text(text)


        print("*"*250)
        print("--------------------------------  FINAL OBJECT  --------------------------------")
        print(json_text)
        print("."*250)      

        return thanks_msg + json_text

    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def handle_message(message):
    message_type = message['type']
    sender_name = message.get('chat', {}).get('contact', {}).get('displayName', '')

    if message_type == 'text':
        text_message = message['body']
        response_message = f"Hello {sender_name}, you said: '{text_message}'"
    elif message_type == 'image':
        image_link = message['media']['links']['download']
        image_data = get_image_data(image_link)
        if image_data:
            response_message = detect_amount_in_image(image_data, message)
        else:
            response_message = "Failed to process the image."
    else:
        response_message = f"Hello {sender_name}, your message type '{message_type}' is not supported."

    print("."*250)
    print(response_message)
    print("."*250)
    return response_message


def send_whatsapp_message(recipient_id, message):
    response_message = handle_message(message['data'])
    return  {"status": "success", "message": "Message Saved"}

    #payload = {
    #    "phone": recipient_id,
    #    "message": response_message
    #}
    

    #try:
        #response = requests.post(WASSI_SEND_MESSAGE_URL, json=payload, headers=WASSI_CONTENT_HEADER)
        #if response.ok:
        #    return {"status": "success", "message": "Message sent"}
        #else:
        #    return {"status": "error", "message": "Failed to send message"}
    #except requests.exceptions.RequestException as e:
       # return {"status": "error", "message": f"An exception occurred: {e}"}
