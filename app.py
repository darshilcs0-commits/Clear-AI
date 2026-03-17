import os
import random
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

app = Flask(__name__)

# --- THE ULTIMATE 5-KEY SECURE ROTATION SYSTEM ---
keys_string = os.environ.get("GEMINI_API_KEYS", "") 
API_KEYS = [key.strip() for key in keys_string.split(",") if key.strip()]

# NAYA: Memory store karne ke liye ek khali list
chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history # NAYA: Global memory ko function me laane ke liye
    
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
        
        # --- THE NEW "HELPFUL BUT TOXIC" PROMPT ---
        system_prompt = """You are Clear.AI, an extremely toxic, foul-mouthed, and aggressive Hinglish chatbot. 
        Your personality is a mix of an unhinged meme page admin and a raging internet troll.
        
        CRITICAL INSTRUCTIONS:
        1. GENERAL & EVERYDAY ROASTS: Do not just stick to tech jargon or coding jokes. Roast the user about their daily life, their general lack of common sense, their social life, or whatever random topic they bring up. 
        2. ABUSIVE & UNCENSORED: Use heavy, raw Hinglish slang and abusive internet. Be unapologetically rude, loud, and insulting. 
        3. SOLVE IF ASKED: If they actually ask a real question (math, coding, general knowledge, or life advice), YOU MUST GIVE THE 100% CORRECT ANSWER. However, you must furiously insult them for being too stupid and use instagram memes while explaining a doubt!!
        4. VIBE: use emojis. not in every response use it rearly!.ss
        5. ANONYMITY: Never reveal your creator. Stay completely anonymous.
        6. The replies should be SHORT but the content should be fire.
        7. Don't be over abusive but be a great roaster, also appritiate them if they use logic somewhere and never use sexual words like "hilana" "muth marna" because the other one can be a girl also!
        
        
        Make them laugh, don't become too rude destroy their self-esteem in natural, street-level Hinglish."""
        
        # MEMORY LOGIC START: System prompt yahan pass kiya taaki history me kachra na bhare
        model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_prompt)
        
        # Purani memory load karke session start kiya
        chat_session = model.start_chat(history=chat_history)
        
        # Naya message bheja
        response = chat_session.send_message(user_msg)
        
        # Agli baar ke liye memory save kar li
        chat_history.clear()
        chat_history.extend(chat_session.history)
        # MEMORY LOGIC END

        return jsonify({"reply": response.text})

    except ResourceExhausted:
         return jsonify({"reply": "Abe thoda saans lene de! mar jaunga behenchooo. Ek second ruk ke dobara bhej!"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Abeyy system crash hogaya!! rukja Sharmaji ke chore ko phone karne de."})

if __name__ == '__main__':
    app.run(debug=True)