from netmiko import ConnectHandler
import time

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

timestr = time.strftime("%Y%m%d%H%M")
mes = time.strftime("%B")

# LOOPING THROUGH HP 1920 SWITCHES
for key, values in sw_hp_1920.items():
    device_type = values.get('device_type', {})
    ip_address = values.get('ip', {})
    username = values.get('username', {})
    password = values.get('password', {})

    net_connect = ConnectHandler(device_type=device_type, host=ip_address, username=username, password=password)

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

    backup_path = str('/home/rconfig/data/SwitchHP1920/%s' % (key) + '/2020/' + mes + '/%s' % (ip_address))
    filename = backup_path + str('_displaycurrent-configuration_' + timestr + '.txt')
    # print(filename)
    f = open(filename, 'w+')
    f.write(output)
    f.close()
    net_connect.disconnect()