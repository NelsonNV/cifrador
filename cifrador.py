import argparse
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def obtener_fernet(clave):
    clave = clave.encode()  # Convertir a bytes
    salt = b'salt_'  # Debe ser bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    clave = base64.urlsafe_b64encode(kdf.derive(clave))  # Can only use kdf once
    return Fernet(clave)

def cifrar_descifrar(accion, clave, ruta):
    fernet = obtener_fernet(clave)

    if os.path.isdir(ruta):
        archivos = os.listdir(ruta)
    else:
        archivos = [ruta]

    for nombre_archivo in archivos:
        with open(nombre_archivo, 'rb') as f:
            datos = f.read()

        if accion == 'cifrar':
            datos_transformados = fernet.encrypt(datos)
        else:
            datos_transformados = fernet.decrypt(datos)

        with open(nombre_archivo, 'wb') as f:
            f.write(datos_transformados)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cifra o descifra archivos.')
    parser.add_argument('accion', choices=['cifrar', 'descifrar'], help='La acción a realizar: cifrar o descifrar.')
    parser.add_argument('clave', help='La clave utilizada para cifrar o descifrar.')
    parser.add_argument('ruta', help='La ruta del archivo o carpeta a cifrar o descifrar.')

    args = parser.parse_args()

    cifrar_descifrar(args.accion, args.clave, args.ruta)

