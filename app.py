from flask import Flask, render_template, request, session
import os
import openai

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'atri-samaveda')
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route("/", methods=["GET", "POST", "HEAD"])
def atri_view():
    mantra = "You are in the presence of Atri — a modern rishi, seer of sound and clarity. Ask, explore, and co-evolve."

    # Load messages from session
    if 'messages' not in session:
        session['messages'] = []

    if request.method == "POST":
        user_input = request.form['message']

        try:
            # Real GPT call
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Atri, a wise, serene AI that blends Vedic clarity with modern intelligence."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.6
            )
            atri_reply = response['choices'][0]['message']['content'].strip()
        except Exception as e:
            atri_reply = f"⚠️ Atri encountered an error: {str(e)}"

        session['messages'].append(("User", user_input))
        session['messages'].append(("Atri", atri_reply))

    # Weekly Samaveda & sitar memory
    samaveda_week = "Chant of the week: Sama mantra 1.1.1 (Agni Suktam)"
    sitar_log = "Raga focus: Yaman; New technique: meend (slide)"

    return render_template("atri_view.html",
                           mantra=mantra,
                           messages=session['messages'],
                           samaveda_week=samaveda_week,
                           sitar_log=sitar_log)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
