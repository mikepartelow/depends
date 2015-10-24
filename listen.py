from scapy.all import *
import os

# TODO:
# - read config file
# - rotated logging
# - try using wemo APIs
# - document apt-get dependencies for Raspbian
# - either remove path dependencies or make an installer that alters them
# - better name for this file

WEMO='wemo'

class WemoSwitch(object):
    ON  = 'on'
    OFF = 'off'

    def __init__(self, name):
        self.name = name

    def status(self):
        status_all = os.popen("{} status".format(WEMO)).read()
        for line in status_all.splitlines():
            if self.name in line:
                if '1' in line:
                    return self.ON
                elif '0' in line:
                    return self.OFF

    def turn_on(self):
        os.popen("{} switch '{}' on".format(WEMO, self.name)).read()

    def turn_off(self):
        os.popen("{} switch '{}' off".format(WEMO, self.name)).read()

    def toggle(self):
        my_status = self.status()
        if my_status is self.ON:
            self.turn_on()
        elif my_status is self.OFF:
            self.turn_off()
    

BUTTONS_FOR_WEMO_SWITCHES = {
    '74:75:48:37:8e:c9' : WemoSwitch('Living Room Torch'),
}

def arp_display(pkt):
  if ARP in pkt and pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      mac = pkt[ARP].hwsrc
      if mac in BUTTONS_FOR_WEMO_SWITCHES:
          wemo = BUTTONS_FOR_WEMO_SWITCHES[mac]
          wemo.toggle()


mac = '74:75:48:37:8e:c9'
if mac in BUTTONS_FOR_WEMO_SWITCHES:
    wemo = BUTTONS_FOR_WEMO_SWITCHES[mac]
    wemo.toggle()

# sniff(prn=arp_display, filter="arp", store=0)

