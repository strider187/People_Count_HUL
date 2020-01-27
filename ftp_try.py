import smtplib
import ssl
context = ssl.create_default_context()
port = 465
print(1)
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:


    print(2)

    server.set_debuglevel(True)

    print(3)
    try:
        print(4)
        test_mail = server.verify("test180797@gmail.com")
        test_mail2 = server.verify("bafgahgv")

    finally:
        print(5)
        server.quit()

    print(test_mail)
    print((test_mail2))