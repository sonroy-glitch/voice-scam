# 🎙️ Voice Scam Detection

A real-time voice scam detection system that transcribes incoming audio and classifies it as fraudulent or safe using advanced NLP models. This project combines speech-to-text and transformer-based classification to help users identify scam calls with ease.

---

## 🚀 Tech Stack

| Technology       | Role                                                  |
|------------------|-------------------------------------------------------|
| 🧠 RoBERTa        | Pre-trained transformer model for text classification |
| 🤗 Hugging Face   | Model hosting and tokenizer utilities                 |
| 🔊 AssemblyAI     | Speech-to-text transcription of audio input           |
| 🧪 Transformers   | NLP pipeline and model integration                    |
| 🧬 Flask          | Backend API for model inference                       |
| 📊 Streamlit      | Interactive frontend dashboard                        |

---

## 📂 Project Structure

voice-scam/ ├── backend.py # Flask backend for processing and inference ├── frontend.py # Streamlit UI for user interaction ├── config.json # Model configuration ├── requirements.txt # Python dependencies ├── tokenizer_config.json # Tokenizer settings ├── vocab.json # Vocabulary file ├── special_tokens_map.json # Token mapping └── README.md # Project documentation

---

## 🧠 How It Works

1. **Audio Input**: User uploads or records a voice call.
2. **Transcription**: Audio is transcribed to text using AssemblyAI.
3. **Classification**: Transcribed text is passed to RoBERTa via Hugging Face Transformers.
4. **Result Display**: Streamlit dashboard shows whether the call is likely a scam.

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sonroy-glitch/voice-scam.git
   cd voice-scam
🔐 API Keys
Create a .env file to store your API keys:

env
ASSEMBLYAI_API_KEY=your_assemblyai_key
HF_TOKEN=your_huggingface_token
Make sure to load these keys securely in your application.
📈 Future Improvements
Add multilingual support

Integrate real-time call monitoring

Enhance model accuracy with fine-tuning

Add alert system for flagged calls
🤝 Contributing
Pull requests are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a PR.
📄 License
This project is open-source and available under the MIT License.
🙌 Acknowledgements
AssemblyAI

Hugging Face

RoBERTa

Streamlit
