from email_report.my_email import email_mine , password_mine
from email_report.email_addresses import email1 #,email2

from config import excel_report_path

import smtplib, ssl
import glob

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "Excel report of test cases"
body = "These are the test case results"
# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = email_mine
message["To"] = email1
message["Subject"] = subject
#message["Bcc"] = email1  # Recommended for mass emails

# Add body to email
#message.attach(MIMEText(body, "plain"))

filename = glob.glob(f"{excel_report_path}/*.xlsx")[0]

# Open Excel file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)
# Add link to Allure
#text1 = """\
    #Here is the link to the Allure Report and Excel File"""
html = """\
<html>
  <body>
    <p>
       <a href="https://alluringreport.netlify.app/">Allure Report</a> 
    </p>
    <br><br>
    <div>Here is the link to the Allure Report and Excel File</div>
  </body>
</html>
"""
#message.attach(MIMEText(text1, "plain"))
message.attach(MIMEText(html, "html"))
#message.attach(MIMEText(text1, "plain"))

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(email_mine, password_mine)
    server.sendmail(email_mine, email1, text)