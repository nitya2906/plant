import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌱",
    layout="centered"
)

st.title("🌱 Plant Disease Detection System")
st.write("Detect plant diseases using **Camera** or **Image Upload**")

# ---------------- LOAD MODEL ----------------
model = tf.keras.models.load_model("plant_disease_model.h5")

with open("class_names.txt") as f:
    class_names = f.read().splitlines()

# ---------------- REMEDIES ----------------
remedies = {
    "Tomato___Late_blight":
        "Remove infected leaves immediately. Spray copper-based fungicide. Avoid excess watering.",
    "Tomato___Early_blight":
        "Use recommended fungicide. Maintain proper spacing and crop rotation.",
    "Potato___Late_blight":
        "Destroy infected plants. Apply fungicide and ensure good air circulation.",
    "Tomato___healthy":
        "Plant is healthy 🌱 Maintain regular watering and sunlight.",
    "Potato___healthy":
        "Healthy plant 🌿 Continue good soil nutrition."
}

# ---------------- IMAGE INPUT ----------------
st.subheader("📸 Image Input")

input_option = st.radio(
    "Choose input method",
    ("Camera", "Upload Images (Multiple)")
)

images = []

if input_option == "Camera":
    cam_img = st.camera_input("Take a picture of the leaf")
    if cam_img:
        images.append(Image.open(cam_img))

elif input_option == "Upload Images (Multiple)":
    files = st.file_uploader(
        "Upload leaf images",
        type=["jpg", "png", "jpeg"],
        accept_multiple_files=True
    )
    for file in files:
        images.append(Image.open(file))

# ---------------- PREDICTION FUNCTION ----------------
def predict(image):
    img = image.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)
    index = np.argmax(pred)

    disease = class_names[index]
    confidence = np.max(pred) * 100

    return disease, confidence

# ---------------- OUTPUT ----------------
if images:
    st.subheader("🧪 Detection Results")

    for i, img in enumerate(images):
        st.image(img, caption=f"Leaf Image {i+1}", width=300)

        disease, confidence = predict(img)

        st.markdown(f"### 🦠 Disease: **{disease}**")
        st.write(f"📊 Confidence: **{confidence:.2f}%**")

        remedy = remedies.get(
            disease,
            "Please consult an agricultural expert."
        )

        st.success(f"💊 Remedy: {remedy}")
        st.divider()
