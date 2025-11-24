# Import the necessary libraries
import streamlit as st
from PIL import Image
import io

# Set the title for the web app
st.title("🖼️ Image Background Remover")
st.write("Upload an image to remove its background.")

# Create a file uploader widget
uploaded_file = st.file_uploader("Choose your image...", type=["jpg", "jpeg", "png"])

# Check if a user has uploaded a file
if uploaded_file is not None:
    # Open the uploaded image
    input_image = Image.open(uploaded_file)
    
    # Split the screen into two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        # Display the original image
        st.image(input_image, caption="Your uploaded image", use_column_width=True)

    # Create a button to trigger the background removal
    if st.button("Remove Background"):

        # Try to import rembg at runtime so the app can start even if it's missing
        try:
            from rembg import remove
        except Exception as e:
            st.error(
                "Missing dependency: `onnxruntime` (required by `rembg`) is not installed.\n"
                "Install with: `pip install rembg onnxruntime`\n"
                "On Debian/Ubuntu you may also need: `sudo apt-get install -y libgomp1`"
            )
            st.stop()

        # It's necessary to convert the image to bytes
        input_bytes = io.BytesIO()
        input_image.save(input_bytes, format="PNG")
        input_bytes = input_bytes.getvalue()

        # Main function from rembg
        try:
            output_bytes = remove(input_bytes)
        except Exception as e:
            st.error(f"Error while removing background: {e}")
            st.stop()

        # Open the resulting image
        output_image = Image.open(io.BytesIO(output_bytes))

        with col2:
            st.subheader("Result")
            # Display the image with the background removed
            st.image(output_image, caption="Image with background removed", use_column_width=True)

        # Create a download button for the result
        st.download_button(
            label="Download Image",
            data=output_bytes,
            file_name="background_removed.png",
            mime="image/png"
        )