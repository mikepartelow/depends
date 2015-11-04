# -*- coding: utf-8 -*-

from scapy.all import *
from ouimeaux.environment import Environment
import smtplib
import os, sys, json

# TODO:
# - rotated logging
# - document apt-get dependencies for Raspbian
# - better name for this file
# - consider making a Raspbian package (.deb?) for apt-get
# - discovery tool for creating the conf
#   - use depends(.sh) as entry point: depends discover; depends listen

button_switches = {}
email_switches = {}

with open("/opt/code/depends/gmail-creds") as f:
    GMAIL_USER, GMAIL_PASS = f.readlines()

class Email(object):
    def __init__(self, to_addr):
        self.to_addr = to_addr

    def send(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        r = server.login(GMAIL_USER, GMAIL_PASS) 

        headers = ["From: " + GMAIL_USER,
                   "Subject: A Message From Mike's Cottonelle Button",
                   "To: " + self.to_addr,
                   "MIME-Version: 1.0",
                   "Content-Type: text/plain; charset=\"UTF-8\"" ]
        headers = "\r\n".join(headers)

        msg = u"💩 Happens/happened."
        mail = headers.encode('UTF-8') + u"\r\n\r\n".encode('UTF-8') + msg.encode('UTF-8')
        server.sendmail(GMAIL_USER, self.to_addr, mail)
        server.quit()

def button_arp(pkt):
    if ARP in pkt and pkt[ARP].op == 1: #who-has (request)
        if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
            mac = pkt[ARP].hwsrc
            if mac in button_switches:
	        wemo = button_switches[mac]
		wemo.toggle()
            if mac in email_switches:
                email = email_switches[mac]
                email.send()

if len(sys.argv) < 2:
    print("Usage: {} <path to config file>".format(sys.argv[0]))
    sys.exit(1)

with open(sys.argv[1]) as conf:
    config = json.loads(conf.read())

env = Environment(with_subscribers=False)
env.start()
env.discover()
#env.wait(3)

found_wemos = False

for switch_name in env.list_switches():
    for entry in config:
        if switch_name == entry.get('wemo name'):
	    # FIXME: log
	    print("Found Wemo: {}".format(switch_name))
	    button_switches[entry['button mac']] = env.get(switch_name)
            found_wemos = True

for entry in config:
    if entry.get('email to'):
        email_switches[entry['button mac']] = Email(entry['email to'])

if found_wemos or email_switches:
    # FIXME: log
    print("Sniffing for: {}".format(", ".join(button_switches.keys() + email_switches.keys())))
    sniff(prn=button_arp, filter="arp", store=0)
else:
    print("Found no Wemos, exiting.")
