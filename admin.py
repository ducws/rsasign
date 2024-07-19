from Crypto.Cipher import AES
import rsa
import streamlit as st
from NCSV import *
import json
from base64 import b64encode, b64decode


# Function to add key to _secret_auth_.json file
def add_key_to_auth(username, public_key, private_key):
    with open('_secret_auth_.json', 'r') as f:
        data = json.load(f)
    for user in data:
        if user['username'] == username:
            user['public_key'] = public_key.save_pkcs1().decode()
            user['private_key'] = private_key.save_pkcs1().decode()
            break
    with open('_secret_auth_.json', 'w') as f:
        json.dump(data, f, indent=4)

# Function to get or create session state
def get_state():
    if 'selected_username' not in st.session_state:
        st.session_state.selected_username = None
    if 'rsa_keys' not in st.session_state:
        st.session_state.rsa_keys = None
    return st.session_state

# Main function
def spe():


    st.title('ADMINISTRATOR')
    # tab1, tab2, tab3 = st.tabs(["RSA Key Management", "File signing", "Decrypt file"])
    # with tab1:
    st.header("RSA Key Management")
    state = get_state()

    # Button to generate RSA keys
    if st.button("Generate RSA Key"):
        public_key, private_key = generate_rsa_keys()
        state.rsa_keys = (public_key, private_key)
        st.success("RSA key pair generated successfully!")

    # Select box to choose username
    usernames = [user['username'] for user in json.load(open('_secret_auth_.json'))]
    state.selected_username = st.selectbox("Select Username to Add Key", usernames, index=usernames.index(state.selected_username) if state.selected_username else 0)

    if st.button("Add Key"):
        if state.rsa_keys:
            add_key_to_auth(state.selected_username, state.rsa_keys[0], state.rsa_keys[1])
            st.success(f"Keys added for user: {state.selected_username}")
        else:
            st.warning("Please generate RSA key pair first.")

