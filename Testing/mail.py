import smtplib
mailserver = smtplib.SMTP('smtp.office365.com',587)
mailserver.ehlo()
mailserver.starttls()
mailserver.login('soul_asset01@outlook.com', 'soulsvciot02')
#Adding a newline before the body text fixes the missing message body
mailserver.sendmail('soul_asset01@outlook.com','alertasset9@gmail.com','\npython email')
mailserver.quit()
