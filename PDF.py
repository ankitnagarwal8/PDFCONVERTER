from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import streamlit as st
import os

def images_to_pdf(image_files, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    
    for image_file in image_files:
        try:
            img = Image.open(image_file)
            img_width, img_height = img.size
            
            if img_width > 612 or img_height > 792:
                img.thumbnail((612, 792))

            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            temp_img_path = "temp_image.jpg"
            img.save(temp_img_path, "JPEG")
            
            c.drawImage(temp_img_path, 0, 0, width=img.width, height=img.height)
            c.showPage()

            img.close()
            if os.path.exists(temp_img_path):
                os.remove(temp_img_path)

        except Exception as e:
            st.error(f"Error processing image: {e}")
            continue

    c.save()
    st.success(f"PDF created successfully: {output_pdf}")

# Streamlit UI with dropdowns and enhanced styling
st.title("📸 Photo to PDF Converter 🎉", anchor="title")

st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #FF5733; /* Bright orange */
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 18px;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #C70039; /* Darker red on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Dropdown for image selection method
selection_method = st.selectbox("Choose how to add images:", ["Upload from Computer", "Take a Photo with Camera"])

# Initialize image file list
image_files = []

# Upload or take photo based on selection
if selection_method == "Upload from Computer":
    uploaded_files = st.file_uploader("Choose images 📁", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
        image_files.extend(uploaded_files)
elif selection_method == "Take a Photo with Camera":
    camera_image = st.camera_input("Take a photo 📷")
    if camera_image is not None:
        image_files.append(camera_image)

output_pdf = "output.pdf"

# Convert images to PDF if button clicked
if st.button("Convert to PDF"):
    if image_files:
        images_to_pdf(image_files, output_pdf)
        with open(output_pdf, "rb") as pdf_file:
            st.download_button(
                label="Download PDF 📥",
                data=pdf_file,
                file_name=output_pdf,
                mime="application/pdf",
                key="download_pdf"
            )
    else:
        st.warning("Please upload at least one image or take a photo.")
