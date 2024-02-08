from flask import Flask, render_template, jsonify
import pickle

# 1
model = pickle.load(open('KoGPT2_003.pkl', 'rb'))

# # 2
# with open('KoGPT2_003.pkl', 'rb') as f:
#     model = pickle.load(f)


app = Flask(__name__)

hostAddr = "127.0.0.1"
portNum = 8000

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
    response = model.predict("단체생활 적응이 안돼.")
    return jsonify({
       "response": response
    })

if __name__ == '__main__':
    # 3
    # model = pickle.load(open('KoGPT2_003.pkl', 'rb'))

    # 4
    # with open('KoGPT2_003.pkl', 'rb') as f:
    #     model = pickle.load(f)

    app.run(host=hostAddr, port=portNum, debug=True)