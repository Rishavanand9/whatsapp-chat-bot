from flask import Flask, Blueprint, request, jsonify
from app.send_message import send_whatsapp_message
import json

print('main', __name__)
main = Blueprint('main', __name__)


@main.route('/webhook', methods=['POST'])
def webhook():
    try:
        msg = request.json  # Assuming each request contains a single message

        if not isinstance(msg, dict) or 'event' not in msg or 'data' not in msg:
            return jsonify({"error": "Invalid message format"}), 200

        data = msg['data']
        # with open("webhook_logs.txt", "a") as logfile:
        #     logfile.write(json.dumps(data) + "\n")
        event_type = msg['event']
        if event_type != "message:in:new":
            return jsonify({"error": "Unsupported event type"}), 200

        # Extract necessary fields
        phone = data.get('fromNumber')

        print("."*250)
        print("-------------------------------- Operation started : Reading message  --------------------------------" )
        print("*"*250)
        response = send_whatsapp_message(phone, msg)
        print("*"*250)
        print("--------------------------------  End of Operation  --------------------------------" )
        print("."*250)
        return jsonify({"message": "Message processed successfully."}), 200

    except Exception as e:
        print("------------------------------------Operation failed------------------------------------------------" )
        print(f"Error: {e}")
        print("-------------------------------------------------------------------------------------------" )
        return jsonify({"error": str(e)}), 500

