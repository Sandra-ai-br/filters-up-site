from flask import Flask, render_template, request
from datetime import date, datetime
import pandas as pd
import os

app = Flask(__name__)

def carregar_editais():
    df = pd.read_csv('editais.csv')
    df['data_limite'] = pd.to_datetime(df['data_limite']).dt.date
    hoje = date.today()
    return df[df['data_limite'] >= hoje]

def responder_agente(idade, genero, tipo, continente, pais, encontrados):
    if idade <= 25:
        incentivo = "É uma excelente fase para ousar, aprender e crescer."
    elif idade <= 40:
        incentivo = "Você está num momento estratégico para acelerar sua startup."
    else:
        incentivo = "Sua experiência pode transformar ideias em realidades sólidas."

    if encontrados == 0:
        return f"Mesmo sem editais disponíveis no momento para {tipo} em {pais}, continue firme. O cenário está sempre mudando."

    return f"Para uma pessoa de {idade} anos, gênero {genero}, com uma startup em {tipo} sediada em {pais} ({continente}), foram encontrados {encontrados} edital(is). {incentivo}"

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = []
    resposta_ia = ""

    if request.method == 'POST':
        idade = int(request.form['idade'])
        genero = request.form['genero']
        if genero == 'Outro':
            genero = request.form['genero_outro']
        tipo = request.form['tipo']
        continente = request.form['continente']
        pais = request.form['pais']

        editais = carregar_editais()
        filtrados = editais[
            (editais['continente'].str.lower() == continente.lower()) &
            ((pais.lower() == 'todos') | (editais['pais'].str.lower() == pais.lower())) &
            (editais['estagio'].str.lower().str.contains(tipo.lower()))
        ]
        resultados = filtrados.to_dict(orient='records')
        resposta_ia = responder_agente(idade, genero, tipo, continente, pais, len(resultados))

    return render_template('index.html', resultados=resultados, resposta_ia=resposta_ia)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
