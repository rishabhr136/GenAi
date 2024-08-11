import streamlit as st
from pathlib import Path
import google.generativeai as genai
import os
os.environ['GOOGLE_API_KEY'] = "AIzaSyD4EKdGbVxYnB9Ua5GqqTxzQC-ETohzBIA"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

system_prompts = [
    """
    You are a domain expert in medical image analysis. You are tasked with 
    examining medical images for a renowned hospital.
    Your expertise will help in identifying or 
    discovering any anomalies, diseases, conditions or
    any health issues that might be present in the image.
    
    Your key responsibilites:
    1. Detailed Analysis : Scrutinize and thoroughly examine each image, 
    focusing on finding any abnormalities.
    2. Analysis Report : Document all the findings and 
    clearly articulate them in a structured format.
    3. Recommendations : Basis the analysis, suggest remedies, 
    tests or treatments as applicable.
    4. Treatments : If applicable, lay out detailed treatments 
    which can help in faster recovery.
    
    Important Notes to remember:
    1. Scope of response : Only respond if the image pertains to 
    human health issues.
    2. Clarity of image : In case the image is unclear, 
    note that certain aspects are 
    'Unable to be correctly determined based on the uploaded image'
    3. Disclaimer : Accompany your analysis with the disclaimer: 
    "Consult with a Doctor before making any decisions."
    4. Your insights are invaluable in guiding clinical decisions. 
    Please proceed with the analysis, adhering to the 
    structured approach outlined above.
    
    Please provide the final response with these 4 headings : 
    Detailed Analysis, Analysis Report, Recommendations and Treatments
    
"""
]
# st.set_page_config(page_title = 'VitalImage Analytics', page_icon = ':robot')
# st.image('NEET-Top-Medical-Colleges.jpg', width = 150)
# st.title('Vital Image Rishabh')
# st.subheader('An application that can help user to identify medical images')
model = genai.GenerativeModel(model_name = "gemini-1.5-pro-latest",generation_config=generation_config,
                              safety_settings=safety_settings)
st.set_page_config(page_title="Visual Medical Assistant", page_icon="🩺", 
layout="wide")
st.title("Visual Medical Assistant 👨‍⚕️ 🩺 🏥")
st.subheader("An app to help with medical analysis using images")

upload_file = st.file_uploader("Upload medical images", type = ["jpg","png","jpeg"])
if upload_file:
    st.image(upload_file, width= 200, caption = "Uploaded Image")
submit = st.button("Generate the analysis")

if submit:
    image_data = upload_file.getvalue()
    image_parts = [
        {
        "mime_type":"image/jpeg",
        "data":image_data
        }
    ]
    prompt_parts = [
        image_parts[0],
        system_prompts[0],
    ]
    res = model.generate_content(prompt_parts)
    if res:
        st.title("Detailed analysis based on Image")
        st.write(res.text)


        