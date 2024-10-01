import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_to = os.getenv("EMAIL_TO")
email_from = os.getenv("EMAIL_FROM")
email_password = os.getenv("EMAIL_PASSWORD")

msg = MIMEMultipart()
msg["Subject"] = "Resultado do Pipeline"
msg["From"] = email_from
msg["To"] = email_to

body = "Pipeline executado com sucesso!"
msg.attach(MIMEText(body, "plain"))

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_from, email_password)
        server.sendmail(email_from, email_to, msg.as_string())
    print(f"E-mail enviado para {email_to}")
except smtplib.SMTPException as e:
    print(f"Falha ao enviar e-mail: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
