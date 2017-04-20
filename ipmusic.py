# IPMUSIC
# By CristaL
# V 0.4a
# 20/04/2017


import re
import subprocess
import socket
import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client


i = 0


# récuperation ip & network mask
ipconfig_output = subprocess.run(["ipconfig"], stdout=subprocess.PIPE)
m = re.findall(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}\\r\\n\ \ \ Passerelle par d\\x82faut\.\ \.\ \.\ \.\\xff\.\ \.\ \.\ \.\ \.\ :\ \d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}', str(ipconfig_output))
subnet_mask = re.findall(r'255\.\d{0,3}\.\d{0,3}\.\d{0,3}', str(m))
subnet_mask = str(subnet_mask[0])
subnet_mask = sum([bin(int(x)).count("1") for x in subnet_mask.split(".")])
network = re.findall(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.', str(m))
network = str(network[1]) + '0/' + str(subnet_mask)


while True:
	

	i = i + 1
	print("\n****************")
	print("*   LOOP : " + str(i) + "   *")
	print("****************")
	
	# launching nmap quick scan
	print("\nScanning Network " + network + " ...")
	nmap_output = subprocess.run(["nmap", "-sn", network], stdout=subprocess.PIPE)
	print("Done")
	
	# regex nmap output to retrieve ip addresses
	liste_ip = re.findall(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',str(nmap_output))
	
	# retire le premier element de la liste (le network)
	liste_ip.pop(0)
	
	# compte combien de personnes sont connectées, basé sur la longueur de la liste d ip
	nbrgens = len(liste_ip)
	

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
			print("sending ip : ", str(k))
			client.send_message("/IPS", str(k))
			
			# ping l ip puis envoie le ping correspondant à l ip
			dat_ping = subprocess.run(["ping", "-n", "1", "-w", "300", k], stdout=subprocess.PIPE)
			dat_ping = re.findall(r'temps=\d{1,3}', str(dat_ping))
			dat_ping = re.findall(r'\d{1,3}', str(dat_ping))
			
			try :
				client.send_message("/PING", dat_ping[0])
				print("ping : "+ dat_ping[0] + "ms\n")
			except :
				print("can't ping or < 1ms \n")
			
			
			#message = str(k)
					
			#client.send_message("/IPS", message)
			
			
			time.sleep(3)
		print("\nDone")
		
		
		
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