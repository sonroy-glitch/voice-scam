import os
import tempfile
import joblib
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
import assemblyai as aai
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ----------------------
# Model & Label Encoder
# ----------------------
tokenizer = AutoTokenizer.from_pretrained('./roberta-audio-model-inference')
model = AutoModelForSequenceClassification.from_pretrained('./roberta-audio-model-inference')

device = torch.device('cpu')
model.to(device)
model.eval()

# Load label encoder
le = joblib.load('./encoder.pkl')

def get_prediction(input_text):
    inputs = tokenizer([input_text], return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)
    predicted_label = predictions.item()
    return le.inverse_transform([predicted_label])[0]

# ----------------------
# Flask App Setup
# ----------------------
flask_app = Flask(__name__)
CORS(flask_app)

# AssemblyAI setup
aai.settings.api_key = "ee7668fc7e9c49139de60eeba6e14bbc"
config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@flask_app.route("/detect", methods=["POST"])
def detect_fraud():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    audio_file = request.files["file"]
    _, ext = os.path.splitext(audio_file.filename)
    if not ext:
        ext = ".wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext, dir=UPLOAD_DIR) as tmp:
        tmp_path = tmp.name
        audio_file.save(tmp_path)

    try:
        transcript = aai.Transcriber(config=config).transcribe(tmp_path)

        if transcript.status == "error":
            return jsonify({"error": transcript.error}), 500

        text = transcript.text or ""
        predicted_class = get_prediction('''Good morning, this is [Your Name]'s personal assistant. How can I help you today?''')
        fraud_detected = (predicted_class.lower() == "scam"or predicted_class.lower() == "suspicious" )

        return jsonify({
            "fraud_detected": fraud_detected,
            "predicted_class": predicted_class,
            "transcript": text,
            "filename": os.path.basename(tmp_path)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5054, debug=True)
