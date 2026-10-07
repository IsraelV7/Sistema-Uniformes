import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)


def enviar_pin(correo_destino: str, pin: str):
    cuerpo = (
        f"Tu codigo de verificacion para restablecer tu contrasena es: {pin}\n\n"
        f"Este codigo expira en 10 minutos. Si no solicitaste este cambio, ignora este correo."
    )

    # "utf-8" le dice a MIMEText que el texto puede tener tildes/ñ sin romperse
    mensaje = MIMEText(cuerpo, "plain", "utf-8")
    mensaje["Subject"] = Header("Codigo de recuperacion de contrasena", "utf-8")
    mensaje["From"] = SMTP_FROM
    mensaje["To"] = correo_destino

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as servidor:
        servidor.starttls()
        servidor.login(SMTP_USER, SMTP_PASSWORD)
        servidor.sendmail(SMTP_FROM, [correo_destino], mensaje.as_string())