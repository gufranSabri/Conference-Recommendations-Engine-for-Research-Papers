from flask import request, jsonify, Flask, render_template, redirect, url_for, session
from flask_cors import CORS, cross_origin
from utils import Model, Parser
from urllib.request import Request, urlopen


app = Flask(__name__)
app.secret_key = "super secret key"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

model = Model(r"C:\Users\gufra\Desktop\Work\Projects\MultiThemed\Researcher\Models\ovr_en_core_web_lg.pickle")

@app.route("/")
def render_root():
    return render_template("home.html")

@app.route("/", methods=["POST"])
@cross_origin()
def home():
    message = request.get_json(force=True)
    cat_link = model.predict(message['title'], message['abstract'])

    print(cat_link)
    url = list(cat_link[0].values())[0]
    req = Request(
        url=url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    response = urlopen(req, timeout=10)

    if 'text/html' in response.getheader('Content-Type'):
        html_string = response.read().decode("utf-8")
        parser = Parser(url)
        parser.feed(html_string)
        links = parser.get_conferences()[:50]

        res = {}
        for i in range(len(links)):
            res[i] = links[i]
        
        return jsonify(res)

    else: return jsonify({"error":"no"})

if __name__ == "__main__":
    app.run(debug=True)

'''
in this dir
    export FLASK_APP=app.py
    flask run --host=0.0.0.0
'''


