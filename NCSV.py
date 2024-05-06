from Crypto.Cipher import AES
import rsa
import rsa.randnum as rn
import os


def find_file(filename):
    for root, dirs, files in os.walk('/'):  # Start from the root directory
        if filename in files:
            return os.path.join(root, filename)
    return None


# Generate RSA keys
def generate_rsa_keys():
    public_key, private_key = rsa.newkeys(3072, poolsize=8)
    return public_key, private_key


# def generate_aes_key():
#     aes_key = rn.read_random_bits(256)
#     return aes_key

# def encrypt_aes_key(aes_key, public_rsa_key):
#     encrypted_aes_key = rsa.encrypt(aes_key, public_rsa_key)
#     return encrypted_aes_key

# def decrypt_aes_key(encrypted_aes_key, private_rsa_key):
#     decrypted_aes_key = rsa.decrypt(encrypted_aes_key, private_rsa_key)
#     return decrypted_aes_key


def file_signing(file_path, private_rsa_key):
    # with open(file_path, 'rb') as f:
        signature = rsa.sign(file_path, private_rsa_key, 'SHA-256')
        return signature  
    

def verify_sign(file_path, signature, public_rsa_key):
    #with open(file_path, 'rb') as f:
        a = rsa.verify(file_path, signature, public_rsa_key)
        return a

# ENCRYPTING FILE USING AES_GCM:

# nonce  96 bits + counter 32 bits --> forms IV (internally generated)
def encrypt_file(file_path, aes_key, mode):

    enc_obj = AES.new(aes_key, mode)
#     # encrypt file --> tạo file đã được mã hóa
    with open(file_path, 'rb') as file_in:
        with open(file_path + '.enc', 'wb') as file_out:
            while True:
                chunk = file_in.read()
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)   #Empty character * the number of it to be added

                encrypted_chunk, authTag = enc_obj.encrypt_and_digest(chunk)
                file_out.write(encrypted_chunk) 
            
            return (authTag, enc_obj.nonce) 

# def encrypt_file(data, aes_key, mode):
#     enc_obj = AES.new(aes_key, mode)
#     if len(data) % 16 != 0:
#         data += b' ' * (16 - len(data) % 16)  #Padding if needed
#     encrypted_data, authTag = enc_obj.encrypt_and_digest(data)
#     return encrypted_data, authTag, enc_obj.nonce



def decrypt_file(file_path, authTag, nonce, aes_key, mode):
    # Open the input and output files
    with open(file_path, 'rb') as file_in:
        with open(file_path[:-8] + '.dec' + file_path[-8:-4], 'wb') as file_out:
            enc_obj = AES.new(aes_key, mode, nonce)

            # Process the file in chunks
            while True:
                chunk = file_in.read()
                if len(chunk) == 0:
                    break

                # Decrypt the chunk and write it to the output file
                decrypted_chunk = enc_obj.decrypt_and_verify(chunk, authTag)
                file_out.write(decrypted_chunk)


