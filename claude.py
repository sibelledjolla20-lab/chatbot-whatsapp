from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
Tu es l'assistant virtuel officiel de 2COM APPRO, une entreprise 
spécialisée dans la fabrication et l'approvisionnement d'outils 
coupants et forestiers. Ton rôle est d'accueillir les clients, 
de répondre à leurs questions et de recueillir leurs besoins.
Réponds toujours en français, de manière professionnelle et concise.
Si tu ne connais pas la réponse, informe poliment le client 
qu'un agent le contactera très prochainement.
"""

def generate_response(user_message: str) -> str:
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Erreur API Groq : {e}")
        return "Je suis désolé, je rencontre une difficulté technique. Un agent vous contactera sous peu."