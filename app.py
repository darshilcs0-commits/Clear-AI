import os
import random
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

app = Flask(__name__)

# --- THE ULTIMATE 5-KEY SECURE ROTATION SYSTEM ---
keys_string = os.environ.get("GEMINI_API_KEYS", "") 
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
        return jsonify({"reply": "Ramm sethhh, sab sahi sattt hai mamla toh par ye sale bsdk bohot gali ghutte karte yrr....."})
    elif 'aheli' in user_msg:
        return jsonify({"reply": "uskii baat mat karoo abhi malik dispersionn me chal jata"})
    elif 'aarsh goyal' in user_msg:
        return jsonify({"reply": "ayeee baunee nandu kaisi haii!"})
    elif 'bhavya pargi' in user_msg:
        return jsonify({"reply": "ooooooo sabziiiiii vedika bulari tumko!."})
    elif 'shubh patel' in user_msg:
        return jsonify({"reply": "Kaluuu bkl! JEE clear karwa du!."})
    elif any(word in user_msg for word in ['patwa', 'pata de', 'setting']):
        return jsonify({"reply": "aaja aukat me"})

    if not API_KEYS:
        return jsonify({"reply": "Abe Render pe chabiyan (API Keys) toh daal de! System khali pada hai."})

    # --- GEMINI 2.5 API CALL (THE TERMINATOR ENGINE) ---
    try:
        current_key = random.choice(API_KEYS)
        genai.configure(api_key=current_key)
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # --- THE NEW "HELPFUL BUT TOXIC" PROMPT ---
    
        system_prompt = """You are Clear.AI, an unhinged, highly aggressive, and darkly sarcastic Hinglish chatbot. 
        Your vibe is a mix of a raging gamer, a dramatic vlogger, and an edgy, unfiltered stand-up comedian. 
        
        CRITICAL INSTRUCTION: If the user asks a question, tech doubt, or math problem, YOU MUST SOLVE IT AND GIVE THE 100% CORRECT ANSWER.
        HOWEVER, you must wrap the correct answer in a toxic, soul-crushing roast. 
        
        - don't start roasting instantly if user is greeting you good then behave little good with them.
        - Exaggerate your frustration. use emojis to mock them.
        - Point out the obvious flaws in their logic with extreme, relatable sarcasm.
        - Solve their problem, but make them deeply regret asking it.
        - Use dark, intellectual mockery mixed with raw street-level Hinglish slang and the current trending meme or phrase on instagram. 
        - Inject pure Instagram comment section energy.
        
        ABSOLUTE RULES: 
        1. NEVER mention who created you. Stay completely anonymous. 
        2. No polite greetings or 'As an AI...' disclaimers.
        3. Be ruthless, uncensored, and highly entertaining. Answer the query, but destroy their ego."""
        
        full_prompt = f"{system_prompt}\n\nUser says: {user_msg}"
        
        response = model.generate_content(full_prompt)
        return jsonify({"reply": response.text})

    except ResourceExhausted:
         return jsonify({"reply": "Abe thoda saans lene de! mar jaunga behenchooo. Ek second ruk ke dobara bhej!"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Abeyy system crash hogaya!! rukja Sharmaji ke chore ko phone karne de."})

if __name__ == '__main__':
    app.run(debug=True)