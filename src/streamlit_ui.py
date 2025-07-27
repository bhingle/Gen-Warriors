import streamlit as st
import tempfile
import os
from agent import agent_main

def main():
    st.title("🔒 AI Open-Source Dependency Guardian")
    st.markdown("Scan your dependency files for security risks and get AI-powered recommendations!")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your dependency file", 
        type=['txt', 'json'], 
        help="Upload requirements.txt or package.json"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            # Process the file
            with st.spinner("🔍 Analyzing dependencies..."):
                report, patched_file = agent_main(tmp_file_path)
            
            # Display results
            st.success("✅ Analysis complete!")
            
            # Show risk report
            st.subheader("📊 Risk Report")
            st.text_area("Analysis Results", report, height=400)
            
            # Download patched file
            if patched_file:
                st.subheader("📥 Download Patched File")
                st.download_button(
                    label="Download Patched Dependencies",
                    data=patched_file,
                    file_name=f"{uploaded_file.name}.patched",
                    mime="text/plain"
                )
            
            # Show file preview
            st.subheader("📋 Original File Preview")
            with open(tmp_file_path, 'r') as f:
                original_content = f.read()
            st.code(original_content, language="text")

            # Patched File
            st.subheader("🔧 Patched File Preview")
            st.code(patched_file, language="json" if uploaded_file.name.endswith(".json") else "text")

            
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
    
    # Sidebar with info
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This tool helps you:
        - 🔍 Detect outdated packages
        - ⚠️ Identify security vulnerabilities  
        - 🤖 Get AI-powered recommendations
        - 📝 Generate patched dependency files
        """)
        
        st.header("📋 Supported Files")
        st.markdown("""
        - `requirements.txt` (Python)
        - `package.json` (Node.js) - Coming soon
        """)

if __name__ == "__main__":
    main() 