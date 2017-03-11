# IPMUSIC
# By CristaL
# V 0.2a
# 11/03/2017


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
	
	# launching nmap quick scan
	print("\nScanning Network...")
	nmap_output = subprocess.run(["nmap", "-sn", local_ip], stdout=subprocess.PIPE)
	print("Done")
	
	# regex nmap output to retrieve ip addresses
	liste_ip = re.findall(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',str(nmap_output))
	
	# print(liste_ip)
	
	# retire le premier element de la liste (le network)
	liste_ip.pop(0)
	
	# compte combien de personnes sont connectées, basé sur la longueur de la liste d ip
	nbrgens = len(liste_ip)
	#print(nbrgens)

	"""
	# commenté jusqu a ... plus tard
	# nmap ne retournant pas toujours le nom netbios des hosts
	# suivant quel ordi effectue le scan
	
	# regex nmap output to retrieve names
	liste_noms = re.findall(r'(?<=for\ )\w+',str(nmap_output))
	# add "network" on top of name list
	liste_noms.insert(0,'network')

	# make a dictionnary by combining names and ips
	dat_dict = dict(zip(liste_noms, liste_ip))
	#print(dat_dict)
	# get the total numer of connected device by getting the length of the dictionnary
	nbrgens = len(dat_dict.items())
	"""

	if __name__ == "__main__":
		parser = argparse.ArgumentParser()
		parser.add_argument("--ip", default="127.0.0.1",
			help="The ip of the OSC server")
		parser.add_argument("--port", type=int, default=2002,
			help="The port the OSC server is listening on")
		args = parser.parse_args()

		client = udp_client.SimpleUDPClient(args.ip, args.port)
		
		print("\nSending to Usine...")
		
		# envoie le nombre de personne connectées 1 fois
		client.send_message("/NBRGENS", int(nbrgens))
		print("\nNombre de personnes connectees : ", nbrgens, "\n")
		
		# for k, v in dat_dict.items():
		for k in liste_ip:
			
			# envoie, a chaque tour de boucle, [ip] d'un client different
			message = str(k)
					
			client.send_message("/IPS", message)
			
			print(message)
			time.sleep(3)
		print("\nDone")
		
