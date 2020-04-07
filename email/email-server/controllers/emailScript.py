from constants.constants import GMAIL_HOST, GMAIL_PORT, ENABLE_LESS_SECURE_APPS_URL, SAVE_DIR
import imaplib, os, email

class GmailAccount:
    """
    Represents an gmail account.
    """
    def __init__(self, receiver, pw, sender):

        self.receiver = receiver
        self.password = pw
        self.sender = sender

        self.__server = self.__connect()

    def run(self) -> None:
        """
        Method called to get the attachments on the email.
        """
        try:
            attachments = self.__getAttachments(self.__server)
            return attachments
        except EOFError:
            raise EOFError
    
    def quit(self) -> None:
        """
        Closes the server.
        """
        print('End.')
        self.server.quit()

    def __connect(self) -> None:
        """
        Connects to the gmail server using the username and password.
        """
        print('Connecting...')
        # Get server
        server = imaplib.IMAP4_SSL(GMAIL_HOST, GMAIL_PORT)
        print('Logging in...')
        # Try username and password
        server.login(self.receiver, self.password)
        # Select inbox only
        server.select('inbox')
        # Success
        print(server.check())
        return server

    def __getAttachments(self, server) -> list:
        """
        Private method that searchs through inbox to emails sent by an specific sender.
        """
        # Stores the paths to the attachments stored on the computer.
        attachments = []
        # Search data
        resp, messages = server.search(None, 'UNSEEN', 'FROM', self.sender)
        for message in messages[0].split():
            typ, data = server.fetch(message, '(RFC822)')
            # Decode
            msg= email.message_from_string(str(email.message_from_bytes(data[0][1])))
            # Search for pdf
            for part in msg.walk():
                # If a pdf is found, try to save it.
                if part.get_content_type() ==  'application/pdf':
                        print('Found a new file.')
                        payload = part.get_payload(decode=True)
                        filename = part.get_filename()

                        # If there isn't false data, save it
                        if payload and filename:
                            filepath = SAVE_DIR + '/' + filename
                            with open(filepath, 'wb') as f:
                                f.write(payload)
                            # Store the path
                            attachments.append(filepath)
        return attachments