from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os

load_dotenv()  

app = Flask(__name__)

class Resumentexto:
    model_openai = "gpt-3.5-turbo"

    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def resumen(self, texto, idioma):
        response = openai.chat.completions.create(
            model=self.model_openai,
            messages=[
                {"role": "system", "content": f"Eres un asistente que puede leer un texto y resumirlo. El resumen debe ser conciso y detallado y debe estar en {idioma}."},
                {"role": "user", "content": "El texto que quiero resumir es el siguiente:\n" + texto},
            ],
        )
        respuesta = response.choices[0].message['content']
        return respuesta

api_key = os.getenv("OPENAI_API_KEY") 
resumen_texto = Resumentexto(api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resumir', methods=['POST'])
def resumir():
    data = request.get_json()
    texto = data['texto']
    idioma = data['idioma']
    try:
        resumen = resumen_texto.resumen(texto, idioma)
        return jsonify({'resumen': resumen})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
