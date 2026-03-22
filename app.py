import streamlit as st
from PIL import Image
import io
import json
import os

# -------- PAGE CONFIG --------
st.set_page_config(page_title="Image Tool Pro", layout="wide")

# -------- HEADER DESIGN --------
st.markdown("""
    <style>
    .header {
        text-align: center;
        padding: 20px;
        background-color: #0e1117;
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>🖼️ Image Tool Pro</h1>
    <h3>Developer: Prayansh Gautam</h3>
</div>
""", unsafe_allow_html=True)

# -------- USER SYSTEM --------
USER_FILE = "users.json"
MASTER_KEY = "8969720851"

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

# -------- LOGIN --------
if not st.session_state.user:
    st.subheader("🔐 Login / Signup")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    key = st.text_input("Pro Key (optional)")

    if st.button("Login / Signup"):
        if username == "" or password == "":
            st.error("Enter username & password")
        else:
            if username not in users:
                users[username] = {
                    "password": password,
                    "pro": False,
                    "history": []
                }

            if users[username]["password"] != password:
                st.error("Wrong password")
            else:
                if key == MASTER_KEY:
                    users[username]["pro"] = True

                save_users(users)
                st.session_state.user = username
                st.rerun()

# -------- MAIN APP --------
else:
    user = st.session_state.user
    st.success(f"Welcome {user}")

    # PLAN STATUS
    if users[user]["pro"]:
        st.success("🌟 PRO USER")
    else:
        st.warning("Free Plan (Enter Pro Key to unlock PRO)")

    uploaded_file = st.file_uploader("📤 Upload Image", type=["jpg","jpeg","png","webp"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Original Image", use_column_width=True)

        st.subheader("⚙️ Settings")

        # Resize
        resize = st.checkbox("Resize Image")
        if resize:
            width = st.number_input("Width", value=img.width)
            height = st.number_input("Height", value=img.height)

        # Compression
        quality = st.slider("Compression Quality", 10, 100, 80)

        # Format conversion
        format_option = st.selectbox("Convert Format", ["JPEG","PNG","WEBP"])

        # PRO FEATURES
        if users[user]["pro"]:
            grayscale = st.checkbox("Convert to Grayscale")
            rotate = st.slider("Rotate Image", 0, 360, 0)
        else:
            grayscale = False
            rotate = 0

        if st.button("🚀 Process Image"):
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

            st.image(processed, caption="Processed Image", use_column_width=True)

            st.download_button(
                "📥 Download Image",
                byte_im,
                file_name="image."+format_option.lower()
            )

            # SAVE HISTORY
            users[user]["history"].append({
                "format": format_option,
                "quality": quality
            })
            save_users(users)

    # -------- HISTORY --------
    st.subheader("📜 Your History")
    if users[user]["history"]:
        for h in users[user]["history"]:
            st.write(h)
    else:
        st.write("No history yet")

    # -------- LOGOUT --------
    if st.button("🚪 Logout"):
        st.session_state.user = None
        st.rerun()