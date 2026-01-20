import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import Criteria, Job
import datetime

def send_job_email(jobs):
    criteria = Criteria.query.first()
    if not criteria or not criteria.email_enabled or not criteria.email_address:
        print("Email sending skipped: No criteria or email disabled.")
        return

    msg = MIMEMultipart()
    msg['From'] = criteria.smtp_user
    msg['To'] = criteria.email_address
    msg['Subject'] = f"Weekly Job Feed - {len(jobs)} New Jobs found"

    body = f"<h2>Found {len(jobs)} new jobs for keywords: {criteria.keywords}</h2><ul>"
    
    for job in jobs:
        body += f"<li><a href='{job['url']}'><b>{job['title']}</b></a> at {job['company']} ({job['location']}) - Score: {job['relevance_score']}</li>"
    
    body += "</ul>"
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(criteria.smtp_server, criteria.smtp_port)
        server.starttls()
        server.login(criteria.smtp_user, criteria.smtp_password)
        text = msg.as_string()
        server.sendmail(criteria.smtp_user, criteria.email_address, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
