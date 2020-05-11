from netmiko import ConnectHandler 
import time

hp_switch_1920 = {
	'device_type': 'hp_comware',
	'ip': 'tu_ip',
	'username': 'tu_usuario',
	'password': 'tu_contrasena'
}

timestr = time.strftime("%Y%m%d%H%M")
	
net_connect = ConnectHandler(**hp_switch_1920)

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
print (output)
if 'Continue' in output:
    output += net_connect.send_command_timing(
		'y', 
		strip_prompt=False, 
		strip_command=False
	)
print (output)
if 'ssword' in output:
    output = net_connect.send_command_timing(
		'Jinhua1920unauthorized',
		strip_prompt=False, 
		strip_command=False
		)
print (output)
output = net_connect.send_command_timing(
	'screen-length disable',
	strip_prompt=False,
	strip_command=False
	)
print (output)

output = net_connect.send_command_timing(
	'display current-configuration',
	delay_factor=2,
	strip_prompt=False,
	strip_command=False
	)

# Ruta donde se aloja los backups en rconfig
# /home/rconfig/data/{Categoria}/{NombreDispositivo}/{Año}/{Mes}/{dia}
backup_path = '/Users/jose/Downloads/backup_pulp/%s' % (hp_switch_1920['ip'])

filename = backup_path + str("_displaycurrent-configuration_" + timestr + '.txt')
f = open(filename, 'w+')
f.write(output)
f.close()

net_connect.disconnect()
