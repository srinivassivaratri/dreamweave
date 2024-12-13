# DreamWeave

An AI-powered interactive storytelling application that creates dynamic stories with audio narration.

🌐 **Live Demo**: [https://dreamweave-8we6.onrender.com/](https://dreamweave-8we6.onrender.com/)

## Features
- Dynamic story generation using X.AI
- Voice narration using ElevenLabs
- Interactive story progression
- Beautiful, responsive UI

## Setup

1. Clone the repository:
```bash
git clone https://github.com/srinivassivaratri/dreamweave.git
cd dreamweave
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
ELEVENLABS_API_KEY=your_elevenlabs_key
FLASK_SECRET_KEY=your_secret_key
X_AI_API_KEY=your_xai_key
X_AI_API_URL=https://api.x.ai/v1/chat/completions
```

4. Run the application:
```bash
flask run
```

Visit `http://localhost:5000` in your browser.

## Deployment
This application is configured for deployment on Render.com. See `render.yaml` for configuration details. 