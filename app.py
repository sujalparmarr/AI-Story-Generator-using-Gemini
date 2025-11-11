import streamlit as st 
from story_generator import generate_story_from_images,narrate_story
from PIL import Image

#st.title("AI Story Maker")
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap');

        /* Force apply font + shadow */
        h1.main-title, .main-title {
            font-family: 'Poppins', sans-serif !important;
            font-size: 52px !important;
            font-weight: 700 !important;
            text-align: center !important;
            color: #ffffff !important;
            text-shadow:
                0px 0px 4px rgba(255, 0, 0, 0.4),
                0px 0px 10px rgba(255, 0, 0, 0.6),
                0px 0px 18px rgba(255, 0, 0, 0.8);
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("<h1 class='main-title'>AI Story Generator</h1>", unsafe_allow_html=True)


#st.markdown("Upload 1–10 images, and AI will turn them into a story")
st.markdown(
    """
    <style>
        .subtitle-text {
            font-family: 'Poppins', sans-serif !important;
            text-align: center !important;
            font-size: 20px !important;
            font-weight: 400 !important;
            color: rgba(255,255,255,0.75) !important;
            margin-top: -10px !important;
            margin-bottom: 25px !important;
        }
    </style>
    <p class="subtitle-text">Upload 1–10 images, and AI will turn them into a story</p>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("Your Inputs")
    
    
    
    upload_files= st.file_uploader(
        "Drop your images here...",
        type=["png","jpg","jpeg"],
        accept_multiple_files=True
    )
    
    
    story_style= st.selectbox(
        "Pick your story style",
        ("Comedy","Thriller","Sci fi","Mystery","Adventure")
        
    )
    
    generate_button=st.button("Generate Story + Voice-over",type="primary")
    
    
if generate_button:
    if not upload_files:
        st.warning("Please upload atlest 1 image.")
    elif len(upload_files)>10:
        st.warning("Please upload an maximum of 10 images.")
    else:
        with st.spinner("Almost there… AI is preparing your story and audio."):
            try:
                pil_images= [Image.open(uploaded_file) for uploaded_file in  upload_files]
                st.subheader("Your visual Inspiration:")
                image_columns= st.columns(len(pil_images))

                for i ,image in enumerate(pil_images):
                    with image_columns[i]:
                        st.image(image, use_container_width=True)

                generate_story= generate_story_from_images(pil_images, story_style)
                if "Error" in generate_story or "failed" in generate_story or"API key" in generate_story:
                    st.error(generate_story)
                else:
                    st.subheader(f"Your {story_style} story: ")
                    st.success(generate_story)


                st.subheader("Listen to your Story:")
                audio_file= narrate_story(generate_story)
                if audio_file:
                    st.audio(audio_file,format="audio/mp3")

            except Exception as e:
                st.error(f"An application  error occurred {e}")