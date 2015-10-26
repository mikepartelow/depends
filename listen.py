from scapy.all import *
from ouimeaux.environment import Environment
import os, sys, json

# TODO:
# - rotated logging
# - document apt-get dependencies for Raspbian
# - better name for this file
# - consider making a Raspbian package (.deb?) for apt-get
# - discovery tool for creating the conf
#   - use depends(.sh) as entry point: depends discover; depends listen

button_switches = {}

def arp_display(pkt):
    if ARP in pkt and pkt[ARP].op == 1: #who-has (request)
        if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
            mac = pkt[ARP].hwsrc
            if mac in button_switches:
	        wemo = button_switches[mac]
		wemo.toggle()

if len(sys.argv) < 2:
    print("Usage: {} <path to config file>".format(sys.argv[0]))
    sys.exit(1)

with open(sys.argv[1]) as conf:
    config = json.loads(conf.read())

env = Environment()
env.start()
env.discover()
env.wait(3)

for switch_name in env.list_switches():
    for button_switch in config:
        if switch_name == button_switch['wemo name']:
	    # FIXME: log
	    print("Found Wemo: {}".format(switch_name))
	    button_switches[button_switch['button mac']] = env.get(switch_name)

# FIXME: log
print("Sniffing for: {}".format(", ".join(button_switches.keys())))

sniff(prn=arp_display, filter="arp", store=0)
