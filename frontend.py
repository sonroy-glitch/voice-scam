import streamlit as st
import streamlit.components.v1 as components

# Change to your backend's address
BACKEND_URL = "http://localhost:5054/detect"

st.set_page_config(page_title="Fraud Call Detector", page_icon="🎙️")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #fdf6e3;
        color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎙️ Fraud Call Detector")
st.write("Record audio in the browser and send it to backend for AssemblyAI transcription & fraud detection.")

recorder_html = f"""
<div>
  <button id="startBtn">Start Recording</button>
  <button id="stopBtn" disabled>Stop Recording</button>
  <p id="status">Not recording</p>
  <pre id="result" style="white-space: pre-wrap;"></pre>
</div>

<script>
let mediaRecorder;
let chunks = [];

const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const status = document.getElementById('status');
const result = document.getElementById('result');

startBtn.onclick = async () => {{
  try {{
    const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
    mediaRecorder = new MediaRecorder(stream);
    chunks = [];
    mediaRecorder.ondataavailable = e => chunks.push(e.data);
    mediaRecorder.onstart = () => {{
      status.innerText = "Recording...";
      startBtn.disabled = true;
      stopBtn.disabled = false;
      result.innerText = "";
    }};
    mediaRecorder.start();
  }} catch (err) {{
    alert("Error accessing microphone: " + err.message);
  }}
}};

stopBtn.onclick = async () => {{
  if (!mediaRecorder) return;
  mediaRecorder.onstop = async () => {{
    status.innerText = "Processing audio...";

    const blob = new Blob(chunks, {{ type: 'audio/wav' }});
    result.innerText = "Uploading to backend...";

    const formData = new FormData();
    const filename = "recording_" + Date.now() + ".wav";
    formData.append("file", blob, filename);

    try {{
      const resp = await fetch("{BACKEND_URL}", {{
        method: "POST",
        body: formData
      }});
      if (!resp.ok) {{
        const text = await resp.text();
        result.innerText = "Backend error: " + resp.status + " - " + text;
      }} else {{
        const json = await resp.json();
        let out = "Response:\\n" + JSON.stringify(json, null, 2) + "\\n\\n";
        if (json.transcript) {{
          out += "Transcript:\\n" + json.transcript + "\\n\\n";
        }}
        if (json.fraud_detected) {{
          out += "🚨 Fraud detected!";
        }} else {{
          out += "✅ No fraud detected.";
        }}
        result.innerText = out;
      }}
    }} catch (err) {{
      result.innerText = "Upload failed: " + err;
    }}

    status.innerText = "Done.";
    startBtn.disabled = false;
    stopBtn.disabled = true;
  }};

  mediaRecorder.stop();
}};
</script>
"""

components.html(recorder_html, height=260)
