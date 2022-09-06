from datetime import date
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from player import Player


class PlayerEmail:

    def __init__(self, header, senderinfo, players):
        self.header = header
        self.players = players
        self.senderinfo = senderinfo

    def sendEmail(self):
        smtpObj = smtplib.SMTP("smtp.gmail.com", 587) #Создание объекта SMTP
        smtpObj.starttls()  #Шифрование

        from_addr = "example@gmail.com" #Адрес отправителя
        to_addr =  "example@yandex.ru" #Адрес получателя
        smtpObj.login(from_addr,"Insert your 16-signed code") #Вход в аккаунт почты, используя 16-значный код


        #Сообщение
        msg = MIMEMultipart()
        msg["Subject"] = self.header #Тема



        try:
            msg.attach(MIMEText(f"{self.senderinfo}\n", 'plain'))

            text = ''
            for player in self.players:
                #текст
                if player.z_type == 'Заявка':
                    text = f"\n{player.z_type}\n{player.fio}\n{player.birthday}\n{player.position}\n"
                    msg.attach(MIMEText(text, 'plain'))
                    #фото
                    part = MIMEBase('application', 'octet-stream')
                    with open(player.photo, "rb") as photo:
                        part.set_payload(photo.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', f"{player.fio.replace(' ', '_')}.jpg"))
                    msg.attach(part)
                else:
                    text = f"\n{player.z_type}\n{player.fio}\n"
                    msg.attach(MIMEText(text, 'plain'))
        except:
            print("Error")
                
        smtpObj.sendmail(from_addr, to_addr, msg.as_string()) #Отправка
        smtpObj.quit() #Выход

        print("successfully sent email to %s:" % (to_addr))
        

class RegularEmail:
    def __init__(self, header, body, attachments):
        self.header = header
        self.body = body
        self.attachments = attachments
        
    def sendEmail(self):
        smtpObj = smtplib.SMTP("smtp.gmail.com", 587) #Создание объекта SMTP
        smtpObj.starttls()  #Шифрование

        from_addr = "alekseilapchik2001@gmail.com" #Адрес отправителя
        to_addr =  "ithideout@yandex.ru" #Адрес получателя
        smtpObj.login(from_addr,"unihqmxleirxkwxm") #Вход в аккаунт почты, используя 16-значный код
  
        msg = MIMEMultipart()
        #Тема
        msg["Subject"] = self.header 
              
        try:
            #Сообщение
            text = self.body
            msg.attach(MIMEText(text, 'plain'))
            #Вложения
            part = MIMEBase('application', 'octet-stream')
            for attachment in self.attachments:
                with open(attachment, "rb") as doc:
                    part.set_payload(doc.read())
                encoders.encode_base64(part)
                if attachment.startswith("images"):
                    part.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', f"{datetime.now().strftime('%d%m%Y%H%M%S')}.jpg"))  
                else:
                    part.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', str(attachment).replace("docs/", "")))
                msg.attach(part)
        except:
            print("Error")
        smtpObj.sendmail(from_addr, to_addr, msg.as_string()) #Отправка
        smtpObj.quit() #Выход

        print("successfully sent email to %s:" % (to_addr))