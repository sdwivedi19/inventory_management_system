######### app password= tseowxiqnkausqux ##########
# for sending emails there are two methods -
# 1. less secure app in gmail (won't work if you have done two step verification & also it's not secure for your account)
# 2. generate an app password for gmail so that you dont have to reveal your actual password anywhere

import smtplib      #SMTP library
import time

class Email_Otp:
    def __init__(self, email_to, otp):
        #(host,port) #gmail works at 587 port, we can search it on web
        self.s=smtplib.SMTP('smtp.gmail.com',587)   #object of smtplib calling SMTP function of smtplib library
        self.s.starttls()   #encryption of email #important so that third party can't read our email

        email_from = 'sudhansudwivedi1999@gmail.com'  # email through which you want to send the otp to the user
        pass_ = 'tseowxiqnkausqux'

        self.s.login(email_from,pass_)

        subject='IMS: Reset Password OTP'
        msg=f'Dear Sir/Madam,\n\nYour Reset OTP is {str(otp)}.\n\nWith Regards,\nIMS Team'
        msg="Subject:{}\n\n{}".format(subject,msg)
        self.s.sendmail(email_from,email_to,msg)

        #==to check whether the email is delivered====
        self.chk = self.s.ehlo()
        self.email_send_status()

    def email_send_status(self):
        if self.chk[0]==250:
            return 's'
        else:
            return 'f'

