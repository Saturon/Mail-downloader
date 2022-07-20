import smtplib

#Sending email

smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
smtpObj.starttls()
smtpObj.login('Example1@mail.ru','ExamplePassword')
smtpObj.sendmail("Example1@mail.ru","Example2@mail.ru","TextMessag")
smtpObj.quit()