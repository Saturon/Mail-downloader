
import imaplib
#This script moves msg from 1 folder to another
obj = imaplib.IMAP4_SSL('imap.mail.ru', 993)
obj.login('Example@mail.ru', 'Examplepassword')
obj.select('INBOX')
apply_lbl_msg = obj.uid('COPY', b'1', 'Archive')
if apply_lbl_msg[0] == 'OK':
    mov, data = obj.uid('STORE', b'1' , '+FLAGS', '(\Deleted)')
    obj.expunge()