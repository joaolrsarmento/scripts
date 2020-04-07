from controllers.emailScript import GmailAccount
from constants.constants import ENABLE_LESS_SECURE_APPS_URL, EMAIL_RECEIVER, EMAIL_SENDER, PASSWORD_RECEIVER
import sys
import os

print('Be sure to enable the access on your email.')
print('If you are not sure, check on:', ENABLE_LESS_SECURE_APPS_URL)
print('Remember to fill the informations marked with "INSERT HERE" in constants/constants.py file.')
print('Be sure to enable the access of the module IMAP Lib on your email.\n'
    'You should go to your email settings and enable the access of IMAP')
print('Starting program...')

while True:
    """
    This server shall be running until EOF.
    Obs. It's only available for windows for now.
    """
    try:
        # Connects
        account = GmailAccount(EMAIL_RECEIVER,
                                PASSWORD_RECEIVER,
                                EMAIL_SENDER)

        # Get printer
        if sys.platform.lower() == 'linux':
            # Linux
            from controllers.printScriptLinux import PrinterLinux
            printer = PrinterLinux()
        else:
            # Windows
            from controllers.printScriptWindows import PrinterWindows
            printer = PrinterWindows()
        # Get new attachments
        attachments = account.run()
        # Iterate over them, print and delete.
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
        print('Unable to connect. Trying again.')
        continue
