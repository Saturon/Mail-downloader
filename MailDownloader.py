#Данная программа скачивает все сообщения вашей почты вам на пк и переносит их в папку скачаное


import imaplib
import email
import hashlib
import email.message
import time
import os.path
import subprocess
import re
import sys

imaplib._MAXLINE = 1000000
server = 'imap.mail.ru'
login = "******@mail.ru"
pause_time = 30
password = '*****password'


def main_loop_proc():
    print("Подключение к {}...".format(server))
    imap = imaplib.IMAP4_SSL(server)
    print("Идет подключение! Логин: {}...".format(login));
    imap.login(login, password)
    print("Мы подключенны! Собираем сообщения...");
    status, select_data = imap.select('INBOX')
    nmessages = select_data[0].decode('utf-8')
    status, search_data = imap.search(None, 'ALL')
    
    if b'() "/" "Downloaded"' not in imap.list()[1]:
        print("Папки Downloaded не существовало, перезапустите программу", file = sys.stderr)
        imap.create("Downloaded")
        imap.logout()
        sys.exit(1)
  
    for msg_id in search_data[0].split():
        msg_id_str = msg_id.decode('utf-8')
        print("Скачиваю сообщение {} of {}".format(msg_id_str,
                                                 nmessages))
        status, msg_data = imap.fetch(msg_id, '(RFC822)')
        msg_raw = msg_data[0][1]
        msg = email.message_from_bytes(msg_raw,
            _class = email.message.EmailMessage)
        # mailing_list = msg.get('X-Mailing-List', 'undefined')
        mailing_list = msg.get('List-Id', 'Saving') #'undefined'
        mailing_list = re.sub('^(?s).*?<([^>]+?)(?:\\..*?)>.*$',
                              '\\1', mailing_list)
        timestamp = email.utils.parsedate_tz(msg['Date'])
        year, month, day, hour, minute, second = timestamp[:6]
        msg_hash = hashlib.sha256(msg_raw).hexdigest()[:16]
        fname = ("./archive/" +
                 "{0:04}-{1:02}-{2:02}-{3:02}-{4:02}-{5:02}" +
                 "-{6}.txt").format(
            year, month, day, hour, minute, second,
            msg_hash, mailing_list)
        dirname = os.path.dirname(fname)
        print("Сохраняю сообщение {} В файл {}".format(msg_id_str, fname))
        subprocess.call('mkdir -p {}'.format(dirname), shell=True)
        with open(fname, 'wb') as f:
            f.write(msg_raw)
        apply_lbl_msg = imap.uid('COPY', msg_id, "Downloaded")  ### Тут происходит копирование файла и последующие удаление его из директории
        if apply_lbl_msg[0] == 'OK':
            mov, data = imap.uid('STORE', msg_id , '+FLAGS', '(\Deleted)')
            print("Успешно перенес ", msg_id, "в папку Downloaded")
            imap.expunge()
    imap.logout()       

while True:
    try:
        main_loop_proc()
    except Exception as e:
        print("ERROR:" + str(e))
    print("Sleeping {} seconds...".format(pause_time))
    time.sleep(pause_time)