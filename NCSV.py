from Crypto.Cipher import AES
import rsa
import rsa.randnum as rn
import os


# Generate RSA keys
def generate_rsa_keys():
    public_key, private_key = rsa.newkeys(2048, poolsize=8)
    return public_key, private_key


def file_signing(file_path, private_rsa_key):
    # with open(file_path, 'rb') as f:
        signature = rsa.sign(file_path, private_rsa_key, 'SHA-256')
        return signature  
    

def verify_sign(file_path, signature, public_rsa_key):
    #with open(file_path, 'rb') as f:
        a = rsa.verify(file_path, signature, public_rsa_key)
        return a

#sonarqubetest password = trolvietnam
