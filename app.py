import streamlit as st
from PIL import Image
import io
import json
import os

st.set_page_config(page_title="Image Tool Pro", layout="centered")

# -------- USER SYSTEM --------
USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

users = load_users()

if "user" not in st.session_state:
    st.session_state.user = None

st.title("🖼️ Image Tool Pro")

# -------- LOGIN --------
if not st.session_state.user:
    st.subheader("Login / Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login / Signup"):
        if username not in users:
            users[username] = {"password": password, "pro": False, "history": []}
            save_users(users)
            st.success("Account created!")
        elif users[username]["password"] != password:
            st.error("Wrong password")
        st.session_state.user = username
        st.rerun()

else:
    user = st.session_state.user
    st.success(f"Welcome {user}")

    # -------- PRO PLAN --------
    if not users[user]["pro"]:
        st.warning("Free Plan (Upgrade to Pro ₹30/month)")
        if st.button("Activate Pro (Demo)"):
            users[user]["pro"] = True
            save_users(users)
            st.success("Pro Activated!")
    else:
        st.success("🌟 Pro User")

    # -------- IMAGE TOOL --------
    uploaded_file = st.file_uploader("Upload Image", type=["jpg","jpeg","png","webp"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Original", use_column_width=True)

        st.subheader("Settings")

        # Resize
        resize = st.checkbox("Resize")
        if resize:
            width = st.number_input("Width", value=img.width)
            height = st.number_input("Height", value=img.height)

        # Compress
        quality = st.slider("Quality", 10, 100, 80)

        # Convert
        format_option = st.selectbox("Format", ["JPEG","PNG","WEBP"])

        # PRO FEATURES
        if users[user]["pro"]:
            grayscale = st.checkbox("Convert to Grayscale")
            rotate = st.slider("Rotate", 0, 360, 0)
        else:
            grayscale = False
            rotate = 0

        if st.button("Process"):
            processed = img

            if resize:
                processed = processed.resize((int(width), int(height)))

            if grayscale:
                processed = processed.convert("L")

            if rotate:
                processed = processed.rotate(rotate)

            if format_option == "JPEG":
                processed = processed.convert("RGB")

            buf = io.BytesIO()
            processed.save(buf, format=format_option, quality=quality)
            byte_im = buf.getvalue()

            st.image(processed, caption="Processed", use_column_width=True)

            st.download_button("Download", byte_im, file_name="image."+format_option.lower())

            # SAVE HISTORY
            users[user]["history"].append({
                "format": format_option,
                "quality": quality
            })
            save_users(users)

    # -------- HISTORY --------
    st.subheader("📜 History")
    for h in users[user]["history"]:
        st.write(h)

    # -------- LOGOUT --------
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()