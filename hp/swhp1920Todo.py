import os
from datetime import datetime
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

sw_hp_1920 = {
    'sw-p1': {
        'device_type': 'hp_comware',
        'ip': '172.10.254.110',
        'username': 'tu_usuario',
        'password': 'tu_contrasena'
    },
    'sw-p2': {
        'device_type': 'hp_comware',
        'ip': '172.10.254.111',
        'username': 'tu_usuario',
        'password': 'tu_contrasena'
    },
    'sw-p3': {
        'device_type': 'hp_comware',
        'ip': '172.10.254.112',
        'username': 'tu_usuario',
        'password': 'tu_contrasena'
    }
}

STARTTIME = datetime.now()
mes = STARTTIME.strftime("%b")
anio = STARTTIME.strftime("%Y")
dia = STARTTIME.strftime("%d")

# LOOPING THROUGH HP 1920 SWITCHES
for key, values in sw_hp_1920.items():
    device_type = values.get('device_type', {})
    ip_address = values.get('ip', {})
    username = values.get('username', {})
    password = values.get('password', {})

    print('#' * 50)
    print('Intentando conectar al dispositivo')
    timestr = STARTTIME.strftime("%d%m%Y%H%M")

    try:
        net_connect = ConnectHandler(device_type=device_type, host=ip_address, username=username, password=password)
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
    print('[OK]: Conectado via SSH a: ' + ip_address)

    output = net_connect.send_command_timing(
        'y',
        strip_prompt=False,
        strip_command=False
    )
    output = net_connect.send_command_timing(
        '_cmdline-mode on',
        strip_prompt=False,
        strip_command=False
    )
    print(output)
    if 'Continue' in output:
        output += net_connect.send_command_timing(
            'y',
            strip_prompt=False,
            strip_command=False
        )
    print(output)
    if 'ssword' in output:
        output = net_connect.send_command_timing(
            'Jinhua1920unauthorized',
            strip_prompt=False,
            strip_command=False
        )
    print(output)
    output = net_connect.send_command_timing(
        'screen-length disable',
        strip_prompt=False,
        strip_command=False
    )
    print(output)
    output = net_connect.send_command_timing(
        'display current-configuration',
        delay_factor=2,
        strip_prompt=False,
        strip_command=False
    )

    backup_path = str('/home/rconfig/data/SwitchHP1920/%s' % (key))
    path = os.path.join(backup_path, anio, mes)
    # Si no existe directorio, lo crea
    if not os.path.exists(path):
        os.makedirs(path)
        print('[OK]: Se creo el siguiente directorio')
        print('--> ' + path)

    file = str(ip_address + '_displaycurrent-configuration_' + timestr + '.txt')
    filename = os.path.join(path, file)
    f = open(filename, 'w+')
    f.write(output)
    f.close()
    print('[OK]: Se creo el siguiente archivo')
    print('--> ' + filename)

    net_connect.disconnect()
ENDTIME = datetime.now()
TOTALTIME = ENDTIME - STARTTIME
print('-' * 50)
print('-----Tarea finalizada-----')
print('Tiempo total de ejecucion: ', str(TOTALTIME))