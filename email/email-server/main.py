from controllers.emailScript import GmailAccount
import os

while True:
    try:
        account = GmailAccount()
        attachments = account.run()
        for attachment in attachments:
            print('Deleting...')
            os.remove(attachment)
        
    except EOFError:
        account.quit()
        break
