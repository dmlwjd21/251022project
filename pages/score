import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("학생 성적 추이 시각화")

# 파일 업로드
st.sidebar.header("데이터 업로드")
exam_files = st.sidebar.file_uploader(
    "지필고사 및 모의고사 파일 업로드 (여러 파일 가능)", 
    accept_multiple_files=True, 
    type=["csv", "xlsx"]
)

# 학생 정보 입력
st.sidebar.header("학생 정보 입력")
entry_year = st.sidebar.number_input("입학년도", min_value=2000, max_value=2100, value=2023)
grade = st.sidebar.number_input("학년", min_value=1, max_value=3, value=1)
class_num = st.sidebar.number_input("반", min_value=1, max_value=10, value=1)
name = st.sidebar.text_input("학생 이름")

if exam_files and name:
    all_data = []
    
    for file in exam_files:
        # 학년 정보를 파일 이름에서 추출 (예: 2023_1학년_지필.csv)
        filename = file.name
        try:
            file_grade = int(filename.split("_")[1][0])  # '1학년' -> 1
        except:
            st.warning(f"파일 이름에서 학년을 추출할 수 없습니다: {filename}")
            continue
        
        # 파일 읽기
        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        df["학년"] = file_grade
        all_data.append(df)
    
    if not all_data:
        st.error("올바른 파일이 없습니다.")
        st.stop()
    
    data = pd.concat(all_data, ignore_index=True)
    
    # 입력 학생 데이터만 필터링
    student_data = data[
        (data["입학년도"] == entry_year) &
        (data["학년"] == grade) &
        (data["반"] == class_num) &
        (data["이름"] == name)
    ]
    
    if student_data.empty:
        st.warning("해당 학생 데이터가 없습니다.")
        st.stop()
    
    # 성적 추이 시각화
    subjects = [col for col in student_data.columns if col not in ["입학년도", "학년", "반", "이름"]]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 학생 성적 막대그래프
    student_means = student_data[subjects].mean()
    student_means.plot(kind="bar", color="skyblue", ax=ax, label=f"{name} 성적")
    
    # 전체 평균 꺾은선 그래프
    overall_means = data.groupby("학년")[subjects].mean().mean(axis=1)
    overall_means.plot(kind="line", marker="o", color="red", linewidth=2, ax=ax, label="전체 평균")
    
    ax.set_title(f"{name} 학생 성적 추이")
    ax.set_xlabel("과목")
    ax.set_ylabel("점수")
    ax.legend()
    plt.xticks(rotation=45)
    
    st.pyplot(fig)
