import imaplib
import email
import os
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re
from config import mail_pass, username, imap_server
import chardet

mail = imaplib.IMAP4_SSL(imap_server)
mail.login(username, mail_pass)
mail.select("INBOX")
res, msg = mail.search(None, "ALL")
msg = msg[0].split()[-20:]
data = [email.message_from_string(mail.fetch(i, "(RFC822)")[1][0][1].decode()) for i in msg]
components = []
for i in data:
    if i.is_multipart():
        n = []
        for j in i.get_payload():
            # if len(j.get_payload()) == 2:
            #     print(j.get_payload()[1])
            #     print('---')
            n.append(len(j.get_payload()))
        components.append(n)
    else:
        components.append(len(i.get_payload()))

print(components)