from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from datetime import datetime
import colorama
import time

with open('cisco_ip_list.txt') as f:
    device_list = f.read().splitlines()

STARTTIME = datetime.now()

for devices in device_list:
    if devices.strip().startswith('#'):
        # re-inicia el loop al detectar el simbolo de numeral
        continue
    print('------------------------------------------------')
    print(colorama.Fore.WHITE + 'Conectando al dispositivo con ip: ' + devices)
    ip_address = devices
    router = {
        'device_type': 'cisco_nxos',
        'ip': ip_address,
        'username': 'admin',
        'password': 'Admin_1234!',
        'port': '8181'
    }

    timestr = time.strftime("%Y%m%d%H%M")

    try:
        net_connect = ConnectHandler(**router)
    except (AuthenticationException):
        print(colorama.Fore.RED + 'Error de autenticacion')
        continue
    except (NetMikoTimeoutException):
        print(colorama.Fore.RED + 'El dispositivo es inalcanzable o se encuentra apagado')
        continue
    except (EOFError):
        print('End of file while attempting device ' + ip_address)
        continue
    except (SSHException):
        print('Problema con SSH. Estas seguro de que SSH esta habilitado en este dispositivo ' + ip_address)
        continue
    except Exception as unknown_error:
        print('Algun otro error: ' + unknown_error)
        continue

    output = net_connect.send_command("show running-config", delay_factor=2)
    # Aca verificamos si el archivo tiene contenido
    # buscando dentro si tiene registro del user que inició sesión
    if 'username' in output:
        backup_path = '/Users/jose/Downloads/Networking/networking_scripts/cisco/%s' % (router['ip'])
        filename = backup_path + str("_show running-config_"+ timestr + '.txt')
        f = open(filename, 'w+')
        f.write(output)
        f.close()
        print(colorama.Fore.GREEN + 'Backup realizado con exito')
    else:
        print(colorama.Fore.RED + 'Backup error')

    net_connect.disconnect()
ENDTIME = datetime.now()
TOTALTIME = ENDTIME - STARTTIME
print(colorama.Fore.WHITE + '------------------------------------------------')
print(colorama.Fore.WHITE + '---Tarea finalizada---')
print(colorama.Fore.WHITE + 'Tiempo total de ejecucion: ', str(TOTALTIME))
