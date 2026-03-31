import smtplib

server = smtplib.SMTP("127.0.0.1", 1025)
server.set_debuglevel(1)

message = """From: lead@example.com
Subject: Interested

I want to know more about your product
Schedule me a meeting
"""

print(" Sending email...\n", message)

result = server.sendmail(
    "lead@example.com",
    ["sales@yourapp.com"],
    message
)

print(" Result:", result)

server.quit()