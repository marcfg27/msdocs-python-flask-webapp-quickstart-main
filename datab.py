import base64
import os
import secrets

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from flask_sqlalchemy import SQLAlchemy

import hashlib
import hmac


def cifrar_clave(clave_a_cifrar, clave_cifrado, nonce):
    l =len(clave_cifrado)
    encode= clave_cifrado.encode('utf-8')
    aesgcm = AESGCM(encode)
    nonce = nonce.encode('utf-8')  # secrets.token_bytes(12)
    clave1_cifrada = aesgcm.encrypt(nonce, clave_a_cifrar.encode('utf-8'), None)

    return  base64.b64encode(clave1_cifrada).decode('utf-8')



def descifrar_clave(clave1_cifrada, clave_cifrado, nonce):

    try:
        clave1_cifrada = base64.b64decode(clave1_cifrada.encode('utf-8'
                                               ))
        aesgcm = AESGCM(clave_cifrado.encode('utf-8'))
        clave1_descifrada = aesgcm.decrypt(nonce.encode('utf-8'),     clave1_cifrada   , None)
    except:
        return None

    return clave1_descifrada.decode("utf-8")

db = SQLAlchemy()
KEK = os.environ.get('KEK')
nonce = os.environ.get('nonce')
secret_key = descifrar_clave(os.environ.get('MI_SECRET_KEY'),KEK,nonce)
secret_key2 = descifrar_clave(os.environ.get('MI_SECRET_KEY2'),KEK,nonce)
admin_pass = descifrar_clave(os.environ.get('ADMIN_PASS'),KEK,nonce)

email_user = descifrar_clave(os.environ.get('MAIL_USERNAME'),KEK,nonce)

email_pass = descifrar_clave(os.environ.get('MAIL_PASSWORD'),KEK,nonce)




#Salt = "11600f8a2e578cc957564c13dc3f5c57bc52c5cfd5324f36b40be7b96f090b6d"