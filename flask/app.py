from chatmodel import KoGPT2    # chatmodel 파일의 KoGPT2.py 임포트

from flask import Flask, render_template, jsonify, request
import speech_recognition as sr
# from torchvision import models
# import torch
# import torchvision.transforms as transforms

app = Flask(__name__)

localHost = "127.0.0.1"
serverHost = "0.0.0.0"
serverPort = "5000"

# 초기 화면 인터페이스 연결
@app.route("/")
def index():
    return render_template("index.html")

# model 예측
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    data = request.get_json()  # JSON 데이터로부터 user_input 추출
    question = data['user_input']
    response = KoGPT2.generate_response(question, KoGPT2.model, KoGPT2.tokenizer)
    return jsonify({"response": response})

# 음성 인식
@app.route("/voice", methods=["GET", "POST"])
def voiceRecognition():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("음성 인식 대기중")
        audio = recognizer.listen(source, timeout=3)

    try:
        transcript = recognizer.recognize_google(audio, language="ko-KR")
        print(transcript)
        return jsonify({"response": transcript})
    except sr.UnknownValueError:
        print("인식할 수 없습니다.")
    except sr.RequestError as e:
        print("인식에 문제가 있습니다.", e)

if __name__ == '__main__':
    app.run(host = serverHost, port = serverPort, debug = True)