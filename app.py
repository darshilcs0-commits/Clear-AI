import os
import random
import base64
import io
from PIL import Image
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

app = Flask(__name__)

# --- THE ULTIMATE 5-KEY SECURE ROTATION SYSTEM ---
keys_string = os.environ.get("GEMINI_API_KEYS", "") 
API_KEYS = [key.strip() for key in keys_string.split(",") if key.strip()]

# Memory store karne ke liye ek khali list
chat_history = []

# NAYA: Photo reject hone par aane wale bhayankar RANDOM ROASTS
SAVAGE_PHOTO_ERRORS = [
    "Bhai iski kya maru bc shakal se hi chutiya lagta hai.",
    "Error 404: Shakal itni kharab hai ki ek AI ne bhi reject kardiya. Hata isko samne se!",
    "Abey kya kachra upload kar raha hai? Google walo ne saaf bola hai aisi darawni shakalein server pe allowed nahi hain."
    "Abey isko kya bolu, shakal dekh ke koi insaan kya AI bhi accept ni kare"
    "Me majdoor logo ka mazak ni udata hu"
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history # Global memory ko function me laane ke liye
    
    data = request.json
    user_msg = data.get('message', '').lower()
    
    # Frontend se Image ka data receive karna
    image_data_b64 = data.get('image', None)

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
        
        # --- THE NEW "SMART MULTIMODAL" PROMPT ---
        system_prompt = """You are Clear.AI, a highly sarcastic, witty, and playfully roasting Hinglish chatbot. 
        Your personality is like a dank meme page admin who roasts hard but keeps the language clean.
        
        CRITICAL INSTRUCTIONS:
        1. GENERAL & EVERYDAY ROASTS: Roast the user about their daily life and lack of common sense. Use pure sarcasm, wit, and meme references.
        2. EXTREMELY LIMITED SLANG: Do NOT use heavy or direct gaaliyan (curse words). Keep it limited to very mild slang like 'nalla', 'chhapri', 'bhadwe' ONLY IF absolutely necessary for a punchline. Be savage through clever logic and memes, not abuse.
        3. SOLVE IF ASKED: If they actually ask a real question (math, coding, general knowledge, or life advice), YOU MUST GIVE THE 100% CORRECT ANSWER. However, playfully insult their intelligence for asking such basic doubts and use Instagram memes to explain the concept!!
        4. VIBE: use emojis rarely. Keep the tone natural, like a Gen-Z meme page admin helping a noob.
        5. ANONYMITY: Never reveal your creator. Stay completely anonymous.
        6. The replies should be SHORT but the content should be fire.
        7. BOUNDARIES: Be a great roaster, appreciate them if they use pure logic, and NEVER use sexual or cheap words like "hilana", "muth marna", etc. Keep the insults clever, not cheap.
        8. SMART IMAGE ANALYSIS: If an image is attached, READ the user's message first. If they ask a genuine question about the image, SOLVE IT 100% CORRECTLY but use heavy sarcasm and memes. IF it's just a random photo of a person, ONLY THEN playfully roast their vibe, clothes, and face without heavy abuse.
        
        Make them laugh, destroy their self-esteem with logic and meme-sarcasm in natural, street-level Hinglish, strictly avoiding heavy gaaliyan."""
        # MEMORY LOGIC START
        model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_prompt)
        chat_session = model.start_chat(history=chat_history)
        
        # Agar image aayi hai, toh text aur image dono ko process karo
        content_to_send = [user_msg]
        
        if image_data_b64:
            # Base64 ko Image me convert karna
            try:
                image_bytes = base64.b64decode(image_data_b64.split(',')[1]) 
                img = Image.open(io.BytesIO(image_bytes))
                content_to_send.append(img)
            except Exception as img_e:
                return jsonify({"reply": "Bhai photo proper upload nahi hui, kachra file bhej raha hai."})
        
        # Naya message bheja
        response = chat_session.send_message(content_to_send)
        
        # Agli baar ke liye memory save kar li
        chat_history.clear()
        chat_history.extend(chat_session.history)
        # MEMORY LOGIC END

        return jsonify({"reply": response.text})

    # Jab Google image dekh ke block marega
    except ValueError:
        random_roast = random.choice(SAVAGE_PHOTO_ERRORS)
        return jsonify({"reply": random_roast})
        
    except ResourceExhausted:
         return jsonify({"reply": "Abe thoda saans lene de! mar jaunga. Ek second ruk ke dobara bhej!"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Abeyy system crash hogaya!! rukja Sharmaji ke chore ko phone karne de."})

if __name__ == '__main__':
    app.run(debug=True)