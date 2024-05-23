import time
import streamlit as st
import google.generativeai as genai 
import random

def stream_data():
    for word in ("스무 고개에 오신것을 환영합니다. 랜덤 주제가 주어지며 스무고개를 음성이나 텍스트로 진행해 주세요 기회는 총 5번이며 마지막 시도에는 힌트를 사용할 수 있습니다."):
        yield word + ""
        time.sleep(0.05)
        has_executed_stream_data = True

st.title(" :dog: :blue[스무고개]")
st.write_stream(stream_data)

if "has_executed_stream_data" not in st.session_state:
      st.session_state["has_executed_stream_data"] = True


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

def get_random_topic(prompt="랜덤 주제를 선택해 주세요."):
    possible_topics = ["동물", "음식", "나라", "물건", "영화"]

    # Try using generate_text, fallback to a random topic from the list
    try:
        # Check for the latest method name for text generation
        if hasattr(model, "generate_text"):
            response = model.generate_text(prompt=prompt, temperature=0.9, top_p=1)
            random_topic = response.text
        else:
            raise AttributeError("GenerativeModel object has no attribute for text generation.")
    except (AttributeError, Exception) as e:
        # Handle potential errors and fallback to a random topic
        print(f"Error generating topic: {e}")
        random_topic = random.choice(possible_topics)  # Import the random module

    # Select a random topic from the generated text or list
    random_topic_index = int(random_topic.strip()) % len(possible_topics) if random_topic.isdigit() else 0
    return possible_topics[random_topic_index]


with st.status("주제 선정중...", expanded=True) as status:
    st.write("주제 선별중...")
    time.sleep(2)
    st.write("데이터 확인중...")
    time.sleep(2)

    # Generate and display the random topic
    random_topic = get_random_topic()
    st.write(f"주제는 **{random_topic}**입니다!!")
    time.sleep(1)
    status.update(label=f"주제 선정 완료! 주제는 {random_topic} 입니다!", state="complete", expanded=False)

    st.button("다시 선정 하기", on_click=get_random_topic)


level = st.slider("난이도를 선택해 주세요 0으로 갈수록 쉽고 10으로 갈수록 어렵습니다. ",0,10,5)
st.write("난이도는",level,"입니다.")

    
st.page_link("pages/page3.py", label="스무고개 시작", icon="🎮")
   