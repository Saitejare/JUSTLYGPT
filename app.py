from flask import Flask, render_template, request, jsonify
import json
import os  # Added missing import

app = Flask(__name__)

# Load legal knowledge base
with open('legal_knowledge.json', encoding='utf-8') as f:
    legal_db = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
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
            if language in case:  # Check if language exists in case data
                response = case[language]['answer']
            else:
                response = case['answer']
            break

    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
