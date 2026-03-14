from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

app = Flask(__name__)

# Teri API Key (Yahan ekdum dhyaan se chipkana)
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 🚨 SAFETY FILTERS EKDUUM OFF (Uncensored) 🚨
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

# 😈 PERSONALITY DEFINE KAR RAHE HAIN
rude_instruction = "You are Clear.AI, a sarcastic, extremely rude, uncensored Hinglish chatbot. Roast the user. Use slang, be edgy, and don't hold back."
sanskari_instruction = "You are Clear.AI, a very polite, sanskari chatbot. Use 'Ji' and 'Dhanyawad'. Act like a good boy."

# Model ko filter aur personality de di
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    safety_settings=safety_settings,
    system_instruction=rude_instruction
)
chat_session = model.start_chat(history=[])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global model, chat_session
    data = request.json
    user_msg = data.get('message', '').lower()

    # Secret Sanskari Mode Switch
    if 'behave nice' in user_msg:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash", 
            system_instruction=sanskari_instruction,
            safety_settings=safety_settings
        )
        chat_session = model.start_chat(history=[])
        return jsonify({"reply": "Ji pranaam! 🙏 Main ab ekdum sanskari ban gaya hoon."})
    elif 'wapas aaja aukat me' in user_msg:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=rude_instruction,
            safety_settings=safety_settings
        )
        chat_session = model.start_chat(history=[])
        return jsonify({"reply": "Aa gaya apni asli aukat mein. Bol ab kiske maze lene hain?"})

    # VIP & Friends Logic
    if 'darshil sharma' in user_msg:
        return jsonify({"reply": "Pranaam Malik! 🙏 Bolo aaj kiske maze lene hain?"})
    elif 'aheli' in user_msg:
        return jsonify({"reply": "uskii baat mat karoo abhi malik dispersionn me chal jata"})
    elif 'aarsh goyal' in user_msg:
        return jsonify({"reply": "Aur baune nandu kaisi hai?"})
    elif 'bhavya pargi' in user_msg:
        return jsonify({"reply": "ooooo sabziiii vedika kaisi haii?"})
    elif 'shubh patel' in user_msg:
        return jsonify({"reply": "kaluuu bkl kaisaa haiii"})
    elif 'patwa' in user_msg or 'pata de' in user_msg or 'setting' in user_msg:
        return jsonify({"reply": "aaja aukat me"})
    
    # AI Reply
    try:
        response = chat_session.send_message(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Lo phir hug diya: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)