import smtplib, ssl
import email
import getpass
import sys
file = open("result.txt", "r")

file_data = file.readline()
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

port = 465
print("Strating...")

subject = "The file is attached"
body = file_data
password = "HULtest@1807"
sendermail = "testmail180797@gmail.com"
recievermail = "vishutyagi018@gmail.com"

#wpassword = getpass.getpass(prompt='Password: ', stream=None)
print("Got the password")
message = MIMEMultipart()
message["From"] = sendermail
message["To"] = recievermail
message["Subject"] = subject
message["Bcc"] = recievermail
message.attach(MIMEText(body, "plain"))



part = MIMEBase("application", "octet-stream")
part.set_payload(file.read())

encoders.encode_base64(part)

'''part.add_header(
    "Content-Disposition",
    f"attachment; filename= {file}",
)'''

#message.attach(part)
message = message.as_string()



context = ssl.create_default_context()
print("sending")



with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sendermail, password)
    server.sendmail(sendermail, recievermail, message)



