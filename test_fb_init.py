import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

def test():
    print("Testing Firebase Initialization from secrets...")
    try:
        if "firebase_service_account" not in st.secrets:
            print("Error: firebase_service_account not found in st.secrets")
            return
            
        info = dict(st.secrets["firebase_service_account"])
        print(f"Project ID: {info.get('project_id')}")
        
        # Try without replace first
        key = info.get("private_key", "")
        print(f"Key starts with: {key[:30]}...")
        print(f"Key ends with: ...{key[-30:]}")
        print(f"Number of newlines in key: {key.count('\n')}")
        
        try:
            cred = credentials.Certificate(info)
            if firebase_admin._apps:
                for app in list(firebase_admin._apps.keys()):
                    firebase_admin.delete_app(firebase_admin._apps[app])
            firebase_admin.initialize_app(cred)
            print("Success (No replace)!")
            return
        except Exception as e:
            print(f"Failed (No replace): {e}")

        # Try with replace
        info_fixed = dict(info)
        info_fixed["private_key"] = info_fixed["private_key"].replace("\\n", "\n")
        print(f"Number of newlines after replace: {info_fixed['private_key'].count('\n')}")
        
        try:
            cred = credentials.Certificate(info_fixed)
            if firebase_admin._apps:
                for app in list(firebase_admin._apps.keys()):
                    firebase_admin.delete_app(firebase_admin._apps[app])
            firebase_admin.initialize_app(cred)
            print("Success (With replace)!")
        except Exception as e:
            print(f"Failed (With replace): {e}")

    except Exception as g:
        print(f"General error: {g}")

if __name__ == "__main__":
    test()
