# travel_planner_app.py

import streamlit as st

# ---------------------------
# 일정 생성 함수
# ---------------------------
def generate_itinerary(country, days):
    itinerary = []
    for day in range(1, days + 1):
        day_plan = {
            "day": day,
            "morning": f"{country}의 유명 관광지 방문",
            "afternoon": f"{country}의 맛집에서 점심 + 지역 산책",
            "evening": f"{country}의 야경 명소 또는 문화 공연 관람"
        }
        itinerary.append(day_plan)
    return itinerary

# ---------------------------
# Streamlit UI 구성
# ---------------------------
st.title("🌍 여행 일정 추천기")
st.write("여행하고 싶은 나라와 기간을 입력하면 자동으로 일정을 추천해드려요!")

# 사용자 입력
country = st.text_input("여행하고 싶은 나라는 어디인가요?")
days = st.number_input("며칠 동안 여행하시나요?", min_value=1, max_value=30, step=1)

# 버튼을 눌렀을 때 일정 생성
if st.button("일정 생성하기"):
    if country:
        itinerary = generate_itinerary(country, int(days))
        st.success(f"{country}로 {days}일간의 여행 일정입니다!")

        # 일정 출력
        for day_plan in itinerary:
            st.subheader(f"📅 Day {day_plan['day']}")
            st.write(f"🌅 아침: {day_plan['morning']}")
            st.write(f"🍽️ 점심: {day_plan['afternoon']}")
            st.write(f"🌙 저녁: {day_plan['evening']}")
    else:
        st.warning("여행지를 입력해주세요.")
