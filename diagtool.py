import platform
import getpass
import time
import os
import subprocess
import re
from requests import get
import speedtest
import sys
from halo import halo


ops = platform.system()
username = getpass.getuser()

#LINUX PART
if ops == 'Linux':  
    
    os.system('clear')
    print('Hello', username, '\nOS:', ops)
    print('\n')
    time.sleep(2)

    while True:
        os.system('clear')
        print('1- diagnostic du réseau\n2- diagnostic du système')
        print('9- Quiter')   

        try:
            option = int(input())
            if option == 1:
                while True:
                    os.system('clear')
                    print('1- Afficher les adresses IPv4 Privé')
                    print('2- Afficher les adresses IPv4 Publique')
                    print('3- Afficher MAC adresse')
                    print('4- Tester La vitesse de connexion')
                    print('5- Les Ports ouverts')
                    print('0- retour')
                    try:
                        digch = int(input())
                        match digch:
                            case 1:
                                print('////////////////////////////////')

                                output = subprocess.check_output(["ifconfig"]).decode()
                                interfaces = re.findall(r"^([a-zA-Z-0-9]+):", output, flags=re.MULTILINE)
                                ipv4 = re.findall(r"inet (\d+\.\d+\.\d+\.\d+)", output)
                        
                                print("interface\tIPv4 Adresse")
                                for interface, adresse in zip (interfaces, ipv4):
                                    print (f"{interface}\t{adresse}")

                                input('\n"entrer" pour continue...')
                            case 2:

                                print('////////////////////////////////')
                                ip = get('https://api.ipify.org').content.decode('utf8')
                                print('IPv4 Publique est : {}'.format(ip))

                                input('\n"entrer" pour continue...')
                            case 3:
                                print('////////////////////////////////')
                                output = subprocess.check_output(["ifconfig"])
                                output = output.decode() 

                                pattern = r"ether\s([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})"
                                matches = re.findall(pattern, output)

                                for match in matches:
                                    print(match)
                                input('\ntapper "entrer" pour continue...')

                            case 4:
                              while True:
                                print('////////////////////////////////')
                                print('cela prend quelques secondes...')
                                stop = input('\ntapper "entrer" pour continue, Ou "c" pour annuler:')
                                if stop == 'c' :
                                    break
                                else :
                                
                                    spinner = halo.Halo(text='Chargement', spinner='dots')
                                    spinner.start()
                                    speedtester = speedtest.Speedtest()
                                    bestserver = speedtester.get_best_server()
                                    downspeed = speedtester.download()
                                    upspeed = speedtester.upload()
                                    downspeed_mbs = downspeed / 1000000
                                    upspeed_mbs = upspeed / 1000000
                                    spinner.stop()
                        
                                    print(f"\nvitesse de téléchargement : {downspeed_mbs: .2f} Mo/s")
                                    print(f"vitesse Upload : {upspeed_mbs: .2f} Mo/s")

                                input('\n"entrer" pour continue...')
                            
                            case 5:
                                print('////////////////////////////////')
                                print('\nLes ports overts pour localhost :')
                                os.system('netstat -tuln')
                                input('\n"entrer" pour continue...')

                            case 0:
                                break
                    except ValueError:
                        print('veuillez saisir un numéro')
                        input('OK?')  
            elif option ==2:
                print('you chose 2')
            elif option ==9:
                print('Bye...')
                time.sleep(1)
                break
             
            else :
                print('Choix incorrect, ')
                time.sleep(1)
                os.system('clear')
            
        except ValueError:
            print('veuillez saisir un numéro')
            input('OK?')       
        
        
#WINDOWS PART
elif ops == 'Windows':
    os.system('cls')
    print('Hello', username, '\nOS:', ops)
    print('\n')
    time.sleep(2)


    while True:
        os.system('cls')
        print('1- diagnostic du réseau\n2- diagnostic du système')
        print('9- Quiter')   

        try:
            option = int(input())
            if option == 1:
                while True:
                    os.system('cls')
                    print('1- Afficher les adresses IPv4 Privé')
                    print('2- Afficher les adresses IPv4 Publique')
                    print('3- Afficher MAC adresse')
                    print('4- Tester La vitesse de connexion')
                    print('5- Les Ports ouverts')
                    print('0- retour')
                    try:
                        digch = int(input())
                        match digch:
                            case 1:
                                print('////////////////////////////////')

                                os.system('netsh interface ipv4 show addresses')

                                input('\n"entrer" pour continue...')
                            case 2:

                                print('////////////////////////////////')
                                ip = get('https://api.ipify.org').content.decode('utf8')
                                print('IPv4 Publique est : {}'.format(ip))

                                input('\n"entrer" pour continue...')
                            case 3:
                                print('////////////////////////////////')
                                
                                os.system('getmac')

                                input('\ntapper "entrer" pour continue...')

                            case 4:
                             while True:
                                print('////////////////////////////////')
                                print('cela prend quelques secondes...')
                                stop = input('\ntapper "entrer" pour continue, Ou "c" pour annuler:')
                                if stop == 'c' :
                                    break
                                else :
                                
                                    spinner = halo.Halo(text='Chargement', spinner='dots')
                                    spinner.start()
                                    speedtester = speedtest.Speedtest()
                                    bestserver = speedtester.get_best_server()
                                    downspeed = speedtester.download()
                                    upspeed = speedtester.upload()
                                    downspeed_mbs = downspeed / 1000000
                                    upspeed_mbs = upspeed / 1000000
                                    spinner.stop()
                        
                                    print(f"\nvitesse de téléchargement : {downspeed_mbs: .2f} Mo/s")
                                    print(f"vitesse Upload : {upspeed_mbs: .2f} Mo/s")

                                input('\n"entrer" pour continue...')
                            
                            case 5:
                                print('////////////////////////////////')
                                print('\nLes ports overts pour localhost :')
                                print('\n')
                                os.system('netstat -aon | findstr "LISTENING')
                                input('\n"entrer" pour continue...')

                            case 0:
                                break
                    except ValueError:
                        print('veuillez saisir un numéro')
                        input('OK?')  
            elif option ==2:
                print('you chose 2')
            elif option ==9:
                print('Bye...')
                time.sleep(1)
                break
             
            else :
                print('Choix incorrect, ')
                time.sleep(1)
                os.system('clear')
            
        except ValueError:
            print('veuillez saisir un numéro')
            input('OK?')  

else :
    print('sorry',username, 'we do not support ', ops)