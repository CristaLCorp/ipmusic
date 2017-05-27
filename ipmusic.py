# IPMUSIC
# By CristaL
# V 0.5b
# 27/05/2017


import re
import subprocess
import socket
import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client



def fct_ping(ip):
    dat_ping = subprocess.run(["ping", "-n", "1", "-w", "300", ip], stdout=subprocess.PIPE)
    dat_ping = re.findall(r'temps=\d{1,3}', str(dat_ping))
    dat_ping = re.findall(r'\d{1,3}', str(dat_ping))
    try :
        print("ping : "+ str(dat_ping[0]) + "ms\n")
        return dat_ping[0]
    except :
        print("can't ping or < 1ms \n")
        return 1
    
def find_net():
    # recuperation ip & network mask
    ipconfig_output = subprocess.run(["ipconfig"], stdout=subprocess.PIPE)
    m = re.findall(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}\\r\\n\ \ \ Passerelle par d\\x82faut\.\ \.\ \.\ \.\\xff\.\ \.\ \.\ \.\ \.\ :\ \d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}', str(ipconfig_output))
    subnet_mask = re.findall(r'255\.\d{0,3}\.\d{0,3}\.\d{0,3}', str(m))
    subnet_mask = str(subnet_mask[0])
    subnet_mask = sum([bin(int(x)).count("1") for x in subnet_mask.split(".")])
    network = re.findall(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.', str(m))
    network = str(network[1]) + '0/' + str(subnet_mask)
    
    return {'subnet_mask':subnet_mask, 'network':network}

def nmap_shit(subnet_mask, network):
    # launching nmap quick scan
    print("\nScanning Network " + network + " ...")
    nmap_output = subprocess.run(["nmap", "-sn", network], stdout=subprocess.PIPE)
    print("Done")

    # regex nmap output to retrieve ip addresses
    liste_ip = re.findall(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',str(nmap_output))

    # retire le premier element de la liste (le network)
    liste_ip.pop(0)

    # compte combien de personnes sont connectees, base sur la longueur de la liste d ip
    nbrgens = len(liste_ip)
    
    return {'liste_ip':liste_ip, 'nbrgens':nbrgens}

def big_loop(subnet_mask, network, usines):
    
    i = 0
    
    while True:  
    
        i = i + 1
        print("\n****************")
        print("*   LOOP : " + str(i) + "   *")
        print("****************")
        
        results = nmap_shit(subnet_mask, network)
        liste_ip = results['liste_ip']
        nbrgens = results['nbrgens']
        port = 2002
        server_osc = []
        
        # creation du client ip + port = boucle longueur liste des ips
        for bite in range(len(usines)):
            server_osc.append(udp_client.SimpleUDPClient(usines[bite], port))
            
        # boucle pour envoyer le nombre de mecs sur le reseau a autant de client usine
        print("\nSending to Usine...")
        for bite in range(len(usines)):
            # envoie le nombre de personne connectees 1 fois
            server_osc[bite].send_message("/NBRGENS", int(nbrgens))
        print("\nNombre de personnes connectees : ", nbrgens, "\n")

        
        # for k, v in dat_dict.items():
        for ip in liste_ip:

            # envoie, a chaque tour de boucle, [ip] d'un client different
            print("sending ip : ", str(ip))
            for bite in range(len(usines)):
                server_osc[bite].send_message("/IPS", str(ip))

            # ping l ip puis envoie le ping correspondant a l ip
            ping_time = fct_ping(ip)

            for bite in range(len(usines)):
                server_osc[bite].send_message("/PING", str(ping_time))
                    
            time.sleep(3)
        print("\nDone")
    


def main():
    
    nbr_usines = input("Combien d'Usines ? ")
    
    try :
        nbr_usines = int(nbr_usines)
    except :
        print("un nombre on t'a dit !")
        sys.exit(0)
        
    usines = []
    for i in range(nbr_usines):
        ip_usine = input("ip de l'Usine n" + str(i+1) + ": ")
        if not 8 <= len(ip_usine) <= 15 :
            print("Mauvais format ip")
            sys.exit(0)
        else :
            #print(i)
            usines.append(ip_usine)        
    
    #print(usines)
    #print(usines[0])
    #print(len(usines))
    
    result = find_net()
    subnet_mask = result['subnet_mask']
    network = result['network']
    
    big_loop(subnet_mask, network, usines)
    
    

# lancement du programme
main()




# les trucs enleves :

#if __name__ == "__main__":

# deal with args...
#parser = argparse.ArgumentParser()
#parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
#parser.add_argument("--port", type=int, default=2002, help="The port the OSC server is listening on")
#args = parser.parse_args()
