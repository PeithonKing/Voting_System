IP = '127.0.0.1'  # your local IP address
PORT = 5500  # any port you like
DOMAIN = f'http://{IP}:{PORT}'
debug = True  # set to True in testing and False in production

organisation = "Vaktavya"  # your organisation's name
from_name = "Vaktavya Election Committee"  # this will apear in the emails sent

my_email = "example@gmail.com"  # email ID to send emails from
app_password = "<app_password>"  # 16 digit app password for the above email ID (this is not the password of your google account)

mail_ids_file = "mail_ids_test.csv"  # file containing the mail IDs of all the voters (properly formatted)

keep_nota = False  # set to True if you want to keep NOTA as a candidate
allow_empty_submissions = not keep_nota

candidates = {
    "president": [
        "president Candidate 1",
        "president Candidate 2",
    ],
    "vice president": [
        "vice president Candidate 1",
        "vice president Candidate 2",
    ],
    "secretary": [
        "secretary Candidate 1",
        "secretary Candidate 2",
    ],
}

# add NOTA to every position in candidates if keep_nota is True
if keep_nota:
    for position in candidates:
        candidates[position].append("NOTA")
