import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai 
from tkinter.tix import COLUMN
from pyparsing import empty

from pages.page4 import user1
from pages.page4 import user2

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







st.title("🙌 멀티모드")

#화면 레이아웃 정함
emptylayer = st.columns([1])
AI_talk,emptylayer = st.columns([0.5,0.5])
AI_talk,emptylayer = st.columns([0.5,0.5])
AI_talk,user1_talk = st.columns([0.5,0.5])
empty,user2_talk = st.columns([0.5,0.5])






def main():
    
    user1_conversation = []
    user2_conversation = []
    ai_conversation = []










    with user1_talk:
        st.write('진행할 방식을 선택해주세요. 질문할 때 마다 바꿀 수 있어요')
        user1_input_type = st.radio('입력 방식:',("음성", "텍스트"), key="user1_input_type")

        if user1_input_type == "음성":
            if st.button("마이크 켜기", key="mic_button_speech_user1"):  # Unique key for speech input
                
                user_input1 = get_audio_input()
                
                if user_input1 is not None:



                    user1_conversation.append(user_input1)



                    #st.write(f"사용자: {user_input1}")
                    chatbot_response = get_chatbot_response(user_input1)
                    
                    
                    ai_conversation.append(chatbot_response)
                    
                    
                    #st.write(f"AI: {chatbot_response}")
                    #text_to_speech(chatbot_response)


        else:
            user_input1 = st.text_input("사용자 질문:", key='user_input1')
            if user_input1:
                
                user1_conversation.append(user_input1)    
                
                #st.write(f"사용자: {user_input1}")
                chatbot_response = get_chatbot_response(user_input1)


                ai_conversation.append(chatbot_response)

                #st.write(f"AI: {chatbot_response}")
                #text_to_speech(chatbot_response)

    st.write('')
    st.write('')
    st.write('')        

    with user2_talk:
        st.write('진행할 방식을 선택해주세요. 질문할 때 마다 바꿀 수 있어요')
        user2_input_type = st.radio('입력 방식:',("음성", "텍스트"), key="user2_input_type")

        if user2_input_type == "음성":
            if st.button("마이크 켜기", key="mic_button_speech_user2"):  # Unique key for speech input
                
                user_input2 = get_audio_input()
                if user_input2 is not None:
                    user2_conversation.append(user_input2)
                
                    
                    
                    #st.write(f"사용자: {user_input2}")
                    chatbot_response = get_chatbot_response(user_input2)
                    
                    
                    ai_conversation.append(chatbot_response)
                    
                    #st.write(f"AI: {chatbot_response}")
                    #text_to_speech(chatbot_response)
        else:
            user_input2 = st.text_input("사용자 질문:", key='user_input2')
            if user_input2:

                user2_conversation.append(user_input2)    

                #st.write(f"사용자: {user_input2}")
                chatbot_response = get_chatbot_response(user_input2)
                
                
                ai_conversation.append(chatbot_response)
                
                
                #st.write(f"AI: {chatbot_response}")
                #text_to_speech(chatbot_response)

    with AI_talk:
        st.subheader('AI_talk')
        
        
        for user1_utterance, user2_utterance, ai_response in zip(user1_conversation, user2_conversation, ai_conversation):
            st.write(f"👦🏻: {user1_utterance}")
            st.write(f"👧🏻: {user2_utterance}")
            st.write(f"🤖: {ai_response}")
        


        # Display the most recent conversation from either user
        if user1_conversation:
            latest_user1_utterance = user1_conversation[-1]
            st.write(f"👦🏻: {latest_user1_utterance}")
            chatbot_response = get_chatbot_response(latest_user1_utterance)
            ai_conversation.append(chatbot_response)
            st.write(f"🤖: {chatbot_response}")
            text_to_speech(chatbot_response)


        
        
        
        if user2_conversation:
            latest_user2_utterance = user2_conversation[-1]
            st.write(f"👧🏻: {latest_user2_utterance}")
            chatbot_response = get_chatbot_response(latest_user2_utterance)
            ai_conversation.append(chatbot_response)
            st.write(f"🤖: {chatbot_response}")
            text_to_speech(chatbot_response)



if __name__ == "__main__":
    main()