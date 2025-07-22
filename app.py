import streamlit as st
from qreader import QReader
import qrcode
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="QR Repair & Decode", layout="centered")
st.title("🛠️ QR Detect & Repair with QReader + Streamlit")

qreader = QReader(model_size="s", min_confidence=0.5)

uploaded = st.file_uploader("Upload a QR image", type=["png","jpg","jpeg"])
if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Input Image", use_column_width=True)

    with st.spinner("Detecting QR..."):
        decoded_list = qreader.detect_and_decode(image=np.array(image))

    if not decoded_list:
        st.error("❌ No QR detected or decoded.")
    else:
        for idx, txt in enumerate(decoded_list):
            st.success(f"✅ QR #{idx+1} decoded: **{txt}**")
            qr = qrcode.make(txt)
            buf = io.BytesIO()
            qr.save(buf, format="PNG")
            buf.seek(0)
            st.image(buf, caption="🔄 Regenerate QR", width=200)