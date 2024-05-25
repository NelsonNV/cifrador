
# Cifrado y Descifrado de Archivos

Este script de Python permite cifrar y descifrar archivos y carpetas utilizando una clave proporcionada por el usuario.

## Requisitos

Las bibliotecas necesarias para ejecutar este script se pueden instalar con:

```bash
pip install -r requirements.txt
```

Las bibliotecas requeridas son:

- argparse
- base64
- os
- tqdm
- cryptography

## Uso

Para cifrar o descifrar un archivo o carpeta, puedes usar los siguientes argumentos:

- `-c`, `--cifrar`: Cifra el archivo o carpeta.
- `-d`, `--descifrar`: Descifra el archivo o carpeta.
- `-f`, `--file`: El archivo a cifrar o descifrar.
- `-e`, `--directory`: La carpeta a cifrar o descifrar.
- `-k`, `--key`: La clave utilizada para cifrar o descifrar.

Por ejemplo, para cifrar un archivo, puedes usar el siguiente comando:

```bash
python script.py --cifrar --file mi_archivo.txt --key mi_clave
```

Y para descifrar el mismo archivo, puedes usar:

```bash
python script.py --descifrar --file mi_archivo.txt --key mi_clave
```

## Advertencia

Por favor, ten en cuenta que la clave utilizada para cifrar los archivos es necesaria para descifrarlos. Si pierdes la clave, no podrás recuperar tus archivos cifrados.

