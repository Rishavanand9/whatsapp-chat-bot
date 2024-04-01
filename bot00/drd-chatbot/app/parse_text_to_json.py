import json
import re

def parse_text(text):
    with open("image_texts.txt", "a") as logfile:
        logfile.write(json.dumps(text) + "\n" + "----------------------------------------------")
    # Define regular expression patterns to match different data points
    transaction_id_pattern = r"(UPI Ref\. No:|Transaction ID|Reference Number|Reference No\. \(UTR No\./RRN\))\s*:?\s*([A-Za-z0-9]+)"
    date_pattern = r"(\d{1,2} \w{3} 2024[\s,-]+[\d:APM]+)"
    amount_pattern = r"Amount|Payment Successful|Transfer Amount|Total Amount Transfered\s*[^\d]*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)"
    receiver_pattern = r"(To|Paid to|Beneficiary name|Payee Name)\s*:?\s*([A-Za-z\s.]+[A-Za-z])"
    sender_pattern = r"(From)\s*:?\s*([\w\s]+)"
    remarks_pattern = r"Remarks\s*:?\s*(.*)"

    # Search for matches in the text
    transaction_id_match = re.search(transaction_id_pattern, text, re.MULTILINE)
    date_match = re.search(date_pattern, text, re.MULTILINE)
    amount_match = re.search(amount_pattern, text, re.MULTILINE)
    receiver_match = re.search(receiver_pattern, text, re.MULTILINE)
    sender_match = re.search(sender_pattern, text, re.MULTILINE)
    remarks_match = re.search(remarks_pattern, text, re.MULTILINE)

    # Extracting matched values
    transaction_id = transaction_id_match.group(2) if transaction_id_match else None
    date = date_match.group(1) if date_match else None
    amount = amount_match.group(1) if amount_match else None
    receiver = receiver_match.group(2) if receiver_match else None
    sender = sender_match.group(2) if sender_match else None
    remarks = remarks_match.group(1) if remarks_match else None

    # Normalize amount by removing commas
    if amount:
        amount = amount.replace(',', '')

    output = {
        'transaction_id': transaction_id,
        'date': date,
        'amount': amount,
        'receiver': receiver,
        'sender': sender,
        'remarks': remarks,
    }

    with open("output.txt", "a") as logfile:
        logfile.write(json.dumps(output) + "\n")

    return output