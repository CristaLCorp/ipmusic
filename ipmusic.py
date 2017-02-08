# SHIT


import re
import subprocess
import socket

import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client


#local_ip = "192.168.1.0/24"
local_ip = "192.168.2.0/24"
#network_mask = "255.255.255.0"

nmap_output = subprocess.run(["nmap", "-sn", local_ip], stdout=subprocess.PIPE)
#print("\n")
#print(nmap_output)
#print("\n")

liste_ip = re.findall(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',str(nmap_output))
#print("\n")
#print('\n'.join(liste_ip))
#print("\n")

liste_noms = re.findall(r'(?<=for\ )\w+',str(nmap_output))
liste_noms.insert(0,'network')
#print("\n")
#print('\n'.join(liste_noms))
#print("\n")

dat_dict = dict(zip(liste_noms, liste_ip))
print(dat_dict)



if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=2002,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

  #client.send_message(dat_dict, random.random())
  for x in range(10):
    client.send_message("/SHIT", random.random())
    time.sleep(1)