from my_email import email_mine , password_mine

#Added this so that we can import config file

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from config import excel_report_path

import smtplib, ssl
import glob
from datetime import date
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


sys.argv.pop(0)

emails = sys.argv

subject = "Test Case Results for "+date.today().strftime("%d/%m/%Y")
body = "These are the test case results"
# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = email_mine
message["To"] = ", ".join(emails) #for multiple
message["Subject"] = subject


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
  
    <div>Hi User, <br><br>
The test cases have been run successfully.<br>
You can view the excel report in the attachment and the Allure report in the link provided.</div>
    <p>
       <a href="https://alluringreport.netlify.app/">Allure Report</a> 
    </p>
    <div>Thank you, <br>
    PFD Automation Team A</div>
    
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
    server.sendmail(email_mine, emails, text)