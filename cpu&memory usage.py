from time import sleep
import psutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

def mailToUser(parameter, value):
    mail_content = 'Your ' + parameter +' load is higher then expected\n'+parameter+' load was around '+str(value)+' in the last 2 minutes'
    sender_address = 'XXXXXXX@XXXXXX.com'
    sender_pass = 'XXXXXXXXXXXXX'
    receiver_address = 'XXXXXXXX@XXXXX.com'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = parameter+' usage alert!'
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_UN and password

    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

def avg_limit_test(CPU_avg,memory_avg):
    load_limit = 95
    print CPU_avg
    print memory_avg

    if CPU_avg > load_limit and memory_avg > load_limit:
        mailToUser('CPU', CPU_avg)
        mailToUser('Memory', memory_avg)
        sys.exit()

    if CPU_avg > load_limit:
        mailToUser('CPU', CPU_avg)
        print 'GoodBy!!!'
        sys.exit()

    if memory_avg > load_limit:
        mailToUser('Memory', memory_avg)
        print 'GoodBy!!!'
        sys.exit()

secondsCounter = 1
interval_time = 120
CPU_counter = 0
memory_counter = 0

CPU_avg = 0
memory_avg = 0

while secondsCounter < interval_time:
    #get CPU utilization, Return a float representing the current system-wide CPU utilization as a percentage.
    CPU_usage = psutil.cpu_percent()
    print CPU_usage
    #get memory usage, usage calculated as (total - available) / total * 100
    memory_usage = dict(psutil.virtual_memory()._asdict())
    print memory_usage['percent']

    CPU_counter += CPU_usage
    CPU_avg = CPU_counter / secondsCounter
    memory_counter += float(memory_usage['percent'])
    memory_avg = memory_counter / secondsCounter

    secondsCounter += 1

    if secondsCounter == interval_time-1:
        avg_limit_test(CPU_avg, memory_avg)

        oneMinuteCounter = 1
        CPU_counter = 0
        memory_counter = 0
        CPU_avg = 0
        memory_avg = 0

    sleep(1)
