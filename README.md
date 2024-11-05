# Real-Time Minutes of Meeting (MoM) Generator

A powerful FastAPI-based web application that revolutionizes meeting documentation by combining real-time audio transcription via Deepgram with intelligent summarization using OpenAI's API. This tool automatically generates structured meeting minutes, helping teams capture and organize important meeting content effortlessly.

## 🚀 Features

### Core Functionality
- **Real-Time Audio Transcription**
  - WebSocket-based audio streaming
  - Low-latency transcription using Deepgram's API
  - Support for multiple speakers detection
  - Real-time text display during meetings

### AI-Powered Summary Generation
- **Intelligent Meeting Minutes**
  - Automatic extraction of key discussion points
  - Action item identification and assignment
  - Decision tracking and documentation
  - Meeting context preservation
  - Priority-based content organization

### User Interface
- **Intuitive Web Interface**
  - Clean, responsive design
  - Real-time transcription display
  - Meeting controls (start/stop/pause)
  - Summary preview and export options

## 🛠️ Technical Architecture

### Project Structure
```plaintext
mom_realtime/
│
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── routes/
│   │   ├── websocket.py        # WebSocket handling
│   │   └── api.py             # REST API endpoints
│   │
│   ├── services/
│   │   ├── transcription.py    # Deepgram integration
│   │   └── summarization.py    # OpenAI integration
│   │
│   ├── models/
│   │   └── schemas.py          # Data models and schemas
│   │
│   └── static/                 # Static assets
│       ├── css/
│       ├── js/
│       └── index.html
│
├── tests/                      # Test suite
├── .env                        # Environment configuration
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

## 📋 Prerequisites

- Python 3.8+
- Deepgram API key
- OpenAI API key
- Modern web browser with WebSocket support

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mom-realtime.git
   cd mom-realtime
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🔧 Configuration

Create a `.env` file with the following variables:
```plaintext
DEEPGRAM_API_KEY=your_deepgram_api_key
OPENAI_API_KEY=your_openai_api_key
WEBSOCKET_PORT=8000
```

## 🎯 Usage

1. Open your browser and navigate to `http://localhost:8000`
2. Click "Start Meeting" to begin audio recording
3. Speak naturally - the application will transcribe in real-time
4. End the meeting to generate the summary
5. Review and export the meeting minutes

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 API Documentation

### WebSocket Endpoints

- `GET /ws/audio`
  - Handles real-time audio streaming
  - Expects binary audio data
  - Returns transcription results

### REST Endpoints

- `POST /api/summary`
  - Generates meeting summary
  - Request body: `{ "transcript": "string" }`
  - Returns structured MoM

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [Deepgram](https://deepgram.com/) for real-time transcription
- [OpenAI](https://openai.com/) for text summarization
- [FastAPI](https://fastapi.tiangolo.com/) framework

## 📞 Support

For support, email support@example.com or open an issue in the repository.

## 🔮 Future Enhancements

- Multi-language support
- Custom summarization templates
- Meeting analytics dashboard
- Integration with calendar apps
- Export to various formats (PDF, DOCX, etc.)
