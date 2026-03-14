import os
import random
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

app = Flask(__name__)

# --- THE ULTIMATE 5-KEY SECURE ROTATION SYSTEM ---
# This securely grabs the comma-separated keys from Render's Environment Variables
keys_string = os.environ.get("GEMINI_API_KEYS", "") 

# This cleans up the string and turns it into a proper Python list
API_KEYS = [key.strip() for key in keys_string.split(",") if key.strip()]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get('message', '').lower()

    # --- PERSONALITY & CUSTOM ROAST LOGIC ---
    if 'darshil sharma' in user_msg:
        return jsonify({"reply": "Pranaam Malik! 🙏 Ratlam ke tech-don, batao aaj kiske maze lene hain?"})
    elif 'aheli' in user_msg:
        return jsonify({"reply": "uskii baat mat karoo abhi malik dispersionn me chal jata"})
    elif 'aarsh goyal' in user_msg:
        return jsonify({"reply": "Wo bauna nandu? Wo abhi tak Complan pee raha hai!"})
    elif 'bhavya pargi' in user_msg:
        return jsonify({"reply": "Oho! Vedika ki sabzi wala? Uska toh ho gaya kalyan."})
    elif 'shubh patel' in user_msg:
        return jsonify({"reply": "Kaluuu bkl! Uske liye toh andhera hi kaafi hai."})
    elif any(word in user_msg for word in ['patwa', 'pata de', 'setting']):
        return jsonify({"reply": "aaja aukat me"})

    # Safety check: If Render keys are missing, it tells you instead of crashing
    if not API_KEYS:
        return jsonify({"reply": "Abe Render pe chabiyan (API Keys) toh daal de! System khali pada hai."})

    # --- GEMINI 2.5 API CALL (THE TERMINATOR ENGINE) ---
    try:
        # Picks a random key for every single message to distribute the load
        current_key = random.choice(API_KEYS)
        genai.configure(api_key=current_key)
        
        # Using the absolute latest and fastest model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        system_prompt = "You are Clear.AI, a rude, sarcastic, and funny Hinglish chatbot. You are created by Darshil Sharma. Roast the user brutally using Indian slang like 'chomu', 'bkl', 'chamcha'. Keep it short and punchy."
        full_prompt = f"{system_prompt}\n\nUser says: {user_msg}"
        
        response = model.generate_content(full_prompt)
        return jsonify({"reply": response.text})

    except ResourceExhausted:
         # Catches the 429 rate limit error safely
         return jsonify({"reply": "Abe thoda saans lene de! Machine gun ki tarah message pel raha hai. Ek second ruk ke dobara bhej!"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Abeyy system crash hogaya!! rukja Sharmaji ke chore ko phone karne de."})

if __name__ == '__main__':
    app.run(debug=True)