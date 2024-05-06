import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from NCSV import *
import json
import base64
from admin import *
from datetime import datetime
import time

icon_path = "assets/truong.png"
st.set_page_config(layout="wide",  page_icon= icon_path, page_title='RSA Digital Sign')
# Set custom color palette
primaryColor="#0b95c5"
backgroundColor="#f9f9f9"
secondaryBackgroundColor="#e6f2f8"
textColor="#252525"

__login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()
if LOGGED_IN == True:
    username = __login__obj.cookies['__streamlit_login_signup_ui_username__']
    ad_path = "assets/admin.webp"
    us_path = "assets/user.jpg"

    def main():
        if username == 'duc':
            st.image(ad_path, width= 500)
            spe()

        else:
            check = False
            st.image(us_path, width=250)
            st.title(f'Hello {username}')
            col1,col2 = st.tabs(['Verify digital sign', "File signing"])
            with col1:
                st.header('Verify digital sign')
                file_check = st.file_uploader('Upload file to verify the sign')
                if file_check is not None:
                    # start_time = time.time()
                    finder_code = st.text_input('Enter your finder code')
                    if finder_code != '':
                        with open('_secret_auth_.json', 'r') as f:
                            data = json.load(f)
                        for user in data:
                            if "digital_sign" in user:
                                if finder_code in user['digital_sign']:
                                    check = True
                                    sign = user['digital_sign'][finder_code]
                                    get_public_key = user['public_key']
                                    loaded_pubkey = rsa.PublicKey.load_pkcs1(get_public_key.encode())
                                    dig_sign = b64decode(sign)
                                    try:
                                        check = verify_sign(file_check.getvalue(), dig_sign, loaded_pubkey)
                                        st.success('Valid digital sign, nothing was changed 👏👏👏')
                                        # end_time = time.time()
                                        # execution_time = end_time - start_time
                                        # print('veri:', execution_time)
                                    except Exception as e:
                                        st.error("Invalid digital sign, something was changed 🚨🚨🚨")
                        if check == False:
                            st.error("Invalid digital sign, something was changed 🚨🚨🚨")


            # with col2:
            #     st.header('File encryption')
            #     data_to_encrypt = st.file_uploader("Upload File to Encrypt")
            #     if data_to_encrypt is not None:         
            #         # Example usage
            #         filename = data_to_encrypt.name # Replace this with the name of the file you're searching for
            #         result = find_file(filename)
            #         if result:
            #             print(f"File found at: {result}")
            #         else:
            #             print("File not found.")

            #         aes_key = generate_aes_key()
            #         if 'clicked' not in st.session_state:
            #             st.session_state.clicked = False

            #         def click_button():
            #             st.session_state.clicked = True

            #         st.button('Download encrypted file', on_click=click_button)

            #         if st.session_state.clicked:
            #             authTag, nonce = encrypt_file(result, aes_key, AES.MODE_GCM)

            #             with open('_secret_auth_.json', 'r') as f:
            #                 data = json.load(f)

            #                 for user in data:
            #                     if user['username'] == username:
            #                         user['authTag'] = b64encode(authTag).decode('utf-8') 
            #                         user['nonce'] = b64encode(nonce).decode('utf-8')  
            #                         publickey = user['public_key']
            #                         loaded_pubkey = rsa.PublicKey.load_pkcs1(publickey.encode())
            #                         encrypted_aes_key = encrypt_aes_key(aes_key, loaded_pubkey)
            #                         hex_aes = b64encode(encrypted_aes_key).decode('utf-8')
            #                         user['aeskey'] = hex_aes
            #                         break

            #                 # Write the updated data back to the JSON file
            #             with open('_secret_auth_.json', 'w') as f:
            #                 json.dump(data, f, indent=4)
                            
            #             st.success('File downloaded to current directory')
            with col2:
                st.header('File signing')
                check = False
                with open('_secret_auth_.json', 'r') as f:
                    data = json.load(f)
                for user in data:
                    if user['username'] == username:
                        if 'private_key' in user:
                            get_private_key = user['private_key']
                            check = True
                            break

                if check == True:
                    loaded_prikey = rsa.PrivateKey.load_pkcs1(get_private_key.encode())
                    file2 = st.file_uploader('Upload File to sign')
                    if file2 is not None:
                        # start_time = time.time()
                        digital_sign = file_signing(file2.getvalue(), loaded_prikey)
                        c = datetime.now()
                        for user in data:
                            if user['username'] == username:
                                b64name = base64.b64encode((file2.name).encode()).decode()
                                if "digital_sign" in user:
                                    user["digital_sign"][b64name] = b64encode(digital_sign).decode('utf-8')
                                else:
                                    user["digital_sign"] = {
                                        b64name: b64encode(digital_sign).decode('utf-8')
                                    }
                                break

                        # Write the updated data back to the JSON file
                        with open('_secret_auth_.json', 'w') as f:
                            json.dump(data, f, indent=4)

                        st.success(f'Successfully added digital sign of file {file2.name} to user: {username} at: {c}')
                        st.text_input('Here is your finder code', value=f'{b64name}')
                        # end_time = time.time()
                        # execution_time = end_time - start_time
                        # print('sign:', execution_time)
                else:
                    st.warning('Please ask admin for keys first')
    main()