from datetime import date, timedelta

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import urllib.request
import urllib.parse
import requests, sys
requests.packages.urllib3.disable_warnings()

# Variables
smtp_host = ""
smtp_port = 25
smtp_username = ""
smtp_password = ""
smtp_use_tls = False
smtp_use_auth = False
smtp_from_address = ""
smtp_to_address = ""
cv_center_ip = ""
cv_token = ""

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

# Helper: call Cyber Vision API
def call_route(route, params):
    route += '?'
    # append parameters
    for key in params.keys():
        route += '&' + urllib.parse.quote(str(key)) + '=' + \
                 urllib.parse.quote(str(params[key]))
    # finalise the route
    route = url_for(cv_center_ip, route)
    # launch the request
    try:
        json_data = requests.get(route, headers={"X-Token-Id": cv_token}, verify=False).json()
        print("LOG: Succesfull call to %s" % route)
    except:
        print("ERROR: Unable to make a call to %s, exiting..." % route)
        sys.exit(1)
    return json_data

# Helper: call Cyber Vision API recursively
def call_route_recursive(route, params=None):
    results = []
    need_more = True
    offset = 0
    batch_size = 2000
    while need_more:
        if not params:
            params = {}
        params.update({'limit': batch_size, 'offset': offset})
        t = call_route(route, params)
        results = results + t
        # if there is nil answer or we ask for batch_size (ie 2000) and get less, stop
        if len(t) == 0 or batch_size > len(t):
            need_more = False
    return results

# Helper: construct Cyber Vision URL
def url_for(center_ip, route):
    return f"https://{center_ip}{route}"

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
    route = "/api/1.0/event"
    parameters = {
            'start': filter_start.strftime('%Y-%m-%d %H:%M'),
            'end': filter_end.strftime('%Y-%m-%d %H:%M'),
            'severity': "very_high",
            'severity': "high",
        }
    data = call_route_recursive(route, params=parameters)

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
            email_body = render(events, "https://%s" % cv_center_ip)

            # STEP 3.2: Craft the e-mail
            subject = "Cisco Cyber Vision - %d Important Event(s) (From: %s To: %s)" % (nb_new_events, filter_start, filter_end)

            # STEP 3.3: Send the e-mail
            email_notifier.sendEmail(smtp_from_address, smtp_to_address, subject, email_body)
            print("LOG: Email sending successfully with subject : \"%s\"" % subject)
        except:
            print("WARNING: Email notification failed")

if __name__ == "__main__":
    alert_events()