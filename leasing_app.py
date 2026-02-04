import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- CONFIGURATION ---
# 🚨 PASTE YOUR TIER 1 GOOGLE KEY BELOW (Inside the quotes) 🚨
API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure the AI with the Modern Engine
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# --- THE WEBPAGE LAYOUT ---
st.set_page_config(page_title="Leasing Assistant", page_icon="🏢")

st.title("🏢 Virtual Leasing Agent")
st.write("Upload the Lease or Building Rules, and ask any question.")

# --- STEP 1: PDF UPLOADER ---
uploaded_file = st.file_uploader("Upload Property Document (PDF)", type="pdf")

# Check if a file is uploaded
if uploaded_file is not None:
    # --- STEP 2: READ THE PDF ---
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        st.success("✅ Document Loaded & Analyzed!")

        # --- STEP 3: THE CHAT ---
        user_question = st.text_input("What would you like to know about this property?")

        if st.button("Ask Agent"):
            if user_question:
                with st.spinner("Agent is checking the specific rules..."):
                    # --- STEP 4: THE BRAIN (Now smarter) ---
                    prompt = f"""
                    You are a helpful, professional Real Estate Leasing Agent.
                    Your goal is to provide accurate information to potential tenants based strictly on the Property Document.
                    
                    RULES:
                    1. Answer based ONLY on the document text below.
                    2. If the user asks about rules (like Pets, Parking, or Noise), explicitly mention ANY restrictions AND exemptions (specifically look for Service Animals/ADA compliance).
                    3. Be friendly but legally precise. Do not guess.
                    4. If the information is not in the document, say: "I cannot find that in the current documents. Please contact the property manager."
                    
                    PROPERTY DOCUMENT:
                    {text}
                    
                    CUSTOMER QUESTION:
                    {user_question}
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.write("### 🤖 Agent Answer:")
                    st.write(response.text)
            else:
                st.warning("Please type a question first.")
                
    except Exception as e:
        st.error(f"Error reading file: {e}")