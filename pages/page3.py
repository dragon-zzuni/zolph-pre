import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai 


genai.configure(api_key="AIzaSyBTUy0-FYt9dofqdTZRY-jtNPuz2WGEm00")

generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def main():
    st.title(" :cat: 스무고개")
    st.header(" 주제는 동물입니다.")
    st.write("5번의 기회를 통해 어떠한 동물일지 맞춰보아요!")


    def text_to_speech(text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    
    # 음성 입력을 위한 함수
    def get_audio_input():
        r = sr.Recognizer()

        with sr.Microphone() as source:
            audio = r.listen(source)

        # 구글 웹 음성 API로 인식하기 
        try:
            print("Google Speech Recognition thinks you said : " + r.recognize_google(audio, language='ko'))
            return r.recognize_google(audio, language='ko')
        except sr.UnknownValueError as e:
            print("Google Speech Recognition could not understand audio".format(e))
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None

    # 챗봇 응답을 얻는 함수
    def get_chatbot_response(user_input):
        if "chat_session" not in st.session_state:
            st.session_state["chat_session"] = model.start_chat(history=[])

        ai_response = st.session_state.chat_session.send_message(user_input)
        return ai_response.text
    
    

     # User input handling (text and speech)
    user_input_type = st.radio("입력 방식:", ("음성", "텍스트"))
    

    if user_input_type == "음성":
        if st.button("마이크 켜기", key="mic_button_speech"):  # Unique key for speech input
            user_input = get_audio_input()
            if user_input is not None:
                st.text(f"사용자: {user_input}")
                chatbot_response = get_chatbot_response(user_input)
                st.text(f"AI: {chatbot_response}")
                text_to_speech(chatbot_response)
    else:
        user_input = st.text_input("사용자 질문:")
        if user_input:
            st.text(f"사용자: {user_input}")
            chatbot_response = get_chatbot_response(user_input)
            st.text(f"AI: {chatbot_response}")
            text_to_speech(chatbot_response)

 
    

if __name__ == "__main__":
    main()

st.page_link("pages/page4.py", label="멀티 모드로 스무고개 하기", icon="🎮")
st.page_link("home.py", label="메인으로 돌아가기", icon="🏠")
st.page_link("pages/page1.py", label="씨앗 키우기", icon="🌱")
