

import streamlit as st
import tempfile
import os
import re
from agent import agent_main

def highlight_severity(text):
    if "Critical" in text:
        return f"<span style='color:red;font-weight:bold'>{text}</span>"
    elif "High" in text:
        return f"<span style='color:orange;font-weight:bold'>{text}</span>"
    elif "Medium" in text:
        return f"<span style='color:goldenrod'>{text}</span>"
    elif "Low" in text:
        return f"<span style='color:green'>{text}</span>"
    elif "N/A" in text:
        return f"<span style='color:white'>{text}</span>"
    return text

def main():
    st.title("🔒 AI Open-Source Dependency Guardian")
    st.markdown("Scan your dependency files for security risks and get AI-powered recommendations!")
    
    uploaded_file = st.file_uploader(
        "Upload your dependency file", 
        type=['txt', 'json'], 
        help="Upload requirements.txt or package.json"
    )
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            with st.spinner("🔍 Analyzing dependencies..."):
                parsed_results, patched_file, risk_score = agent_main(tmp_file_path)
            
            st.success("✅ Analysis complete!")

            # Risk level indicator with progress
            st.markdown("### 📊 Risk Level")
            
            # Color and styling based on risk level
            if risk_score >= 81:
                bg_color = "#ff4757"
                text_color = "#ffffff"
                emoji = "🚨"
                risk_level = "Critical Risk"
            elif risk_score >= 61 and risk_score <= 80:
                bg_color = "#ff9800"
                text_color = "#ffffff"
                emoji = "⚠️"
                risk_level = "High Risk"
            elif risk_score >= 41 and risk_score <= 60:
                bg_color = "#ffc107"
                text_color = "#333333"
                emoji = "⚡"
                risk_level = "Medium Risk"
            else:
                bg_color = "#4caf50"
                text_color = "#ffffff"
                emoji = "✅"
                risk_level = "Low Risk"
            
            
            # Progress bar and risk level with status
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(risk_score / 100)
                st.markdown(f"**{risk_score}% Risk Level**")
            with col2:
                st.markdown(f"**{emoji} {risk_level}**")

            # ✅ Show each dependency as a card
            st.subheader("Dependency Analysis")
            for dep in parsed_results:
                with st.expander(f"📦 {dep['package']} ({dep['current_version']}) - {dep['severity']}"):
                    st.markdown(
                        f"**CVSS:** {dep['cvss']} | "
                        f"{highlight_severity(dep['severity'])}",
                        unsafe_allow_html=True
                    )
                    st.write(dep['explanation'])
                    st.markdown(f"✅ **Suggested Fix:** `{dep['fix']}`")

            # ✅ Download patched file
            if patched_file:
                base_name, ext = os.path.splitext(uploaded_file.name)
                download_name = f"{base_name}_patched{ext}"
                mime_type = "application/json" if ext == ".json" else "text/plain"

                st.subheader("📥 Download Patched File")
                st.download_button(
                    label="Download Patched Dependencies",
                    data=patched_file,
                    file_name=download_name,
                    mime=mime_type
                )

            # ✅ Side-by-side original and patched file preview
            st.subheader("📂 File Comparison")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original File**")
                with open(tmp_file_path, 'r') as f:
                    original_content = f.read()
                st.code(original_content, language="json" if uploaded_file.name.endswith(".json") else "text")
            with col2:
                st.markdown("**Patched File**")
                st.code(patched_file, language="json" if uploaded_file.name.endswith(".json") else "text")

        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
        finally:
            os.unlink(tmp_file_path)
    
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
        - `package.json` (Node.js)
        """)

if __name__ == "__main__":
    main()
