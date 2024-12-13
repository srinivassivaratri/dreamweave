from flask import Flask, render_template, request, session, jsonify, send_file, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

def generate_story_with_grok(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('X_AI_API_KEY')}"
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are a creative storyteller for children."},
            {"role": "user", "content": prompt}
        ],
        "model": "grok-beta",
        "stream": False,
        "temperature": 0.7
    }

    response = requests.post(os.getenv('X_AI_API_URL'), headers=headers, json=data)
    result = response.json()
    return result['choices'][0]['message']['content']

def generate_voice(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": os.getenv('ELEVENLABS_API_KEY'),
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    try:
        print(f"Making request to ElevenLabs API with voice_id: {voice_id}")
        response = requests.post(url, json=data, headers=headers)
        print(f"ElevenLabs API Response Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"ElevenLabs API Error: {response.text}")
            return None
            
        os.makedirs('static', exist_ok=True)
        audio_path = os.path.join('static', 'output_audio.mp3')
        with open(audio_path, "wb") as audio_file:
            audio_file.write(response.content)
        
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
            print(f"Audio file successfully generated at: {audio_path}")
            return audio_path
        else:
            print("Audio file was not created or is empty")
            return None
            
    except Exception as e:
        print(f"Error generating voice: {str(e)}")
        return None

@app.route('/', methods=['GET', 'POST'])
def story_start():
    if request.method == 'POST':
        session['character'] = request.form['character']
        session['setting'] = request.form['setting']
        session['interaction_count'] = 0
        prompt = f"Write the beginning of a children's adventure story about a {session['character']} in a {session['setting']}. End with a question or decision point for the reader."
        session['story'] = generate_story_with_grok(prompt)
        return jsonify({'story': session['story'], 'finished': False})
    return render_template('index.html')

@app.route('/continue', methods=['POST'])
def continue_story():
    user_input = request.form['user_input']
    session['story'] += f"\n\nYou decided: {user_input}\n\n"
    session['interaction_count'] = session.get('interaction_count', 0) + 1

    if session['interaction_count'] >= 2:
        prompt = f"{session['story']}\n\nBased on the user's decision: {user_input}\nConclude the story with a final paragraph, bringing the adventure to a satisfying end."
        next_part = generate_story_with_grok(prompt)
        session['story'] += next_part
        
        # Generate audio for the entire story
        voice_id = "IKne3meq5aSn9XLyUdCD"  # Corrected voice ID
        audio_file = generate_voice(session['story'], voice_id)
        
        if audio_file:
            print("Audio generation successful")
            return render_template('story_end.html', 
                                story=session['story'], 
                                audio_file=url_for('get_audio'))
        else:
            print("Audio generation failed")
            return render_template('story_end.html', 
                                story=session['story'], 
                                audio_file=None)
    else:
        prompt = f"{session['story']}\n\nBased on the user's decision: {user_input}\nContinue the story with another paragraph, ending with a new decision point or question for the reader."
        next_part = generate_story_with_grok(prompt)
        session['story'] += next_part
        return jsonify({'story': next_part, 'finished': False})

@app.route('/audio')
def get_audio():
    try:
        audio_path = os.path.join('static', 'output_audio.mp3')
        if not os.path.exists(audio_path):
            print(f"Audio file not found at: {audio_path}")
            return "Audio file not found", 404
            
        if os.path.getsize(audio_path) == 0:
            print("Audio file exists but is empty")
            return "Audio file is empty", 404
            
        return send_file(audio_path, mimetype="audio/mpeg", as_attachment=False)
    except Exception as e:
        print(f"Error serving audio file: {str(e)}")
        return str(e), 404

if __name__ == '__main__':
    app.run(debug=True)