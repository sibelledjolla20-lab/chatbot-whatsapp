from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from claude import generate_response
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Récupère le message envoyé par le client
    incoming_message = request.form.get("Body", "").strip()
    sender = request.form.get("From", "")
    
    print(f"Message reçu de {sender} : {incoming_message}")
    
    # Génère une réponse avec Claude
    ai_response = generate_response(incoming_message)
    
    print(f"Réponse générée : {ai_response}")
    
    # Envoie la réponse via Twilio
    response = MessagingResponse()
    response.message(ai_response)
    
    return str(response)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)