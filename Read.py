import email, imaplib

#Read email

mail = imaplib.IMAP4_SSL('imap.mail.ru')
mail.login('Example1@mail.ru', 'Example1Password')
mail.list()
#print('Папки: ', mail.list()) # Выводит список папок в почтовом ящике.
mail.select("inbox") # Подключаемся к папке "входящие".
mail.search(None, 'ALL')
#print('Все ID: ', mail.search(None, 'ALL')) # Выводит список ID
print(mail.fetch(b'11410', '(RFC822)'))


mail.logout()