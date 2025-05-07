from flask import Flask, render_template, request, jsonify
import json
import os
import signal
import sys

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False  # Reduces response size

# Graceful shutdown handler
def handle_exit(signum, frame):
    print("\nGracefully shutting down...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_exit)

# Load legal knowledge base
def load_legal_data():
    with open('legal_knowledge.json', encoding='utf-8') as f:
        return json.load(f)

legal_db = load_legal_data()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_query = request.form['query'].lower()
        language = request.form.get('language', 'en')
        
        # Default responses
        default_responses = {
            'en': "Sorry, I couldn't find an answer. Try asking about 'divorce', 'wages', or 'property'.",
            'hi': "क्षमा करें, मुझे जवाब नहीं मिला। 'तलाक', 'वेतन' या 'संपत्ति' के बारे में पूछें।",
            'te': "క్షమించండి, నాకు సమాధానం కనుగొనబడలేదు. 'డివోర్స్', 'వేతనాలు' లేదా 'ఆస్తి' గురించి అడగండి."
        }
        
        response = default_responses.get(language, default_responses['en'])

        # Search for matching legal case
        for case in legal_db['legal_cases']:
            if any(keyword in user_query for keyword in case['keywords']):
                if language in case:
                    response = case[language]['answer']
                else:
                    response = case['answer']
                break

        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
