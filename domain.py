#!/usr/bin/python3

import requests
import time
from twilio.rest import Client
import os
import sys


#VAR / DYNADOT
domain = "" #Your Domain which you want to register. // must be only lowercases.
currency = "EUR" #DYNADOT CURRENCY PRELOAD example: EUR, USD
dynadot_api_key = "" # DYNADOT API KEY
duration = "1" #How many years you want to register the domain.


#Request interval
req_interval = "11" #every X seconds. max 10 requests in 100 seconds. // minimum 10


#ENABLE / DISABLE Twilio
twilio_onoff = "1" # 1 is enable / 0 is disable

# VAR / Twilio SMS Delivery
account_sid = '' # Your Account SID
auth_token = '' # Your AUTH Token
messaging_service_SID_TW = '' #messaging_service_SID
phonenumber = '' #your verify phonenumber for SMS Delivery

# LOGFILE written in .txt
log = "1" # 1 is enable / 0 is disable
max_logsize = "50" #max filesize in MB.




while True:
    r = requests.get("https://api.dynadot.com/api3.xml?key=%s&command=register&domain=%s&duration=%s&currency=%s"%(dynadot_api_key,domain,duration,currency))

#Time Request
    status = r.text
    today = time.strftime('%d-%m-%Y', time.localtime())
    clock = time.strftime('%H:%M:%S', time.localtime())
    lastcheck = time.strftime('%H:%M:%S %d-%m-%Y', time.localtime())


#Buy Request
    if "<Status>not_available</Status>" in status: #NOT Available
        print("Domain is currently not available at %s %s "%(today,clock))
        os.system("rm -rf /var/www/html/index.html && cp ./index.html.BAK /var/www/html/index.html && sed -i 's/LastCheck: TEST/LastCheck: %s/g' /var/www/html/index.html"%lastcheck)
        #LOGFILE
        if "1" in log:
            logsize = os.path.getsize("./log.txt") / (1024*1024)
            if int(logsize) < int(max_logsize):
                log_in = "%s : Domain: %s \n %s \n \n ###### \n \n"%(lastcheck,domain,status)
                with open("log.txt", "a") as logfile:
                    logfile.write(log_in)
            else:
                os.system("rm -rf ./log.txt")
                log_in = "%s : Domain: %s \n %s \n \n ###### \n \n"%(lastcheck,domain,status)
                with open("log.txt", "a") as logfile:
                    logfile.write(log_in)

        elif "0" in log:
            os.system("rm -rf ./log.txt")
        time.sleep(int(req_interval))
        os.system("clear")





    elif "<Status>success</Status>" in status: #Available book the Domain.
        #LOGFILE
        if "1" in log:
            log_in = "%s : Domain: %s \n %s \n \n ###### \n \n"%(lastcheck,domain,status)
            with open("log.txt", "a") as logfile:
                logfile.write(log_in)
        elif "0" in log:
            os.system("rm -rf ./log.txt")

        #Twilio SMS Delivery
        if "1" in twilio_onoff:
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                                      messaging_service_sid='%s'%messaging_service_SID_TW,
                                      body='%s is registered now!'%domain,
                                      to='%s'%phonenumber
                                  )

            print(message.sid)

        elif "0" in twilio_onoff:
            print("")

        os.system("rm -rf /var/www/html/index.html && cp ./index.html.BAK /var/www/html/index.html && sed -i 's/LastCheck: TEST/LastCheck: %s \n\n Domain %s is now registered./g' /var/www/html/index.html"%(lastcheck,domain))
        time.sleep(int(req_interval))
        sys.exit()
