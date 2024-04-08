from chatmodel import KoGPT2    # chatmodel 파일의 KoGPT2.py 임포트

from flask import Flask, render_template, jsonify, request
import speech_recognition as sr

# 서버 종료 시 동작 코드
# import atexit

# def close():
#    logfile.close()

app = Flask(__name__)

HOST = "0.0.0.0"
PORT = "5000"

MAXLEN = 512
QA = []

# logfile = open("./logs/log.txt", "w")

# 초기 화면 인터페이스 연결
@app.route("/")
def index():
    return render_template("index.html")

# 챗봇 화면 연결
@app.route("/chat")
def chat():
    return render_template("chat.html")

# model 예측
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    data = request.get_json()  # JSON 데이터로부터 user_input 추출
    question = ""
    question += getInput(data['user_input'])
    response = KoGPT2.generate_response(question, KoGPT2.model, KoGPT2.tokenizer)
    QA.append(data['user_input'])
    QA.append(response)
    # logging(data['user_input'], response)
    return jsonify({"response": response})

# 멀티턴 입력 텍스트 만들기
def getInput(input):
    cntQA = len(QA)
    if(cntQA > 0):
        for i in range(cntQA):
            ret = ""
            for j in range(i, cntQA):
                ret += QA[j] + "\t"     # ABABABABA 사이 탭
            ret += input
            if len(ret) < MAXLEN:
                if(cntQA == 8):
                    del QA[:2]
                return ret
    return input

# 로그 작성
# def logging(input, response):
    # logfile.write("User: " + input + "\n")
    # logfile.write("Frieden: " + response + "\n")
    # logfile.flush()

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
        return jsonify({"response": transcript})
    except sr.UnknownValueError:
        print("인식할 수 없습니다.")
    except sr.RequestError as e:
        print("인식에 문제가 있습니다.", e)

# main
if __name__ == '__main__':
    app.run(host = HOST, port = PORT, debug = True)
    # atexit.register(close)