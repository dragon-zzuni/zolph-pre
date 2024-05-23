import pyttsx3

engine = pyttsx3.init()
engine.setProperty('voice', 'espeak')  # `espeak`를 사용하도록 설정
engine.setProperty('rate', 150)  # 발음 속도 설정
engine.setProperty('volume', 1.0)  # 볼륨 설정