# -*- coding: utf-8 -*-

# mailnotify - modul pro posílání notifikací e-mailem

import smtplib
from email.mime.text import MIMEText

def sendNotification(smtp, f, to, subject, body):
    # odešle notifikaci e-mailem
    msg = MIMEText(body) # tělo mailu
    # sestavíme hlavičky:
    msg['Subject'] = subject
    msg['From'] = f
    msg['To'] = to
    # a pošleme:
    s = smtplib.SMTP(smtp)
    s.sendmail(f, [to], msg.as_string())
    s.quit()
