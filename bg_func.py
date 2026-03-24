import base64
import streamlit as st


def set_background(image_file, darkness=0.5):
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{data}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, {darkness});
                z-index: 0;
            }}
            div[data-testid="InputInstructions"] {{
                display: none;
            }}
        </style>
    """, unsafe_allow_html=True)