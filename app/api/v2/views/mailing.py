import smtplib
import os


class SendMail:
    def __init__(self):
        pass

    def send_mail(self, message, to, subject):
        # Gmail Sign In
        gmail_sender = os.getenv("EMAIL")
        gmail_passwd = os.getenv("EMAIL_PASS")

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_sender, gmail_passwd)

            BODY = '\r\n'.join(['To: %s' % to,
                                'From: %s' % gmail_sender,
                                'Subject: %s' % subject,
                                '', message])

            server.sendmail(gmail_sender, [to], BODY)
            res = "sent"
        except:
            res = "fail"
        server.quit()
        return res
