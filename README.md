# HP1920

Script para automatización de backups, fue probado en switches HP 1920 con Sistema Operativo HPE Comware 5.20.99

Para ello ejecuta el comando ```display current-configuration```

Este script contempla la habilitaciòn avanzada de gestión por CLI con que cuentan estos switches mediante los siguientes comandos:
```javascript
_cmdline-mode on
y
Jinhua1920unauthorized
```

## Lo que necesita
Instalar Netmiko atraves de pip, para esto necesita python 3

```
$ pip install netmiko
```

En macOS tuve que utilizar el siguiente comando

```
$ sudo -H pip install netmiko
```

### Cambiar los valores del diccionario con sus parámetros


```py
hp_switch_1920 = {
	'device_type': 'hp_comware',
	'ip': 'tu_ip',
	'username': 'tu_usuario',
	'password': 'tu_contrasena'
}

```

### Cambiar la ubicación en donde quiera que se aloje los archivos de backup

```py
backup_path = '/Users/jose/Downloads/backup/%s' % (hp_switch_1920['ip'])
```

### Ejecutar el script

```py
jose@hackbook-pro# python3 swhp1920.py
```

El archivo de backup se guarda en la ubicación que configuro.
