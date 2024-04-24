import streamlit as st
import openai
from datetime import datetime

## 기능 구현 함수
def ask_gpt(prompt, model, apikey):
    client = openai.OpenAI(api_key = apikey)
    response = client.chat.completions.create(
        model=model,
        messages=prompt)
    gptResponse = response.choices[0].message.content
    return gptResponse
    

## 메인 함수
def main():
    # 기본 설정
    st.set_page_config(
        page_title="ChatGPT 텍스트 비서 서비스",
        layout="wide"
    )

    # 제목
    st.header("ChatGPT 텍스트 비서 서비스")

    # 구분선
    st.markdown("---")

    # 기본 설명
    with st.expander("ChatGPT 텍스트 비서 서비스에 관하여", expanded=True):
        st.write(
        """
        - 텍스트 입력창에 질문을 적고, 텍스트 질문 버튼을 누르세요.
        - 질문/답변을 확인하실 수 있을거에요.
        """
        )
        
        st.markdown("")

    # session state 초기화
    if "chat" not in st.session_state:
        st.session_state["chat"] = []

    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""
        
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]

    if "check_text" not in st.session_state:
        st.session_state["check_reset"] = False

    # 사이드바 생성
    with st.sidebar:

        # Open AI API 키 입력받기
        st.session_state["OPENAI_API"] = st.text_input(label="OPENAI API 키", placeholder="Enter Your API key", value="", type="password")

        st.markdown("---")

        # GPT 모델을 선택하기 위한 라디오 버튼 생성
        model = st.radio(label="GPT 모델", options=["gpt-4", "gpt-3.5-turbo"])

        st.markdown("---")

        # 리셋 버튼 생성
        if st.button(label="초기화"):
            # 리셋 코드
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]
            st.session_state["check_reset"] = True

    
    # 기능 구현 공간
    col1, col2 = st.columns(2)
    with col1:
        # 왼쪽 영역 작성
        st.subheader("질문하기")

        # 텍스트 입력창
        text_input = st.text_input(label="아래에 텍스트를 입력하세요")
        if (st.button(label="텍스트 질문")) and (st.session_state["check_reset"] == False):
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"]+[("user",now, text_input)]
            st.session_state["messages"] = st.session_state["messages"]+[{"role": "user", "content": text_input}]

    with col2:
        # 오른쪽 영역 작성
        st.subheader("질문/답변")
        if (text_input) and (st.session_state["check_reset"] == False):
            # 답변 얻기
            response = ask_gpt(st.session_state["messages"], model, st.session_state["OPENAI_API"])

            # 답변 내용 저장
            st.session_state["messages"] = st.session_state["messages"]+ [{"role": "assistant", "content": response}]

            # 채팅 시각화를 위한 답변 내용 저장
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"] + [("bot", now, response)]

            # 채팅 형식으로 시각화하기
            for sender, time, message in st.session_state["chat"]:
                if sender == "user":
                    st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")
                else:
                    st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:lightgray;border-radius:12px;padding:8px 12px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")

if __name__=="__main__":
    main()