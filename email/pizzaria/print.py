import imaplib
import email
import os
    
svdir = '~/Downloads'
    
    
mail=imaplib.IMAP4('imap.gmail.com', 993)

mail.login("joaolrsarmento@gmail.com","Fake@186684")
mail.select("inbox")
    
typ, msgs = mail.search(None, '(SUBJECT "Cadastro email ITA para google classroom")')
msgs = msgs[0].split()
    
for emailid in msgs:
    resp, data = mail.fetch(emailid)
    email_body = data[0][1] 
    m = email.message_from_string(email_body)
    
    
    if m.get_content_maintype() != 'multipart':
        continue
    
    for part in m.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
    
        filename=part.get_filename()
        if filename is not None:
            sv_path = os.path.join(svdir, filename)
            if not os.path.isfile(sv_path):
                print (sv_path)    
                fp = open(sv_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()