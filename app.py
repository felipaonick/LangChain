# creaimo un web server che ottine una post request con il nome in input ed esegue le chain che desideriamo
# ed ottiene le info circa il nome della persona che abbiamo dato in input e ce le restituisce come servizio
# utilizziamo Flask per creare tale web server

from dotenv import load_dotenv
# carichiamo le variabili d'ambiente

#per creare la Flask application, per rendere (prestare) il codice HTML, request per comunicare, e jsonfy per prendere un dict con le info della persona
# e lo converte in un JSON che è utile per la parte frontend
from flask import Flask, render_template, request, jsonify

from ice_breaker.ice_breaker import ice_breaker_with

load_dotenv()

#settiamo un basic Flask web server

app = Flask(__name__)

"""
    @app.route is a decorator used to register a view function for a specific URL rule.
    When a user sends a request to that URL, the corresponding function is executed.
    Typically used for defining views in Flask.
    You’ve already created one route—the root route '/'
"""
@app.route("/")
def index():
    # restituisce il codice html per la parte di frontend dell'app
    return render_template("index.html")

"""endpoint per eseguire la chain"""
@app.route("/process", methods=['POST'])
def process():
    #ottiene il nome dalla request
    name = request.form['name']
    summary, profile_pic_url = ice_breaker_with(name=name)
    return jsonify({
        "summary_and_facts": summary.to_dict(),
        "picture_url": profile_pic_url
    })


if __name__ == "__main__":

    app.run(host='localhost', debug=True)