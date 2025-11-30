import streamlit as st

# 1. 한글 자음, 모음마다 획수가 몇 개인지 적어둔 '족보'입니다.
# (초성, 중성, 종성 순서대로 리스트를 만듭니다)
CHOSUNG_STROKES = [2, 4, 2, 3, 6, 5, 4, 4, 8, 2, 4, 1, 3, 6, 4, 3, 6, 2, 4] # ㄱ~ㅎ
JUNGSUNG_STROKES = [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 3, 4, 3, 4, 3, 4, 2, 3, 1, 2, 1] # ㅏ~ㅣ
JONGSUNG_STROKES = [0, 2, 4, 2, 3, 6, 5, 4, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26] # 받침 없음~ㅎ

# 2. 글자 하나를 넣으면 획수를 계산해주는 기계(함수)입니다.
def get_stroke_count(char):
    # 한글이 아니면 0점 처리 (예: 영어, 숫자 등)
    if not '가' <= char <= '힣':
        return 0
    
    # 컴퓨터가 한글을 분해하는 수학 공식 (유니코드 공식)
    char_code = ord(char) - 44032
    cho = char_code // 588
    jung = (char_code % 588) // 28
    jong = (char_code % 588) % 28
    
    # 초성 + 중성 + 종성 획수를 다 더합니다.
    stroke = CHOSUNG_STROKES[cho] + JUNGSUNG_STROKES[jung]
    
    # 받침이 있는 경우에만 종성 획수를 더합니다.
    if jong > 0:
        stroke += JONGSUNG_STROKES[jong]
    
    return stroke


def calculate_love_score(name1, name2):
    # 1. 두 이름의 글자 수 중 더 짧은 길이 구하기
    min_len = min(len(name1), len(name2))
    
    # 2. 이름 섞기 (예: 김, 이, 철, 영...)
    combined_names = []
    combined_strokes = []
    
    for i in range(min_len):
        # 내 이름 한 글자 넣고 획수 찾기
        combined_names.append(name1[i])
        combined_strokes.append(get_stroke_count(name1[i]))
        
        # 상대 이름 한 글자 넣고 획수 찾기
        combined_names.append(name2[i])
        combined_strokes.append(get_stroke_count(name2[i]))
    
    # 남은 글자가 있으면 뒤에 붙여주기 (길이가 다를 때)
    if len(name1) > min_len:
        for i in range(min_len, len(name1)):
            combined_names.append(name1[i])
            combined_strokes.append(get_stroke_count(name1[i]))
    elif len(name2) > min_len:
        for i in range(min_len, len(name2)):
            combined_names.append(name2[i])
            combined_strokes.append(get_stroke_count(name2[i]))

    # 화면에 섞인 이름 보여주기 (디버깅용)
    st.text(f"이름 배치: {' '.join(combined_names)}")
    
    # 3. 더하기 반복 (숫자가 2개 남을 때까지!)
    current_list = combined_strokes
    
    while len(current_list) > 2:
        next_list = []
        for i in range(len(current_list) - 1):
            # 앞뒤 숫자 더하기
            sum_val = current_list[i] + current_list[i+1]
            # 10이 넘으면 1의 자리만 남기기 (나머지 연산 %)
            next_list.append(sum_val % 10) 
        current_list = next_list

    # 4. 최종 점수 만들기 (앞숫자 * 10 + 뒷숫자)
    score = current_list[0] * 10 + current_list[1]
    return score

# --- 여기부터 5단계 코드 (화면 만들기) ---

# 1. 제목과 설명 적기
st.title("그 때...ㄱ...ㄴrㄴl..? 두근두근 이름 궁합 테스트 ❤")
st.write("우리 사이... 과연 몇 점일까? 획수로 알아보는 재미있는 궁합!")

# 2. 이름 입력받는 칸 만들기 (화면을 반으로 나눠서)
col1, col2 = st.columns(2) 

with col1:
    name1 = st.text_input("내 이름", placeholder="예: 김철수")

with col2:
    name2 = st.text_input("상대방 이름", placeholder="예: 이영희")

# 3. '결과 확인' 버튼 만들기
if st.button("💘 궁합 결과 보기"):
    # 이름이 둘 다 입력되었는지 확인
    if name1 and name2:
        st.divider() # 가로줄 긋기
        
        # 아까 4단계에서 만든 계산기(함수) 작동!
        final_score = calculate_love_score(name1, name2)
        
        # 결과 점수 크게 보여주기
        st.markdown(f"<h1 style='text-align: center; color: #ff4b4b;'>{final_score}%</h1>", unsafe_allow_html=True)

        st.link_button("📸 Algo 인스타 구경가기", "https://www.instagram.com/algoai.kr")
        st.write("")
        
        # 점수에 따른 멘트 보여주기
        if final_score >= 90:
            st.balloons() # 풍선 효과 팡팡!
            st.success("와우! 천생연분입니다! 결혼하세요! 💍")
            st.image("https://github.com/clap-min06/-by-Algo-/blob/main/name_test/algo_design.jpg?raw=true")
        elif final_score >= 70:
            st.info("꽤 잘 어울리는 한 쌍이네요! 🥰")
            st.image("https://github.com/clap-min06/-by-Algo-/blob/main/name_test/algo_design.jpg?raw=true")
        elif final_score >= 40:
            st.warning("노력이 조금 필요해 보입니다... 화이팅! 😂")
            st.image("https://github.com/clap-min06/-by-Algo-/blob/main/name_test/algo_design.jpg?raw=true")
        else:
            st.error("앗... 우리 그냥 좋은 친구 할까요? 😭")
            st.image("https://github.com/clap-min06/-by-Algo-/blob/main/name_test/algo_design.jpg?raw=true")
            
    else:
        # 이름을 안 썼을 때 혼내기
        st.warning("두 사람의 이름을 모두 입력해주세요!")







