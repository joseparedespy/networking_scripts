import os
from datetime import datetime
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from cisco_ip_list import router

# Obtengo la lista de comandos definidos
with open('cisco_command_list.txt') as c:
    command_list = c.read().splitlines()

STARTTIME = datetime.now()
mes = STARTTIME.strftime("%b")
anio = STARTTIME.strftime("%Y")
for key, values in router.items():
    device_type = values.get('device_type', {})
    ip_address = values.get('ip', {})
    username = values.get('username', {})
    password = values.get('password', {})
    port = values.get('port', {})
    nameRconfig = key

    print('#' * 50)
    print('Conectando al dispositivo con ip: ' + ip_address)
    timestr = STARTTIME.strftime("%d%m%Y%H%M")

    try:
        net_connect = ConnectHandler(device_type=device_type, host=ip_address, username=username, password=password, port=port)
    except (AuthenticationException):
        print('[ERROR]: Falla de autenticacion')
        continue
    except (NetMikoTimeoutException):
        print('[ERROR]: El dispositivo es inalcanzable o se encuentra apagado')
        continue
    except (EOFError):
        print('[ERROR]: End of file while attempting device ' + ip_address)
        continue
    except (SSHException):
        print('Problema con SSH. Estas seguro de que SSH esta habilitado en este dispositivo ' + ip_address)
        continue
    except Exception as unknown_error:
        print('[ERROR]: ' + str(unknown_error))
        continue
    print('[OK]: Conectado via SSH')

    parentPath = '/Users/jose/Downloads/Networking/Netmiko/cisco/backup/%s' % (nameRconfig)
    path = os.path.join(parentPath, anio, mes)
    # Si no existe directorio, lo crea
    if not os.path.exists(path):
        os.makedirs(path)
        print('[OK]: Se creo el siguiente directorio')
        print('--> ' + path)

    for command in command_list:
        if command.strip().startswith('#'):
            continue
        output = net_connect.send_command(command, delay_factor=2)

        file = str(ip_address + '_' + command.replace(' ', '-') + '_' + timestr + '.txt')
        filename = os.path.join(path, file)
        f = open(filename, 'w+')
        f.write(output)
        f.close()

        if os.stat(filename).st_size > 100:
            print('[OK]: COMANDO EJECUTADO: ' + command)
        else:
            if 'Invalid input detected' in output:
                print('[ERROR]: COMANDO INVALIDO ' + command)
            elif 'Incomplete command' in output:
                print('[ERROR]: EL COMANDO ESTA INCOMPLETO ' + command)
            # Ir agregando otras posibles exepciones
            else:
                print('[ERROR]: VERIFICAR INTEGRIDAD DEL ARCHIVO GENERADO --> ' + command)
        output = None
    net_connect.disconnect()
ENDTIME = datetime.now()
TOTALTIME = ENDTIME - STARTTIME
print('-' * 50)
print('-----Tarea finalizada-----')
print('Tiempo total de ejecucion: ', str(TOTALTIME))