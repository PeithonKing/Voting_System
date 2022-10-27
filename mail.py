from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import time
import string
import random
import json
from tqdm import tqdm

class Email:
    def __init__(self, email, password):
        smtp = smtplib.SMTP(host="smtp.gmail.com", port=587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(my_email, app_password)
        self.smtp = smtp

    def send_email(self, to, subject="Vaktabya Election"):

        key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        
        with open("all_keys.json") as f:
            data = json.load(f)
            data.append(key)
        with open("all_keys.json", "w") as f:
            json.dump(data, f)

        body = f"""
Hi!
<p>Your SECRET_KEY: {key}</p>
<p>Link to voting site: <a href="http://10.0.25.108:5050/">Vote Here</a></p>
<p>Link to Results site: <a href="http://10.0.25.108:5050/results">See Live Results Here</a></p>


<p>Thank You,</p>
<p>Team ...</p>
        """

        message = MIMEMultipart()
        message["from"] = "Aritra Mukhopadhyay"
        message["to"] = to
        message["subject"] = subject
        message.attach(MIMEText(body, "html"))
        self.smtp.send_message(message)


my_email = "amukherjeeniser@gmail.com"
app_password = "<app_password>"
email = Email(my_email, app_password)

mail_ids = list(set(pd.read_csv("mail_ids_test.csv").T.values[0].tolist()))

for person in tqdm(mail_ids):
	email.send_email(person)
	time.sleep(1)