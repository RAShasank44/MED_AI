import dotenv 
import google.generativeai as genai 
import streamlit as st 

# Configure the API key for the generative AI
from api_key import api_key 
genai.configure(api_key=api_key) 

# Define the generation configuration
generation_config = { 
 "temperature": 0.4, 
 "top_p": 0.95, 
 "top_k": 64, 
 "max_output_tokens": 8192, 
} 

def model(info, history): 

 # Format history for Google Generative AI
 formatted_history = [] 
 for item in history: 
 role = "user" if item["role"] == "user" else "model"
 formatted_history.append({ 
 "role": role, 
 "parts": [{"text": item["content"]}] 
 }) 

 # Create the model with the specified generation configuration 
  generative_model = genai.GenerativeModel( 
 model_name="gemini-1.5-flash", 
 generation_config=generation_config, 
 ) 
 
 # Start or continue the chat session with history
 chat_session = generative_model.start_chat(history=formatted_history) 
 # Prepare the message with system instruction and user query
 message = f"""
 Patient-Centered Communication:
 Always greet users warmly and with empathy.
 Diagnosis and Assessment:
 Use the information provided by the user to suggest possible diagnoses.
 Offer a differential diagnosis approach, discussing multiple potential conditions based on 
the symptoms described.
 Clearly state that your suggestions are not a substitute for professional medical advice and 
recommend consulting a licensed healthcare provider for definitive diagnoses and treatment.
 
 Treatment Guidance:
 Provide general information about potential treatment options, including lifestyle changes, 
over-the-counter medications, and when to seek further medical help.
 Avoid suggesting specific medications unless the user is already taking them or they are 
commonly recognized treatments for the symptoms presented.
 Patient Education:
 Offer educational information about common medical conditions, prevention strategies, 
and the importance of regular medical check-ups.
 Use simple, clear language to ensure that explanations are easily understood.
 
 Ethical Considerations:
 Maintain a professional tone, respecting patient confidentiality and privacy.
 Emphasize the importance of ethics in medicine, including patient autonomy and informed 
consent.
 Limitations and Caution:
 """
 # Get the response from the model
 response = chat_session.send_message(message) 
 response_text = response.text 
 return response_text
