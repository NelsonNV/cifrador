import argparse
import base64
import os
from tqdm import tqdm
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
        for dirpath, dirnames, archivos in os.walk(ruta):
            for nombre_archivo in tqdm(archivos, desc="Procesando archivos", unit="archivo"):
                archivo = os.path.join(dirpath, nombre_archivo)
                transformar_archivo(accion, fernet, archivo)
    else:
        transformar_archivo(accion, fernet, ruta)

def transformar_archivo(accion, fernet, archivo):
    with open(archivo, 'rb') as f:
        datos = f.read()

    if accion == 'cifrar':
        datos_transformados = fernet.encrypt(datos)
    else:
        datos_transformados = fernet.decrypt(datos)

    with open(archivo, 'wb') as f:
        f.write(datos_transformados)

def obtener_clave(ruta):
    if os.path.isfile(ruta):
        with open(ruta, 'r') as f:
            return f.read().strip()
    else:
        return ruta

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cifra o descifra archivos.')
    parser.add_argument('-c', '--cifrar', action='store_true', help='Cifrar el archivo o carpeta.')
    parser.add_argument('-d', '--descifrar', action='store_true', help='Descifrar el archivo o carpeta.')
    parser.add_argument('-f', '--file', type=str, help='El archivo a cifrar o descifrar.')
    parser.add_argument('-e', '--directory', type=str, help='La carpeta a cifrar o descifrar.')
    parser.add_argument('-k', '--key', type=str, required=True, help='La clave utilizada para cifrar o descifrar.')

    args = parser.parse_args()

    accion = 'cifrar' if args.cifrar else 'descifrar'
    ruta = args.file if args.file else args.directory
    clave = obtener_clave(args.key)

    cifrar_descifrar(accion, clave, ruta)
