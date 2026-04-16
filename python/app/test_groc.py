from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv("../../.env")

key = os.getenv("GROQ_API_KEY")
print("Clé trouvée :", key[:15] if key else "AUCUNE CLÉ ❌")

client = Groq(api_key=key)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Dis juste: OK"}],
    max_tokens=10
)

print("Réponse Groq :", response.choices[0].message.content)
print("✅ Groq fonctionne parfaitement !")