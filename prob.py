import imaplib
import email
import os
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re
from config import mail_pass, username, imap_server

def textParse(body):
    res = BeautifulSoup(body, 'html.parser')
    res = res.get_text().split("\n")
    res = [line.rstrip() for line in res]
    res = [line.replace("\t", '') for line in res]
    return res

def getTextFromLetter():
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, mail_pass)

    mail.list()
    mail.select("INBOX")
    result, data = mail.search(None, "UNSEEN")
    ids = data[0]
    latest_email_id = ids.split()[-1]
    result, data = mail.fetch(latest_email_id, "(RFC822)")
    email_message = email.message_from_string(data[0][1].decode())
    print(email_message)
    text = ""
    if email_message.is_multipart():
        for payload in email_message.get_payload():
            body = payload.get_payload(decode=True).decode('utf-8')
            body = textParse(body)
            for i in body:
                if i != "":
                    text += f" {i}\n"
        if len(text) > 100:
            text = text[0:200]
            text += "..."
    else:
        body = email_message.get_payload(decode=True).decode('utf-8')
        body = textParse(body)
        for i in body:
            if i != "":
                text += f" {i}\n"
        if len(text) > 100:
            text = text[0:200]
            text += "..."
    mail.close()
    mail.logout()
    return getLettersDeliver(email_message) + text

def getLettersDeliver(mail):
    let_from = mail["From"]
    let_theme = mail["Subject"]
    print(let_theme)
    let_theme = decode_header(mail["Subject"])[0][0].decode()
    return f"From: {let_from}\nTheme: {let_theme}\n"