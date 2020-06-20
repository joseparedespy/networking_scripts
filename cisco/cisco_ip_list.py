"""
En este archivo se cargan todas las opciones de los equipos segun necesidad
    - device_type: [fortinet, hp_comware, cisco_ios, etc.]
    - ip:           Dirección ip del equipo
    - username:     Usuario
    - password:     Contraseña
    - port:         Por defecto 22
Los nombres de los diccionarios anidados serían el nombre del equipo en el rconfig - var nameRconfig
"""
router = {
    'iosxr1': {
        'device_type': 'cisco_nxos',
        'ip': 'sbx-iosxr-mgmt.cisco.com',
        'username': 'admin',
        'password': 'Admin_1234!',
        'port': '8181'
    }
}

'''
Soy un comentario :)
'''


