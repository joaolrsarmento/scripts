from constants.constants import GMAIL_HOST, GMAIL_PORT, EMAIL_RECEIVER, EMAIL_SENDER, ENABLE_LESS_SECURE_APPS_URL, SAVE_DIR, PASSWORD_RECEIVER
import imaplib, os, email

class GmailAccount:
    def __init__(self):

        self.__server = self.__connect()

    def run(self):
        try:
            attachments = self.__getAttachments(self.__server)
            return attachments
        except EOFError:
            raise EOFError
    
    def quit(self):
        print('End.')
        self.server.quit()

    def __connect(self):
        print('Connecting...')
        server = imaplib.IMAP4_SSL(GMAIL_HOST, GMAIL_PORT)
        print('Logging in...')
        server.login(EMAIL_RECEIVER, PASSWORD_RECEIVER)
        server.select('inbox')
        print('Logged.')
        return server
    def __getAttachments(self, server):
        
        attachments = []

        resp, messages = server.search(None, 'UNSEEN', 'FROM', EMAIL_SENDER)
        for message in messages[0].split():
            typ, data = server.fetch(message, '(RFC822)')
            msg= email.message_from_string(str(email.message_from_bytes(data[0][1])))

            for part in msg.walk():


                if part.get_content_type() ==  'application/pdf':
                        print('Found a new file.')
                        payload = part.get_payload(decode=True)
                        filename = part.get_filename()

                        if payload and filename:
                            filepath = SAVE_DIR + '/' + filename
                            with open(filepath, 'wb') as f:
                                f.write(payload)
                            attachments.append(filepath)
        return attachments