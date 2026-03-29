from flask import Flask, request
from twilio.rest import Client
from claude import generate_response
from dotenv import load_dotenv
import os
import threading

load_dotenv()

app = Flask(__name__)

twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def process_and_respond(sender, message):
    try:
        ai_response = generate_response(message)
        twilio_client.messages.create(
            from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
            to=sender,
            body=ai_response
        )
        print(f"Réponse envoyée à {sender}")
    except Exception as e:
        print(f"Erreur : {e}")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_message = request.form.get("Body", "").strip()
    sender = request.form.get("From", "")
    print(f"Message reçu de {sender} : {incoming_message}")
    thread = threading.Thread(
        target=process_and_respond,
        args=(sender, incoming_message)
    )
    thread.start()
    return "OK", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)