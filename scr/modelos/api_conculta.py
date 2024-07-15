import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def verificar_si_existe(dni):
    api_token = "AfPB0qvaHtKoHoYsx6KydZWU6x6LBR4AbaOivZYMFgFz6CN5uy"
    url = f"https://api.perufacturacion.com/api?api_token={api_token}&json=dni&id={dni}"
    try: 

        response = requests.get(url, verify=False)
        response.raise_for_status()  

        if response.status_code == 200:
            datos = response.json()
            if datos and 'dni' in datos:
                return True, datos
        return False, None
    
    except requests.exceptions.RequestException as e:
        print("No hay conexion de internet")

    return False, None

# Ejemplo de uso
#dni = "22223347"
#datos_dni = obtener_datos_dni(dni)
'''
if isinstance(datos_dni, dict):
    apellido_materno = datos_dni.get('apellido_materno')
    apellido_paterno = datos_dni.get('apellido_paterno')
    nombres = datos_dni.get('nombres')
    dni = datos_dni.get('dni')
    
    print(f"Apellido Materno: {apellido_materno}")
    print(f"Apellido Paterno: {apellido_paterno}")
    print(f"Nombres: {nombres}")
    print(f"DNI: {dni}")
else:
    print(datos_dni)

'''
