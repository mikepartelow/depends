from scapy.all import *
import os


def toggle_switch(switch_name):
    status = os.popen("venv.depends/bin/wemo status").read()
    switch_status = None
    for line in status.splitlines():
        if switch_name in line:
            if '1' in line:
                switch_status = 'on'
            elif '0' in line:
                switch_status = 'off'
        else:
            print("nope: {}".format(line.strip()))

    if switch_status == 'on':
        os.popen("venv.depends/bin/wemo switch '{}' off".format(switch_name)).read()
    elif switch_status == 'off':
        os.popen("venv.depends/bin/wemo switch '{}' on".format(switch_name)).read()
    else:
        print("found no status for {}".format(switch_name)) 

def arp_display(pkt):
  print("arp")
  if pkt[ARP].op == 1: #who-has (request)
    print("arp1")
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      print("arp2")
      if pkt[ARP].hwsrc == '74:75:48:37:8e:c9':
          print("depend")
          toggle_switch('Living Room Torch')
      else:
        print "ARP Probe from unknown device: " + pkt[ARP].hwsrc


sniff(prn=arp_display, filter="arp")
