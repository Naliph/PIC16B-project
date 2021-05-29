# Streamlit App for the colorization
"""
Run the app by installing streamlit using pip
Type in cmd > streamlit run colorizeApp.py
"""

import streamlit as st
from load_css import local_scss
from serving import (
        load_model,
        evaluate_input,
)
#from model import colorize_model
import numpy as np
import os
import base64
from io import BytesIO
import PIL
from PIL import Image
import cv2
import time

st.page_icon=":art:"
st.page_title="Image Colorization"



st.markdown("<h1 style='text-align: center;'>Image Colorization</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'> with TensorFlow</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'> PIC16B Group Project</h3>", unsafe_allow_html=True)


####################################################
# choice = st.sidebar.number_input(label = 'Enter a value: ', min_value=1, value=1, step=1)
about = '''
### Abstract

>`Colorization` has a variety of applications in recreational and historical context. 
It transforms how we see and perceive photos which provides an immense value in helping us visualize and convey stories, emotion, as well as history. 
Our project scraped data using `selenium`
analyze and prepare the data, train them on a deep neural network deployed through `TensorFlow`,
and use `OpenCv` for image processing.

<div style='text-align: right;'>Alice Pham & Duc Vu</div>
'''

st.sidebar.markdown(about, unsafe_allow_html=True)

####################################################




md = '''
Start colorization with some Black & White images. You can upload an image or choose a pre-existed test images to try out the colorization
'''
st.markdown(md)

st.markdown("### Upload a B&W Picture:")
# Uploading File to Page: Choose your own GRAY picture to colorize
uploadFile = st.file_uploader(label="Upload Gray Image: ", type=['jpg', 'png', 'jpeg'])


# Checking the Format of the page
if uploadFile is not None:
    # Read and Load Image as np.array
    img = Image.open(uploadFile)
    gray = np.array(img)
    st.image(gray)

    start_analyze_file = st.button('Colorize', key='1')

    if start_analyze_file == True:
        with st.spinner(text = 'Colorizing...'):
            input_buffer = BytesIO()
            output_buffer = BytesIO()
            img.save(input_buffer, 'PNG')
            input_img = evaluate_input(input_buffer)
            input_img.save(output_buffer, format='JPG')
            output_img = base64.b64encode(output_buffer.getvalue())
            color = np.array(output_img)
            st.image(color)

###################################################3

# If not upload, choose an image in our test images:
st.markdown("### Choose a B&W Picture from our small collection:")


# Alice's Folder
#img_folder = "C:\\Users\\Alice\\Documents\\GitHub\\PIC16B-project\\colorizer\\Test"

# Duc's Folder
img_folder = "/home/blackbox/Documents/UCLA/PIC-Python/PIC16B/PIC16B-project/colorizer/Test"

def load_img_from_folder(folder):
    imgs = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None: imgs.append(img)
    return imgs

images = load_img_from_folder(img_folder)
st.image([img for img in images])


i = st.number_input(label="Choose a test picture number:", min_value=1, value=1, step=1)
gray2 = images[i-1]

start_analyze_test_file = st.button('Colorize', key='2')

if start_analyze_test_file == True:
    colorize_model(gray2)
