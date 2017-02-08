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
i = 0

print("Press Ctrl-C to quit")


while True:

	i = i + 1
	print("\n****************")
	print("*   LOOP : " + str(i) + "   *")
	print("****************")
	
	print("\nScanning Network...")
	nmap_output = subprocess.run(["nmap", "-sn", local_ip], stdout=subprocess.PIPE)
	print("Done")

	liste_ip = re.findall(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',str(nmap_output))

	liste_noms = re.findall(r'(?<=for\ )\w+',str(nmap_output))
	liste_noms.insert(0,'network')

	dat_dict = dict(zip(liste_noms, liste_ip))
	#print(dat_dict)


	if __name__ == "__main__":
		parser = argparse.ArgumentParser()
		parser.add_argument("--ip", default="127.0.0.1",
			help="The ip of the OSC server")
		parser.add_argument("--port", type=int, default=2002,
			help="The port the OSC server is listening on")
		args = parser.parse_args()

		client = udp_client.SimpleUDPClient(args.ip, args.port)
		
		print("\nSending to Usine...")
		for k, v in dat_dict.items():
			message = str("/")+str(k)+str(" ")+str(v)
			
			################################################
			
			# ici je ne suis pas sur de l'ordre des arguments de send_message
			# a toi de voir ce que tu preferes recevoir dans Usine
			# comment celle que tu n'utilise pas et tu me dira
			
			# 1 - la facon qu'on a testé hier
			client.send_message(message, random.random())
			
			# 2 - la facon qui fait + de sens
			#client.send_message("/NEWCOMER", message)
			
			#################################################
			
			#print(message)
			time.sleep(1)
		print("Done")
		
