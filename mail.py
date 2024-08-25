from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import time
import string
import random
import json
from tqdm import tqdm

from example_settings import *

class Email:
    def __init__(self, email, password):
        smtp = smtplib.SMTP(host="smtp.gmail.com", port=587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(my_email, app_password)
        self.smtp = smtp

    def send_email(self, to, subject=f"{organisation} Election secret key"):

        key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        
        try:
            with open("all_keys.json") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        data.append(key)
        with open("all_keys.json", "w") as f:
            json.dump(data, f)

        body = f"""
Hi!

Here is your secret key for the {organisation} Election. Please keep it safe, don't share it with anyone. <b>You need to connect to the NISER Intranet for the voting site to work.</b>

<p>Your SECRET_KEY (copy this): <strong>{key}</strong></p>
<p>Link to voting site: <a href="{DOMAIN}/">Vote Here</a></p>
<!-- <p>Link to Results site: <a href="{DOMAIN}/results">See Live Results Here</a></p> -->


<p>Thank You,</p>
<p>{from_name}</p>
        """

        message = MIMEMultipart()
        message["from"] = from_name
        message["to"] = to
        message["subject"] = subject
        message.attach(MIMEText(body, "html"))
        
        try:
            self.smtp.send_message(message)
            print(f"Email sent to {to}")
        except Exception as e:
            print(e)
            print(f"ERROR: Email not sent to {to}")


email = Email(my_email, app_password)

mail_ids = list(set(pd.read_csv(mail_ids_file).T.values[0].tolist()))

for person in tqdm(mail_ids):
    email.send_email(person)
    time.sleep(1)
