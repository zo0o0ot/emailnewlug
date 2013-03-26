"""
Changes to this script were done by Ross Larson in 2013.
Original copryright message follows:

Copyright (c) 2012 Mike Putnam <mike@theputnams.net>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import argparse
import os
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64

"""
Based on http://codecomments.wordpress.com/2008/01/04/python-gmail-smtp-example/

Added argparse bits to move gmail credentials out of the script.
Hardcoded the schedule and messages into the script.
"""

def sendMail(u,p,r,subject, text, *attachmentFilePaths):
  gmailUser = u
  gmailPassword = p
  recipient = r

  msg = MIMEMultipart()
  msg['From'] = gmailUser
  msg['To'] = recipient
  msg['Subject'] = subject
  msg.attach(MIMEText(text))

  for attachmentFilePath in attachmentFilePaths:
    msg.attach(getAttachment(attachmentFilePath))

  mailServer = smtplib.SMTP('smtp.gmail.com', 587)
  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  mailServer.login(gmailUser, gmailPassword)
  mailServer.sendmail(gmailUser, recipient, msg.as_string())
  mailServer.close()

def getAttachment(attachmentFilePath):
  contentType, encoding = mimetypes.guess_type(attachmentFilePath)

  if contentType is None or encoding is not None:
    contentType = 'application/octet-stream'

  mainType, subType = contentType.split('/', 1)
  file = open(attachmentFilePath, 'rb')

  if mainType == 'text':
    attachment = MIMEText(file.read())
  elif mainType == 'message':
    attachment = email.message_from_file(file)
  elif mainType == 'image':
    attachment = MIMEImage(file.read(),_subType=subType)
  elif mainType == 'audio':
    attachment = MIMEAudio(file.read(),_subType=subType)
  else:
    attachment = MIMEBase(mainType, subType)
  attachment.set_payload(file.read())
  encode_base64(attachment)

  file.close()

  attachment.add_header('Content-Disposition', 'attachment',   filename=os.path.basename(attachmentFilePath))
  return attachment

meetingNotice = """
Monthly NEWLUG meeting!     
Thursday 6:30pm-9pm     

Comfort Suites
3809 W. Wisconsin Ave.
Appleton, WI, 54914

What to bring:

Bring your own: 
Computer food.
Carry-ins of soda, snacks, and other beverages are allowed.  Send an email to the NEWLUG ninjas if you plan on bringing anything to share with the group.
Linux Devices, Tools and Utilities
Questions to ask about Linux

The Vision:
Bringing talented people together -- Accelerating technological
innovation and encouraging start-up companies in our area.

Open to anyone -- Professionals, Experts, and Students alike.

Further notes about the meeting (subject, presenter, etc.) will come in a separate message.  Hope to see you there!

NEWLUGbot
"""

footer = """
--                               
Recurring Monthly Events:        
* NEWLUG meeting  - 2nd Thursdays      
"""

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Send weekly events to NEWLUG mailing list.')
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    parser.add_argument('recipient')
    args = parser.parse_args()

    import datetime
    d = datetime.date.today()
    mon = d.day #cron runs every monday
    thu = (d + datetime.timedelta(days=3)).day
    if thu > 7  and thu <  15: sendMail(args.user,args.password,args.recipient,"This Week - NEWLUG Meeting Notice)", meetingNotice + footer)

