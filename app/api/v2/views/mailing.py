import smtplib
import os


class SendMail:
    def __init__(self):
        pass

    def send_mail(self, message, to, subject):
        TO = to
        SUBJECT = subject
        TEXT = message
        # Gmail Sign In
        gmail_sender = os.getenv("EMAIL")
        gmail_passwd = os.getenv("EMAIL_PASS")

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_sender, gmail_passwd)

        BODY = '\r\n'.join(['To: %s' % TO,
                            'From: %s' % gmail_sender,
                            'Subject: %s' % SUBJECT,
                            '', TEXT])

        try:
            server.sendmail(gmail_sender, [TO], BODY)
            res = "sent"
        except:
            res = "fail"
        server.quit()
        return res
