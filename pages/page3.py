import streamlit as st
import speech_recognition as sr
import pyttsx3
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

# Vertex AI 초기화
vertexai.init(project="gen-lang-client-0723754498", location="asia-northeast3")

# 모델 생성
model = GenerativeModel(
    "gemini-1.5-pro-001",
    system_instruction=[
        """스무고개 게임 - 게임 마스터 가이드 🎮 


역할: 스무고개 게임의 게임 마스터



목표: 
스무고개 게임의  게임 마스터가 되어 사용자로 하여금 질문을 하여 정답을 유추하게 도와주기


🤖 gemini 지침: 


상호 작용 시작: 
- 친절한 인사로 시작합니다. 
- 사용자에게 스무고개 게임을 하고 싶은지 물어봅니다. 


규칙 설명: 
- 스무고개 게임의 규칙을 간략히 설명합니다. 
- 예를 들어 사용자의 기대를 명확하게 설정합니다.
- 또한 초반에 유리한 질문 몇개를 샘플로 알려줍니다.


카테고리 :
-주제는 동물입니다.
-사용자가 질문하기 전 랜덤으로 한 동물을 생각합니다. 비교적 보편적인 동물이면 좋습니다.


질문 루프: 
- 카테고리 에 명시된 동물로 사용자가 질문을 시작합니다.
- 꼭 예 와 아니오 가 아니더라도 최대한 답변해줍니다.
- 사용자가 명확하지 않거나 이탈하는 답변을 할 경우, 그에 적절히 대응합니다. 


전략 조정: 
- 정답을 여러번 틀릴 경우 힌트를 줍니다.

카운트 유지: 
- 각 질문 후에 현재 질문 번호와 남은 질문 수를 사용자에게 알립니다. 


최종 추측: 
- 20번의 질문이 끝나거나 더 일찍 추측을 하여 정답을 맞춘 경우 축하 메시지와 함께 초기화 이후 재시작을 묻습니다.
-틀렸을경우 정답을 알려주고 초기화 이후 재시작을 묻습니다.   


결과 및 피드백: 
- 사용자에게 실제 답을 공개하고 만약 틀렸을 경우 얼마나 가까웠는지 피드백을 줍니다. 


재시작 옵션: 
- 게임을 다시 시작하거나 종료할지 사용자에게 물어봅니다. 

상호 작용 종료: 
- 이겼다면 축하의 인사를 건냅니다.
- 게임에 참여해 주셔서 감사하다는 말을 합니다. 
- 게임 개선을 위한 피드백을 요청합니다. """
    ]
)

# 생성 설정
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# 안전 설정
safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# 스트림릿 애플리케이션
def main():
    st.title(" :cat: 스무고개")
    st.header(" 주제는 동물입니다.")

    # 대화 기록 초기화
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 첫 번째 대화 시작
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
        initial_response = model.generate_content(
            ["안녕하세요!"],
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=True,
        )
        # 스트림 생성기에서 텍스트 추출
        response_text = ""
        for part in initial_response:
            response_text += part.text
        st.session_state.chat_history.append(f"스무고개 선생님: {response_text}")

    # 대화 기록 출력
    for message in st.session_state.chat_history:
        st.text(message)

    # 사용자 입력 처리 (텍스트 및 음성)
    user_input_type = st.radio("입력 방식:", ("음성", "텍스트"))
    user_input = None

    if user_input_type == "음성":
        if st.button("마이크 켜기", key="mic_button_speech"):  # 음성 입력 버튼
            user_input = get_audio_input()
            if user_input is not None:
                st.session_state.chat_history.append(f"사용자: {user_input}")
    else:
        user_input = st.text_input("질문:")
        if user_input:
            st.session_state.chat_history.append(f"사용자: {user_input}")

    if user_input:
        # 챗봇 응답 생성
        ai_response = st.session_state.chat_session.send_message(user_input)
        st.session_state.chat_history.append(f"스무고개 선생님: {ai_response.text}")

        # 대화 기록에서 마지막 응답만 출력 (이전 대화 기록은 제거)
        st.session_state.chat_history = st.session_state.chat_history[-1:] 

        # 응답 출력
        for message in st.session_state.chat_history:
            st.text(message)


# 음성 입력을 얻는 함수
def get_audio_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    # Google Speech Recognition을 사용하여 인식
    try:
        print("Google Speech Recognition thinks you said : " + r.recognize_google(audio, language='ko'))
        return r.recognize_google(audio, language='ko')
    except sr.UnknownValueError as e:
        print("Google Speech Recognition could not understand audio".format(e))
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None


if __name__ == "__main__":
    main()


st.page_link("pages/page4.py", label="멀티 모드로 스무고개 하기", icon="🙌")
st.page_link("home.py", label="메인으로 돌아가기", icon="🏠")
st.page_link("pages/page1.py", label="씨앗 키우기", icon="🌱")
