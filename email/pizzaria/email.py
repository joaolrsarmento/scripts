import poplib
from constants import ENABLE_LESS_SECURE_APPS_URL, GMAIL_HOST, GMAIL_PORT, SAVE_DIR
import getpass
import email
import os

class GMailAccount:
    """
    Connects to pop gmail server and log in.
    Also, you can get email attachments and others parses.
    """
    def __init__(self) -> None:
        """
        BOOLEAN logged -> is the user logged in? True or False
        """
        self.logged = False
        self._login()
        self._getAttachments()

    def _login(self) -> bool:
        """
        Connects to pop server and log the user in.
        """
        try:
            # Try to connect to the server
            self.server = poplib.POP3_SSL(GMAIL_HOST, GMAIL_PORT)
        except:
            raise "Unable to access gmail server. Try again later."
        
        # Debugger level
        self.server.set_debuglevel(1)
        # Get user credentials
        self._getCredentials()
        # Try to log in until the connection is completed
        while not self.logged:
            try:
                print('Logging...')
                self.server.user(self.username)
                print('Logging...')
                self.server.pass_(self.password)
                print('Logged successfully.')
                self.logged = True
            except:
                print ("Invalid credentials")
                print("Are you sure you have enable access?")
                print("Try to enable access on this link:", ENABLE_LESS_SECURE_APPS_URL)
                answer = input('Want to try again? (Y/N) ')
                if answer.lower() =='y' or answer.lower() == 'yes':
                    self._getCredentials()
        return True

    def _getCredentials(self) -> None:
        """
        If the user is not connected, get username and password
        """
        if not self.logged:
            # Get email
            self.username = input('Enter your email (example: example@gmail.com): ')
            # Get password
            self.password = getpass.getpass('Enter your password: ')
    
    def _getAttachments(self, keyword: str) -> str:
        """
        If there is a new email with the keyword given in the subject, 
        this method gets its attachment.
        :params: keyword -> keyword to be searched for in the email subject
        :returns: path -> path to the attachment
        """
    def _endConnection(self) -> None:
        """
        Closes the connection with the server
        """
        self.server.quit()

account = GMailAccount()

print('Hey mate, here I am')