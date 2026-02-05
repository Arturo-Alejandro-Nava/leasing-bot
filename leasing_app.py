import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURATION ---
# Use the secure key from Streamlit Secrets
API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure the AI
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# --- THE WEBPAGE LAYOUT ---
st.set_page_config(page_title="Leasing Assistant", page_icon="🏢")

st.title("🏢 Virtual Leasing Agent (Vision Enabled)")
st.write("Upload any document (Digital PDF, Scanned Image, or Handwriting).")

# --- STEP 1: PDF UPLOADER ---
uploaded_file = st.file_uploader("Upload Property Document", type=["pdf", "png", "jpg"])

# Check if a file is uploaded
if uploaded_file is not None:
    
    # --- STEP 2: HANDLE THE FILE ---
    # Since this is a vision model, we need to upload the actual file to Google,
    # not just extract text. We must save it to a temporary file first.
    with open("temp_leasing_doc.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("✅ Document uploaded! The AI is looking at it now...")

    # --- STEP 3: THE CHAT FORM ---
    with st.form(key='chat_form'):
        user_question = st.text_input("What would you like to know about this property?")
        submit_button = st.form_submit_button("Ask Agent")

    if submit_button and user_question:
        try:
            with st.spinner("Agent is reading the document (Vision Scan)..."):
                
                # 1. Upload the file to Google's 'Brain'
                sample_file = genai.upload_file(path="temp_leasing_doc.pdf", display_name="Lease Doc")
                
                # 2. Define the Prompt
                system_prompt = """
                You are a professional Leasing Agent.
                The user has uploaded a document (it might be a scanned PDF or image).
                
                RULES:
                1. Answer strictly based on the visible text in the provided file.
                2. If the document is a scan, do your best to read the visual text.
                3. Mention any specific rules (Fees, Pets, Parking).
                4. Look specifically for legal exemptions like "Service Animals".
                5. If you cannot find the answer, say "I cannot find that in this document."
                """
                
                # 3. Ask the Question (We send the Prompt + The File + The Question)
                response = model.generate_content([system_prompt, sample_file, user_question])
                
                # 4. Display Result
                st.write("### 🤖 Agent Answer:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")