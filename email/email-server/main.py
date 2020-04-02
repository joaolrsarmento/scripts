from controllers.emailScript import GmailAccount
from controllers.printScript import Printer
from constants.constants import ENABLE_LESS_SECURE_APPS_URL
import os

print('Be sure to enable the access on your email.')
print('If you are not sure, check on:', ENABLE_LESS_SECURE_APPS_URL)
print('Be sure to fill the informations on the file constants/constants.py')
print('Be sure to enable the access of the module IMAP Lib on your email\n'
      'You should go to your email settings and enable the access of IMAP\n')
print('Starting program...')

while True:
    """
    This server shall be running until EOF.
    Obs. It's only available for windows, for now.
    """
    try:
        # Connects
        account = GmailAccount()
        # Get printer
        printer = Printer()
        # Get new attachments
        attachments = account.run()
        # Iterator over them, print and delete.
        for attachment in attachments:
            print('Printing: ', attachment.split('/')[len(attachment.split('/')) - 1])
            # Print the attachment pdf
            printer.run(attachment)
            print('Deleting...')
            # Delete the attachment from the pc memmory
            os.remove(attachment)
    
    except EOFError:
        # If EOF, quit server.
        account.quit()
        break
    else:
        # Try again.
        continue
