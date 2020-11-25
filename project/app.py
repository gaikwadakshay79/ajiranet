from flask import Flask, request
import json

from models import Network

app = Flask(__name__)

network = Network()

@app.route("/ajiranet/process",methods= ["POST"] )
def process():
    req_data = request.get_data(as_text=True)
    response = network.parse(req_data)
    return json.dumps(response.msg), response.status, {'ContentType':'application/json'}

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)