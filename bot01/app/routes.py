from flask import Flask, Blueprint, request, jsonify
import psycopg2
import psycopg2.extras
from app.send_message import send_whatsapp_message
from config import DATABASE_URL, WASSI_API_KEY
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
        event_type = msg['event']
        if event_type != "message:in:new":
            return jsonify({"error": "Unsupported event type"}), 200

        # Extract necessary fields
        phone = data.get('fromNumber')
        message_id = data.get('id')
        message_type = data.get('type')  # "text" or "image"
        body = data.get('body') if message_type == "text" else data.get('media', {}).get('url')

        print("-------------------------------------------------------------------------------------------" * 6)
        print("-------------------------INCOMING MSG : (message:in:new)---------------------------------------" * 3)
        print("--------------------------------------------------------------------------" * 6)
        print(json.dumps(msg, indent=4))  # Pretty print the incoming JSON payload
        print("--------------------------------------------------------------------------" * 6)

        # Database operations
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                # Check if record already exists for this message_id
                cursor.execute("SELECT message_id FROM processed_messages WHERE message_id = %s", (message_id,))
                row = cursor.fetchone()


                print("-------------------------------------------------------------------------------------------" * 6)
                print("--------------------------------  checking for new Unique ID   --------------------------------" * 3)
                print("-------------------------------------------------------------------------------------------" * 6)

                if not row:
                    # Insert new record
                    print("-------------------------------------------------------------------------------------------" * 6)
                    print("--------------------------------  INSERTING INTO RECORDS  --------------------------------" * 3)
                    print("-------------------------------------------------------------------------------------------" * 6)
                    query = """
                    INSERT INTO processed_messages (phone, message_id, message_type, body) 
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query, (phone, message_id, message_type, body))
                    
                conn.commit()
        #SEND msg to incoming msg
        print("-------------------------------------------------------------------------------------------" * 6)
        print("--------------------------------  Generating Response  --------------------------------" * 3)
        print("-------------------------------------------------------------------------------------------" * 6)
        response = send_whatsapp_message(phone, msg)
        print("-------------------------------------------------------------------------------------------" * 6)
        print("--------------------------------  EOF  --------------------------------" * 3)
        print("-------------------------------------------------------------------------------------------" * 6)
        return jsonify({"message": "Message processed successfully."}), 200

    except Exception as e:
        print("-------------------------------------FAILURE------------------------------------------------" * 6)
        print(f"Error: {e}")
        print("-------------------------------------------------------------------------------------------" * 6)
        return jsonify({"error": str(e)}), 500
