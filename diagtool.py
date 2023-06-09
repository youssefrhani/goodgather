#Vous devez utiliser python (3.10) ou une version plus récente
#car le code est construit avec L'instruction match / case (Python 3.10)
#ce script est compatible avec les systèmes d'exploitation linux et windows
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
import psutil
from reportlab.pdfgen import canvas
import datetime
import colorama

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
        print(colorama.Fore.GREEN +'1- diagnostic du réseau\n2- diagnostic du système\n3- créer un rapport PDF sur l\'état de votre machine')
        print(colorama.Fore.RED + '9- Quiter')   
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
            elif option == 2:
                while True:
                    os.system('clear')
                    print('1- utilisation de la CPU')
                    print('2- utilisation du RAM')
                    print('3- détails du disque')
                    print('4- Task Manager (vue générale )')
                    print('0- retour')

                      
                    sysch = int(input())
                    match sysch:
                        case 1:
                            print('////////////////////////////////')
                            for _ in range(10):
                                cpu = psutil.cpu_percent(interval=0.2)
                                print(f"CPU : {cpu}%")
                            input('\n"entrer" pour continue...')
                        case 2:
                            print('////////////////////////////////')
                            ram_usage = psutil.virtual_memory().percent
                            print(f"RAM : {ram_usage}%")
                            input('\n"entrer" pour continue...')
                        case 4:
                            print('F10 pour quitter...')
                            time.sleep(1.5)
                            os.system('htop')
                        case 3:
                            os.system('df -h')
                            input('\n"entrer" pour continue...')
                        case 0:
                            break
            elif option == 3:
                def get_cpu_utilis():
                    cpu_utilis = psutil.cpu_percent(interval=0.5)
                    return cpu_utilis

                def get_ram_utilis():
                    ram = psutil.virtual_memory()
                    ram_utilis = ram.percent
                    return ram_utilis

                def get_disk_utilis():
                    df_output = subprocess.run(['df', '-h'], capture_output=True, text=True)
                    disk_utilis = df_output.stdout
                    return disk_utilis

                def check_firewall_status():
                    firewall_status = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
                    return firewall_status.stdout

                def get_mac():
                    output = subprocess.check_output(["ifconfig"])
                    output = output.decode() 
                    pattern = r"ether\s([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})"
                    mac = re.findall(pattern, output)
                    return mac


                def rapport_pdf(cpu_utilis, ram_utilis, disk_utilis, firewall_status, user, ipv4, mac):
                    x = datetime.datetime.now()
                    format_date = x.strftime("%Y-%m-%d_%H:%M")
                    rapport_name = f'rapport_{format_date}_{user}.pdf'
                    c = canvas.Canvas(rapport_name)
                    c.setFont('Courier', 16)
                    c.drawString(50, 800, 'Rapport de   :')
                    c.setFont('Courier', 14)
                    c.drawString(50, 775, f'Utilisateur : {user}')
                    c.drawString(255, 775, f'Machine : {machine}')
                    c.drawString(50, 750, f'à : {date}')
                    c.drawString(50, 740, '------------------------------------------------------------------')

                    c.drawString(50, 715, f'IPV4 Local : {ipv4}')
                    c.drawString(50, 690, f'Adresse MAC : {mac}')
                    c.drawString(50, 665, 'Firewall Status:')
                    c.setFont('Courier', 10)
                    c.drawString(50, 645, firewall_status)

                    c.setFont('Courier', 14)
                    c.drawString(50, 615, f'CPU utilis: {cpu_utilis}%')
                    c.drawString(50, 590, f'RAM utilis: {ram_utilis}%')
                    c.drawString(50, 565, 'Disk utilis:')
                    c.setFont('Courier', 10)
                    disk_utilis_lines = disk_utilis.split('\n')
                    y = 540
                    for line in disk_utilis_lines:
                        c.drawString(50, y, line)
                        y -= 15
                    c.save()
                    print(f'rapport généré: {rapport_name}')
                    input('\n"entrer" pour continue...')

                cpu_utilis = get_cpu_utilis()
                ram_utilis = get_ram_utilis()
                disk_utilis = get_disk_utilis()
                firewall_status = check_firewall_status()
                user = os.popen('whoami').read().strip()
                machine = os.popen('hostname').read().strip()
                date = os.popen('date').read().strip()
                ipv4 = os.popen('hostname -I').read().strip()
                mac = get_mac()


                rapport_pdf(cpu_utilis, ram_utilis, disk_utilis, firewall_status, user, ipv4, mac)

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
        print(colorama.Fore.GREEN +'1- diagnostic du réseau\n2- diagnostic du système\n3- créer un rapport PDF sur l\'état de votre machine')
        print(colorama.Fore.RED +'9- Quiter')   

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
                while True:
                    os.system('cls')
                    print('1- utilisation de la CPU')
                    print('2- utilisation du RAM')
                    print('3- détails du disque')
                    print('0- retour')

                    sysch = int(input())
                    match sysch:
                        case 1:
                            print('////////////////////////////////')
                            for _ in range(10):
                                cpu = psutil.cpu_percent(interval=0.2)
                                print(f"CPU : {cpu}%")
                            input('\n"entrer" pour continue...')
                        
                        case 2:
                            print('////////////////////////////////')
                            ram_usage = psutil.virtual_memory().percent
                            print(f"RAM : {ram_usage}%")
                            input('\n"entrer" pour continue...')
                        case 3:
                            print('////////////////////////////////')
                            os.system('wmic logicaldisk get caption')
                            drive = input('Enter your drive letter: ')

                            disk_usage = psutil.disk_usage(drive + ':/') 

                            print(f"Total: {disk_usage.total / (1024 ** 3):.2f} GB")
                            print(f"Utilsé: {disk_usage.used / (1024 ** 3):.2f} GB")
                            print(f"Libre: {disk_usage.free / (1024 ** 3):.2f} GB")
                            print(f"Pousentage: {disk_usage.percent}%")
                            input('\n"entrer" pour continue...')
                        case 0:
                            break


            elif option == 3:
                def get_cpu_utilis():
                    cpu_utilis = psutil.cpu_percent(interval=0.5)
                    return cpu_utilis

                def get_ram_utilis():
                    ram = psutil.virtual_memory()
                    ram_utilis = ram.percent
                    return ram_utilis

                def get_disk_usage():
                    drive = psutil.disk_partitions()[0].device.split(':')[0]
                    disk_usage = psutil.disk_usage(drive + ':/')
                    total = disk_usage.total / (1024 ** 3)
                    utilisé = disk_usage.used / (1024 ** 3)
                    libre = disk_usage.free / (1024 ** 3)
                    pourcentage = disk_usage.percent

                    return f"Lecteur : {drive}\nTotal: {total:.2f} GB\nUtilisé: {utilisé:.2f} GB\nLibre: {libre:.2f} GB\nPourcentage: {pourcentage}%"


                def check_firewall_status():
                    firewall_output = subprocess.run(['netsh', 'advfirewall', 'show', 'currentprofile'], capture_output=True, text=True)
                    firewall_status = firewall_output.stdout
                    return firewall_status

                def get_ipv4():
                    ipconfig_output = subprocess.check_output(['ipconfig'], text=True)
                    lines = ipconfig_output.split('\n')
                    for line in lines:
                        if 'IPv4 Address' in line:
                            ipv4_address = line.split(':')[-1].strip()
                            return ipv4_address
                    return None


                def rapport_pdf(cpu_utilis, ram_utilis, disk_utilis, user, ipv4, ipp, firewall_status):
                    x = datetime.datetime.now()
                    format_date = x.strftime("%Y-%m-%d_%H-%M")
                    rapport_name = (f'rapport_{format_date}.pdf')
                    c = canvas.Canvas(rapport_name)
                    c.setFont('Courier', 16)
                    c.drawString(50, 800, 'Rapport de   :')
                    c.setFont('Courier', 14)
                    c.drawString(50, 775, f'Utilisateur : {user}')

                    c.drawString(50, 750, f'à : {date}')
                    c.setFont('Courier', 10)
                    c.drawString(50, 740, '------------------------------------------------------------------')
                    c.setFont('Courier', 14)
                    c.drawString(50, 715, f'IPV4 Local : {ipv4}')
                    c.drawString(50, 690, f'Adresse IP Publique : {ipp}')
                    c.setFont('Courier', 14)
                    c.drawString(50, 665, f'utilisation CPU: {cpu_utilis}%')
                    c.drawString(50, 640, f'utilisation RAM: {ram_utilis}%')
                    c.drawString(50, 615, 'Détails du disque :')
                    c.setFont('Courier', 10)
                    disk_utilis_lines = disk_utilis.split('\n')
                    y = 590
                    for line in disk_utilis_lines:
                        c.drawString(60, y, line)
                        y -= 15
                    c.setFont('Courier', 14)
                    c.drawString(50, 450, 'firewall status')
                    c.setFont('Courier', 10)
                    firewall_status_lines = firewall_status.split('\n')
                    y = 430
                    for line in firewall_status_lines:
                        c.drawString(50, y, line)
                        y -= 15
                    c.save()
                    print(f'rapport généré : {rapport_name}')

                cpu_utilis = get_cpu_utilis()
                ram_utilis = get_ram_utilis()
                disk_details = get_disk_usage()
                firewall_status = check_firewall_status()
                user = os.popen('whoami').read().strip()
                date = os.popen('date /T').read().strip()
                ipv4 = get_ipv4()
                ipp = os.popen('curl ifconfig.me').read().strip()


                rapport_pdf(cpu_utilis, ram_utilis, disk_details, user, ipv4, ipp, firewall_status)
                input('\n"entrer" pour continue...')           
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
    print('Désolé,',username, ' nous ne prenons pas en charge ', ops)