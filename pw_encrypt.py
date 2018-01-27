import os, base64
from hashlib import sha256
from hmac import HMAC


def encrypt_password(password, salt=None):
    if salt is None:
        salt = os.urandom(8)

    assert 8 == len(salt)
    assert isinstance(salt, bytes)
    assert isinstance(password, str)

    if isinstance(password, str):
        password = password.encode('UTF-8')

    assert isinstance(password, bytes)

    result = password
    for i in range(10):
        result = HMAC(result, salt, sha256).digest()

    return salt + result


def validate_password(hashed, input_password):
    return hashed == encrypt_password(input_password, salt=hashed[:8])
