#import urllib2
import smtplib
import time
import os,sys
import requests
from bs4 import BeautifulSoup
#import pandas as pd
import logging
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


url_post = "https://www.mohfw.gov.in/"
toaddr = ["prateekd@xyz.net"]    #todo
err_list = []
fromaddr = "cockpit-covidtracker@xyz.com" #todo

def start_server():
    """Initializes a SMTP server to be used later.
    Arguements: None
    Returns: Server object"""
    server = ""
    logging.info("start_server")
    try:
	print("Initializing SMTP Server Client")
        logging.debug("Initializing SMTP Server Client")
        server = smtplib.SMTP(host = "xyz")

    except Exception as E:
        print("Exception in start_server")
        print (E)
        logging.info("Server Initialization failed")
        logging.debug(E)
        err_list.append("start_server:" + str(E))
    #log_list.append("start_server:" + str(server))
    return server

mail_server = start_server()

def send_mail(server,toaddr,subject,msg_text,mode):
    """Sends mail using the server based on the passed arguements.
    send_mail(server,toaddr,subject,msg_text)

        server: SMTP server
        toaddr: list of aliases or email-ids
        subject: string
        msg_text: plain-text"""
    logging.info("send_mail()")
    msg = MIMEMultipart()
    global fromaddr
    logging.debug("Parameters:"+ fromaddr + "," +str( toaddr )+"," + subject)
    msg['From'] = fromaddr
    msg['To'] = ",".join(toaddr)
    msg['Subject'] = subject
    msg.attach(MIMEText(msg_text,mode))
    try:
        logging.info("sending mail")
        print ("Send Email")
        server.sendmail(fromaddr,msg['to'].split(","),msg.as_string())
    except Exception as E:
        print ("Exception occured in send_mail")
        print (E)
    print ("Mail Sent")

    #log_list.append("send_mail:" + str(msg['From'])+" "+ str(msg['To']) + " " + str(msg['Subject']))

def get_num_covid_cases():
	session = requests.session()
	response = session.get(url_post, verify = False)
	r = session.get(url_post)
	#r = requests.post(url_post, headers={'User-Agent': 'Custom'})
	url_soup = BeautifulSoup(r.text, 'html.parser')
	a = url_soup.find_all('li', attrs={'class': 'bg-blue'})
	#cases = int(url_soup.find_all(['span'], attrs = {'class': 'icount'})[1].text.encode('utf-8'))
	for i in a:
		cases = int(i.find('strong').text.encode('utf-8'))
	return cases

if (__name__ == "__main__"):
	prev_cases = None
	inc = 0 
	while True:
		cases = get_num_covid_cases()
		send_mail(mail_server, toaddr, str('cockpit-alert: covidtracker'), "Hello, " "\n" " \n" " \nThe #covid-19 cases has been increased by " + str(inc) + " in the last 1hr." " current #cases: " + str(cases) + "\n" "\n" "--Thanks," " \n" "cockpit", 'plain')	
		if (bool(prev_cases)):
			if (prev_cases < cases):
				inc = cases - prev_cases
				#print("#cases current  : {}".format(cases))
				#print("#cases 1hr. bef : {}".format(prev_cases))
				#print("The covid-19 cases has been increased in the last 1 hr. by {}".format((cases - prev_cases)))
				send_mail(mail_server, toaddr, str('cockpit-alert: covidtracker'), "Hello, " "\n" " \n" " \nThe #covid-19 cases has been increased by " + str(inc) + " in the last 1hr." " current #cases: " + str(cases) + "\n" "\n" "--Thanks," " \n" "cockpit", 'plain')	
		prev_cases = cases
		time.sleep(60*60)
