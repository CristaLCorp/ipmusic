# SHIT


import re
import subprocess
import socket

ip_locale = socket.gethostbyname(socket.gethostname())
#subnet_local = 
print("\n")
print(ip_locale)
print("\n")
#print(subnet_local)
print("\n")

nmap_output = subprocess.run(["nmap", "-sn", "192.168.2.0/24"], stdout=subprocess.PIPE)
print("\n")
print(nmap_output)
print("\n")

liste_ip = re.findall(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',str(nmap_output))
print("\n")
print('\n'.join(liste_ip))
print("\n")

liste_noms = re.findall(r'(?<=for\ )\w+',str(nmap_output))
liste_noms.insert(0,'network')
print("\n")
print('\n'.join(liste_noms))
print("\n")

dat_dict = dict(zip(liste_noms, liste_ip))
print(dat_dict)

