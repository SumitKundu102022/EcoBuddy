import streamlit as st

# Set page configuration (must be the very first Streamlit command)
st.set_page_config(page_title="EcoBuddy: Personalized Carbon Footprint Tracker", page_icon="🌍", layout="wide")
# st.set_page_config(
#         page_title="EcoBuddy Login",
#         page_icon="🔐",
#         layout="centered",
#     )


from dotenv import load_dotenv
from database import create_user, authenticate_user, reset_password
import app  # Import the app logic here
from pymongo.errors import ServerSelectionTimeoutError
from streamlit_cookies_manager import EncryptedCookieManager
import requests
import time
import os

# Load environment variables
load_dotenv()

# Load password from environment variable
COOKIE_PASSWORD = os.getenv("COOKIE_PASSWORD")  # Replace or set environment variable

# Initialize the EncryptedCookieManager
cookies = EncryptedCookieManager(prefix="ecobuddy", password=COOKIE_PASSWORD)
if not cookies.ready():
    st.stop()

@st.cache_data
def load_data():
    # Simulate data loading
    return ["data"]

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Login"  # Default page

if "authenticated" not in st.session_state:
    st.session_state.authenticated = cookies.get("authenticated") == "true"

if "username" not in st.session_state:
    st.session_state.username = cookies.get("username")

# Ensure the app redirects to the login page if not authenticated
if not st.session_state.authenticated:
    st.session_state.current_page = "Login"

# Simulated Toast Notification
def show_toast(message, toast_type="success"):
    if toast_type == "success":
        st.success(message)
    elif toast_type == "error":
        st.error(message)
    elif toast_type == "info":
        st.info(message)

# Handle Server/Connection Issues
def check_connection(func):
    """Decorator to handle connection issues."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ServerSelectionTimeoutError:
            show_toast("Connection to the database server failed. Please check your internet or server settings.", "error")
        except requests.ConnectionError:
            show_toast("Connection problem detected. Please ensure your internet connection is active.", "error")
        except Exception as e:
            show_toast(f"An unexpected error occurred: {str(e)}", "error")
    return wrapper


# Login Function
@check_connection
def login():
    
    # Use columns for reduced width
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column proportions for centering
    
    with col2:  # Place the input fields in the center column
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
           if authenticate_user(username, password):
              st.session_state.authenticated = True
              st.session_state.username = username
              st.session_state.current_page = "Dashboard"  # Redirect to dashboard
              cookies["authenticated"] = "true"
              cookies["username"] = username
              #cookies["user"] = username
              cookies.save()  # Save the cookies
              show_toast("Login successful!", "success")
           else:
               show_toast("Invalid username or password", "error")


# Registration Function
@check_connection
def register():
    # Use columns for reduced width
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column proportions for centering
    
    with col2:  # Place the input fields in the center column
        st.title("Register")
        username = st.text_input("Choose a Username")
        password = st.text_input("Choose a Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if password != confirm_password:
                show_toast("Passwords do not match!", "error")
            elif len(password) < 6:
                show_toast("Password must be at least 6 characters long.", "error")
            else:
                create_user(username, password)
                show_toast("Registration successful! Please log in.", "success")


# Forgot Password Function
@check_connection
def forgot_password():
    # Use columns for reduced width
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column proportions for centering
    with col2:  # Place the input fields in the center column
        st.title("Forgot Password")
        username = st.text_input("Enter your Username")
        new_password = st.text_input("Enter a New Password", type="password")
        confirm_new_password = st.text_input("Confirm New Password", type="password")

        if st.button("Reset Password"):
            if new_password != confirm_new_password:
                show_toast("Passwords do not match!", "error")
            elif len(new_password) < 6:
                show_toast("Password must be at least 6 characters long.", "error")
            else:
                if reset_password(username, new_password):
                    show_toast("Password reset successful! Please log in.", "success")
                else:
                    show_toast("Username not found.", "error")


# Logout Function
@check_connection
def logout():
    # Reset session state
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.current_page = "Login"  # Redirect to dashboard
    cookies["authenticated"] = "false"
    cookies["username"] = ""

    # Save changes to cookies
    cookies.save()

    # Reset page state
    st.session_state.submitted = False
    show_toast("Logged out successfully!", "info")
    



# Authentication Flow
def main():
    if st.session_state.authenticated:
        # Show the dashboard only if authenticated
        st.session_state.current_page = "Dashboard"
        placeholder = st.empty()  # Placeholder for the welcome message
        placeholder1 = st.empty()
        with placeholder.container():
            st.title(f"Welcome, {st.session_state.username}!")
            placeholder1.write("You are now logged in.")
        
        # Hide the welcome message after 5 seconds
        time.sleep(5)
        placeholder.container().empty()
        placeholder1.empty()
        
        col1, col2 = st.columns([9, 1])  # Adjust the proportions as needed
        with col2:
            if st.button("Logout"):
                logout()
                st.rerun()  # Use st.rerun() to enforce a rerun after logout
        
        # Only run the app if authenticated
        if st.session_state.authenticated and st.session_state.current_page == "Dashboard":
            app.run_app()
        
    else:
        # Redirect to login if not authenticated
        st.session_state.current_page = "Login"
        menu = st.sidebar.selectbox("Menu", ["Login", "Register", "Forgot Password"])
        if menu == "Login":
            login()
        elif menu == "Register":
            register()
        elif menu == "Forgot Password":
            forgot_password()


# Run the app
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Critical Error: {str(e)}")
        st.stop()
