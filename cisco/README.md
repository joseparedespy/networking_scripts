# Networking scripts

Scripts para redes utilizando la librería [Netmiko](https://github.com/ktbyers/netmiko)

## Instalación de requisitos

Necesita tener python3

Se recomienda hacer las pruebas en un [entorno virtual](https://medium.com/@m.monroyc22/configurar-entorno-virtual-python-a860e820aace)

```py
$ virtualenv env -p python3
$ source env/bin/activate
```

Comprobar que estamos ejecutando python en nuestro entorno vitual
 
```py
$ which python
```

Tiene que ser la dirección donde creamos el entorno

```py
$ pip install netmiko
$ pip install colorama
```

Para desactivar entorno
```py
$ deactivate
```

### Modificar según necesidad

Modificar el archivo cisco_ip_list.txt, ingresando las ip's de los dispositivos cada ip en una linea diferente.

Para mayor seguridad podemos hacer que el script sea dinámico y que solicite el usuario y contraseña del dispositivo en cada iteración. 
De momento solo se ingresa dentro del script y se supone que todos los equipos comparten las mismas credenciales.

Modificar ruta donde se descargará el archivo de configuración.

#### Datos de prueba

Utilizamos las credeciales de un router NX-OSv 9000 extraidos de un lab del sandbox devnet de cisco [Link](https://devnetsandbox.cisco.com/RM/Diagram/Index/dae38dd8-e8ee-4d7c-a21c-6036bed7a804?diagramType=Topology) 

Nexus 9000v Host : sbx-nxos-mgmt.cisco.com
* SSH Port: 8181
* NETCONF Port: 10000
* NXAPI Ports: 80 (http) & 443 (HTTPS)
* RESTCONF Port : 443 (HTTPS)
* Username: admin
* Password: Admin_1234!

#### Ejecución

```py
$ python ciscoNXosbackup.py
```





