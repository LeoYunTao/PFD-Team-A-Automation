import smtplib
gmail_user = 'iamfast987654321@gmail.com'
gmail_password = 'slowestmanever'

sent_from = gmail_user
to = ['s10222202@gmail.com', 'person_b@gmail.com']
subject = 'test'
body = 'testing 123'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print ("Email sent successfully!")
except Exception as ex:
    print ("Something went wrong….",ex)