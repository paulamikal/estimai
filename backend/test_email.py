import resend
from dotenv import load_dotenv
import os

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

r = resend.Emails.send({
    "from": "EstimAI <onboarding@resend.dev>",
    "to": "paulareusok@gmail.com",
    "subject": "Test EstimAI",
    "html": "<p>Prueba de envío desde <strong>EstimAI</strong></p>"
})

print(r)