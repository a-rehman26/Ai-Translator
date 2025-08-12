import streamlit as st
import google.generativeai as genai
import os

# --- Hardcoded Gemini API Key ---
# Replace "YOUR_GEMINI_API_KEY_HERE" with your actual key.
# You can get one for free from Google AI Studio.
GEMINI_API_KEY = "AIzaSyAK0LdUjH07p77HzhAwVKHf8KXlFXQmLkY"

# --- Language List ---
SUPPORTED_LANGUAGES = [
    "Arabic", "Urdu", "English", "French", "German",
    "Spanish", "Mandarin Chinese", "Japanese", "Russian", "Hindi"
]

# --- Placeholder Functions for API Integration ---
def generate_embedding(text):
    """Placeholder for a function that calls an Embedding API."""
    # Placeholder: Return a dummy vector
    return [0.1] * 1536 

def query_vector_db(embedding_vector):
    """Placeholder for a function that queries a Vector Database."""
    # Placeholder: Return a static context.
    return [
        "Context 1: The user is translating technical documentation for a software company.",
        "Context 2: The document mentions terms like 'API', 'framework', and 'deployment'."
    ]

# --- Gemini API Integration for Translation ---
def generate_translation(prompt, api_key):
    """
    This function sends the context-aware prompt to the Gemini language model
    and returns the translated text.
    """
    if not api_key:
        raise ValueError("Gemini API key is not set.")
    
    genai.configure(api_key=api_key)
    
    try:
        # Use the Gemini model for text generation
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        # Extract the content from the API response
        translated_text = response.text
        return translated_text

    except Exception as e:
        st.error(f"Gemini API error: {e}")
        return None

# --- Streamlit User Interface (UI) ---
st.set_page_config(page_title="Intelligent Translator", layout="wide")
st.title("🌐 Intelligent Translation Application (Powered by Gemini)")
st.markdown("This application uses an LLM with context retrieval to provide high-quality translations.")
st.markdown("---")

# --- i. Text Input and Language Selection ---
col1, col2 = st.columns(2)
with col1:
    source_text = st.text_area("Enter text to translate:", height=200, placeholder="Type or paste your text here...")

with col2:
    target_language = st.selectbox(
        "Select a target language:",
        SUPPORTED_LANGUAGES,
        placeholder="Choose a language..."
    )

# --- The Translation Process Button ---
if st.button("Translate", type="primary"):
    if not source_text or not target_language:
        st.error("Please enter text and select a target language.")
    else:
        with st.spinner("Translating..."):
            try:
                # --- ii. Text Processing ---
                st.info("Step 1: Generating semantic embedding...")
                embedding_vector = generate_embedding(source_text)

                # --- iii. Document Retrieval ---
                st.info("Step 2: Retrieving relevant context from the Vector Database...")
                relevant_context = query_vector_db(embedding_vector)

                # --- iv. Context-aware Prompt Creation ---
                st.info("Step 3: Creating a context-aware prompt...")
                prompt = f"""
                You are a highly skilled professional translator.
                The user wants to translate the following text into {target_language}.
                Use the provided context to ensure the translation is accurate and domain-specific.

                Context:
                {relevant_context}

                Source Text:
                {source_text}

                Please provide only the translated text.
                """

                # --- v. Translation Generation ---
                st.info("Step 4: Generating translation with the Language Model...")
                # The hardcoded key is passed directly to the function.
                translated_text = generate_translation(prompt, GEMINI_API_KEY)

                if translated_text:
                    # --- vi. Result Display ---
                    st.success("✅ Translation Complete!")
                    st.write("---")
                    st.subheader("Translated Text")
                    st.markdown(f"**{translated_text}**")

                    st.download_button(
                        label="Download Translated Text",
                        data=translated_text,
                        file_name=f"translation_{target_language}.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                # --- vii. Error Handling ---
                st.error(f"An error occurred: {e}. Please try again.")

# This video provides an overview of how to use the Gemini API in Python, which is a key component for this project. [How to Integrate Gemini API with Python (2025)](https://www.youtube.com/watch?v=yZ4AXBGUnWA)
# http://googleusercontent.com/youtube_content/0