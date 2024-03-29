from datetime import date, timedelta
from dotenv import load_dotenv

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import urllib.request
import urllib.parse
import requests, sys, os, json
requests.packages.urllib3.disable_warnings()

load_dotenv()

# Variables
smtp_host = os.environ['SMTP_HOST']
smtp_port = 587
smtp_username = os.environ['SMTP_USERNAME']
smtp_password = os.environ['SMTP_PASS']
smtp_use_tls = False
smtp_use_auth = False
smtp_from_address = os.environ['SMTP_FROM']
smtp_to_address = os.environ['SMTP_TO']

# Helper: email notifier
class EmailNotifier:
    def __init__(self, host, port, login, password, use_tls = True, use_auth = True):
        self.host = host
        self.port = port
        self.use_auth = use_auth
        self.use_tls = use_tls
        self.login = login
        self.password = password

    def sendEmail(self, fromAddr, toAddr, subject, body):
        with smtplib.SMTP(self.host, self.port) as server:
            server.ehlo()
            if self.use_tls:
                server.starttls()
                server.ehlo()
            if self.use_auth:
                server.login(self.login, self.password)
            msg = MIMEMultipart()
            msg['From'] = fromAddr
            msg['To'] = toAddr
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()
            server.sendmail(fromAddr, toAddr, text)

# Helper: render event e-mail
def render(events = [], link = ""):
    data = {}
    output = "%d new important event(s):\n\n" % len(events)

    # Group by severity
    for event in events:
        if event["severity"] not in data:
            data[event["severity"]] = {}
        if event["type"] not in data[event["severity"]]:
            data[event["severity"]][event["type"]] = {}
        if event["family"] not in data[event["severity"]][event["type"]]:
            data[event["severity"]][event["type"]][event["family"]] = {}
        if event["category"] not in data[event["severity"]][event["type"]][event["family"]]:
            data[event["severity"]][event["type"]][event["family"]][event["category"]] = []
        data[event["severity"]][event["type"]][event["family"]][event["category"]].append(event)

    for severityEvent, level1 in list(data.items()):
        output += "\n# Severity \"%s\"\n" % (severityEvent)
        for typeEvent, level2 in list(level1.items()):
            output += "\n# Type \"%s\"\n" % (typeEvent)
            for familyEvent, level3 in list(level2.items()):
                output += "\n# Family \"%s\"\n" % (familyEvent)
                for categoryEvent, evts in list(level3.items()):
                    output += "\n# Category \"%s\"\n" % (categoryEvent)
                    for evt in evts:
                        output += "- [%s] %s (Id: %s)\n" % (evt["creation_time"].split("+")[0], evt["message"], evt["id"])
                    output += "\n"

    output += "\n\nPlease visit Cisco Cyber Vision backend to obtained more details, ie: %s\n\n" % (link)

    return output

# Main script: Retrieve events of high and very high severity
def alert_events():
    # Init filters
    today               = date.today()
    filter_start        = today - timedelta(hours=1)
    filter_end          = today + timedelta(hours=1)

    # Init notifier
    email_notifier = EmailNotifier(smtp_host, smtp_port, smtp_username, smtp_password, smtp_use_tls, smtp_use_auth)
    print (('ici1'))

    # STEP 1: Retrieve all events from interval
    data = json.load('response.json')

    # STEP 2: Apply logic to events returned
    events = []
    for event in data:
        events.append(event)
    nb_new_events = len(events)

    if nb_new_events > 0:
        print(("%d new important event(s) from %s to %s." % (nb_new_events, filter_start, filter_end)))

        # STEP 3: Send notifications (Email)
        try:
            # STEP 3.1: Craft the e-mail body
            email_body = render(events, "https://%s" % "Cyber Vision DUMMY")

            # STEP 3.2: Craft the e-mail
            subject = "Cisco Cyber Vision - %d Important Event(s) (From: %s To: %s)" % (nb_new_events, filter_start, filter_end)

            # STEP 3.3: Send the e-mail
            email_notifier.sendEmail(smtp_from_address, smtp_to_address, subject, email_body)
            print("LOG: Email sending successfully with subject : \"%s\"" % subject)
        except:
            print("WARNING: Email notification failed")

if __name__ == "__main__":
    alert_events()