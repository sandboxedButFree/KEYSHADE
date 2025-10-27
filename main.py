import os
import base64

from crypt import generate_key, intialise_cipher, encrypt_password, decrypt_password

## Check if an environment variable exists for the encryption key.
if os.getenv('PASSWORD_KEY') == None:

    ## Generate Key.
    key = generate_key()

    ## os.environ can only except a str type so the bytes must be converted to a base64 string to be stored, this will be reverted back for decryption later.
    encoded_key = base64.b64encode(key).decode('utf-8')

    ##Storing the environment variable.
    os.environ['PASSWORD_KEY'] = encoded_key
