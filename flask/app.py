from chatmodel import KoGPT2                                    # chatmodel 파일의 KoGPT2.py 임포트

from flask import Flask, render_template, jsonify, request      # Flask 관련 라이브러리
import speech_recognition as sr                                 # 음성인식 라이브러리

# 서버 종료 시 동작 코드
# import atexit

# def close():
#    logfile.close()

app = Flask(__name__)

HOST = "0.0.0.0"                                                # host 주소
PORT = "5000"                                                   # port 번호

MAXLEN = 512                                                    # 사용자 입력 최대 길이
QA = []                                                         # 멀티턴 데이터 관리 리스트

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
    data = request.get_json()                                                       # JSON 데이터로부터 사용자 입력 추출
    question = ""
    question += getInput(data['user_input'])                                        # 멀티턴 입력 생성
    response = KoGPT2.generate_response(question, KoGPT2.model, KoGPT2.tokenizer)   # 모델 응답
    QA.append(data['user_input'])                                                   # 멀티턴 데이터 리스트에 사용자 입력 삽입
    QA.append(response)                                                             # 멀티턴 데이터 리스트에 모델 응답 삽입
    # logging(data['user_input'], response)
    return jsonify({"response": response})                                          # JSON 형태로 모델 응답 반환

# 멀티턴 입력 텍스트 만들기 (ABABABABA 형식)
def getInput(input):
    cntQA = len(QA)
    if(cntQA > 0):
        for i in range(cntQA):
            ret = ""
            for j in range(i, cntQA):
                ret += QA[j] + "\t"                                                 # ABABABABA 사이 탭
            ret += input
            if len(ret) < MAXLEN:                                                   # 사용자 입력으로 가능한 최대 길이와 비교
                if(cntQA == 8):                                                     # QA 리스트가 8개면 제일 먼저 들어온 2개의 QA 삭제
                    del QA[:2]
                return ret
    return input                                                                    # QA 리스트가 비었으면(첫 입력) 그대로 반환

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
        recognizer.adjust_for_ambient_noise(source)                             # 노이즈가 있는 음성 데이터 인식
        print("음성 인식 대기중")
        audio = recognizer.listen(source, timeout=3)                            # 음성 인식, 3초 타임 아웃 설정

    try:
        transcript = recognizer.recognize_google(audio, language="ko-KR")       # 구글 API
        return jsonify({"response": transcript})                                # JSON 형태로 음성 인식 결과 반환
    except sr.UnknownValueError:                                                # 음성 인식 오류
        print("인식할 수 없습니다.")
    except sr.RequestError as e:
        print("인식에 문제가 있습니다.", e)

# main
if __name__ == '__main__':
    app.run(host = HOST, port = PORT, debug = True)
    # atexit.register(close)