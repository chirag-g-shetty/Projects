from email.message import EmailMessage
import ssl,smtplib,random as rand

my_mail = 'justgestpy@gmail.com'
my_pass = 'pmjwtzmbktrdzick'

sub = 'OTP from JustGest'

otp = str(rand.randint(1000,9999))
body = \
f"""
<html>
<head>Welcome to JustGest!<br>
<i>Hope this software makes your computer experience richer!</i><br>
The OTP is <b>{otp}</b><br>
Note - Please do not share this OTP with anyone.
</head>
</html>"""

em = EmailMessage()
em['From']=my_mail
em['Subject']=sub
em.add_header('Content-Type', 'text/html')
em.set_payload(body)

def mailer(client):
    global em,my_pass,my_mail,otp
    em['To']=client
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(my_mail,my_pass)
        smtp.send_message(em)
    return otp