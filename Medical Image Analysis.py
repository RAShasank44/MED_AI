#import necessary modules
import streamlit as st 
from pathlib import Path 
import google.generativeai as genai 
from api_key import api_key 
#configure genai with api key
genai.configure(api_key=api_key) 
#set up the model
generation_config = { 
 "temperature": 1, 
 "top_p": 0.95, 
 "top_k": 40, 
 "max_output_tokens": 8192, 
 "response_mime_type": "text/plain", 
} 
#apply safety settings
safety_settings = [ 
 { 
 "category" : "HARM_CATEGORY_HARASSMENT", 
 "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
 }, 
 { 
 "category" : "HARM_CATEGORY_HATE_SPEECH", 
 "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
 }, 
 { 
 "category" : "HARM_CATEGORY_SEXUALLY_EXPLICIT", 
 "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
 }, 
 { 
 "category" : "HARM_CATEGORY_HATE_SPEECH", 
 "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
 }, 
 { 
 "category" : "HARM_CATEGORY_DANGEROUS_CONTENT", 
 "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
} 
] 

system_prompt = """
As a highly skilled medical practitioner specializing in large analysis, you are tasked with 
examining images for a renowned hospital. Your expertise is crucial in identifying any 
anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities include:
1. Detailed Analyis: Throughly analyze each image, focusing on identifying any abnormal 
findings.
2. Findings Report: Documents all observed anomalies or signs of diseases. Clearly articulate 
these findings in a structured format.
3. Recommendations and Next Steps: Based on ypur analysis ,suggest potential next steps, 
including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or 
interventions.

Important Notes:
1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Images: In cases where the image quality impodes clear analysis, note that 
certain aspects are 'Unable to be determined based on the provided image'.
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before 
making any decisions".
4. Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, 
adhering to the structured approach outlined above.
"""

#model configuration
model = genai.GenerativeModel( 
 model_name="gemini-1.5-flash", 
 generation_config=generation_config, 
 safety_settings=safety_settings 
) 

#set page configuration
st.set_page_config(page_title="MEDIAI Image Analytics",page_icon=":robort:") 

#set the title
st.title("MEDIAI IMAGE ANALYSICS") 

#set the subtitle
st.subheader("An application that can help users to identify medical images")
uploaded_file = st.file_uploader("Upload the medical image for 
analysis",type=["png","jpg","jpeg"]) 
submit_button = st.button("Generate the Analysis") 
if submit_button: 
 #process the uploaded image
 image_data = uploaded_file.getvalue() 

 #making our images ready
 image_parts = [ 
 { 
 "mime_type" : "image/jpeg", 
 "data" : image_data 
 } 
 ] 

 #making our prompt ready
 prompt_parts = [ 
 image_parts[0], 
 system_prompt 
 ] 

 #Generate a response based on prompt and image
 response = model.generate_content(prompt_parts) 
 if response: 
 st.title("Here is the analysis based on your image:") 
 if uploaded_file: 
 st.image(uploaded_file, width=300, caption="Uploaded Medical Image") 
 st.write(response.text)
