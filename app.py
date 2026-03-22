import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Image Tool Pro", layout="centered")

st.title("🖼️ Image Tool Pro")
st.write("Compress • Resize • Convert images easily")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Original Image", use_column_width=True)

    st.subheader("⚙️ Settings")

    # Resize option
    resize = st.checkbox("Resize Image")
    if resize:
        width = st.number_input("Width", value=img.width)
        height = st.number_input("Height", value=img.height)

    # Compression quality
    quality = st.slider("Compression Quality", 10, 100, 80)

    # Format conversion
    format_option = st.selectbox("Convert Format", ["JPEG", "PNG", "WEBP"])

    if st.button("🚀 Process Image"):
        processed_img = img

        # Resize
        if resize:
            processed_img = processed_img.resize((int(width), int(height)))

        # Convert mode for JPEG
        if format_option == "JPEG":
            processed_img = processed_img.convert("RGB")

        # Save to memory
        buf = io.BytesIO()
        processed_img.save(buf, format=format_option, quality=quality)
        byte_im = buf.getvalue()

        st.success("✅ Image Processed!")

        st.image(processed_img, caption="Processed Image", use_column_width=True)

        st.download_button(
            label="📥 Download Image",
            data=byte_im,
            file_name=f"processed.{format_option.lower()}",
            mime=f"image/{format_option.lower()}"
        )