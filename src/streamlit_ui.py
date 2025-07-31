

import streamlit as st
import tempfile
import os
import base64
from agent import agent_main
from st_circular_progress import CircularProgress

st.markdown("""
    <link rel="stylesheet" 
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# ✅ Convert video to base64
def get_video_base64(video_path):
    with open(video_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ✅ Use relative path to your media folder
video_path = os.path.join(os.path.dirname(__file__), "media", "cyber4.mp4")
video_b64 = get_video_base64(video_path)

# ✅ Inject video background
st.markdown(
    f"""
    <style>
    .stApp {{
        background: none;
    }}
    video.background-video {{
        position: fixed;
        top: 50%;
        left: 50%;
        min-width: 100%;
        min-height: 100%;
        width: auto;
        height: auto;
        z-index: -1;
        transform: translate(-50%, -50%); /* ✅ Centers video */
        object-fit: cover;  /* ✅ Maintains aspect ratio and covers screen */
    }}
    .video-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.8);
        z-index: -1;
    }}
    /* Expander header */
    div[data-testid="stLayoutWrapper"] div:first-child {{
        background: rgb(26, 28, 36); /* header background */
    }}
    
    /* Style only download buttons */
    div.stDownloadButton > button {{
        background-color: green !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
    }}

    /* Optional hover effect */
    div.stDownloadButton > button:hover {{
        background-color: darkgreen !important;
        color: #fff !important;
    }}
    h1 {{
        text-align: center;
        background: transparent;
        color: #00ffcc !important;
        padding: 15px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 2.2rem;
        text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffaa;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.4);
        margin-bottom: 55px !important;
    }}
    </style>

    <video id="bgvid" autoplay loop muted playsinline class="background-video">
        <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
    </video>

    <div class="video-overlay"></div>

    """,
    unsafe_allow_html=True
)
st.set_page_config(
    page_title="AI Open-Source Dependency Guardian",
    page_icon="🔒",
    
)
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
    st.title("AI Open-Source Dependency Guardian")
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
                parsed_results, patched_file, risk_score, improvement = agent_main(uploaded_file.name,tmp_file_path)
            
            st.success("✅ Analysis complete!")

            # Risk level indicator with circular progress
            st.markdown("### 📊 Risk Level")
            
            # Color and styling based on risk level
            if risk_score >= 81:
                color = "#fa1a2c"
                emoji = "🚨"
                risk_level = "Critical Risk"
            elif risk_score >= 61:
                color = "#ff4901"
                emoji = "⚠️"
                risk_level = "High Risk"
            elif risk_score >= 41:
                color = "#ffc107"
                emoji = "⚡"
                risk_level = "Medium Risk"
            else:
                color = "#4caf50"
                emoji = "🛡️"
                risk_level = "Low Risk"
            
            # Circular progress and risk level display
            # Create circular progress component
            risk_value = max(0, min(100, int(risk_score)))
            
            # Try circular progress first
            try:
                circular_progress = CircularProgress(
                    label=f"{emoji} {risk_level}",
                    value=risk_value,
                    key=f"risk_circular_progress_{uploaded_file.name}_{risk_value}",
                    size="large",
                    color=color
                )
                circular_progress.st_circular_progress()
                if improvement is not None:
                    if improvement > 0:
                        st.markdown(
                            """
                            <div style='text-align:center; color:#4caf50; font-weight:bold;'>
                                <i class="fas fa-arrow-up"></i> Improved by {0} points since last scan!
                            </div>
                            """.format(improvement),
                            unsafe_allow_html=True
                        )
                    elif improvement < 0:
                        st.markdown(
                            """
                            <div style='text-align:center; color:#ff4757; font-weight:bold;'>
                                <i class="fas fa-arrow-down"></i> Increased by {0} points since last scan!
                            </div>
                            """.format(abs(improvement)),
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            "<div style='text-align:center; color:#ffc107; font-weight:bold; margin-top:8px;'>📊 No change since last scan.</div>",
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown(
                        "<span style='color: #00bcd4; text-align:center;font-weight: bold;'>📌 First scan - baseline risk score set.</span>",
                        unsafe_allow_html=True
                    )
            except Exception as e:
                st.error(f"Circular progress error: {e}")
                # Fallback to regular progress bar
                st.progress(risk_value / 100)
                st.markdown(f"**{emoji} {risk_level} - {risk_value}%**")

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
                download_name = f"{base_name}{ext}"
                mime_type = "application/json" if ext == ".json" else "text/plain"

                st.subheader("📥 Download Patched File")
                b64_file = base64.b64encode(patched_file.encode()).decode()

                download_link = f"""
                    <a href="data:{mime_type};base64,{b64_file}" 
                    download="{download_name}" 
                    style="
                            display:inline-block;
                            padding:10px 20px;
                            background-color:green;
                            color:white;
                            font-weight:bold;
                            border-radius:8px;
                            text-decoration:none;">
                            <i class="fa-solid fa-download fa-bounce" style="color: #ffffff;margin-right:8px;"></i>
                            Download Patched Dependencies
                    </a>
                """

                st.markdown(download_link, unsafe_allow_html=True)

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

if __name__ == "__main__":
    main()
