import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.title("📊 학생 성적 추이 시각화")

st.sidebar.header("데이터 업로드")
exam_files = st.sidebar.file_uploader(
    "지필고사 및 모의고사 파일 업로드 (여러 파일 가능)", 
    accept_multiple_files=True, 
    type=["xlsx", "csv"]
)

st.sidebar.header("학생 정보 입력")
name = st.sidebar.text_input("학생 이름")
grade = st.sidebar.number_input("조회할 마지막 학년 (1~3)", 1, 3, 1)

def extract_grade_from_filename(filename):
    """파일명에서 '1학년', '2학년' 등을 찾아 숫자로 반환"""
    match = re.search(r"(\d)학년", filename)
    return int(match.group(1)) if match else None

def clean_mock_exam(df):
    """모의고사 엑셀 정리: 병합 셀, 불필요한 행 제거"""
    # 학교명(관악고등학교) 등 있는 행 제거
    df = df.dropna(how="all", axis=1)  # 완전 빈 열 제거
    df = df.dropna(how="all", axis=0)  # 완전 빈 행 제거

    # '관악고등학교' 같은 행 제거
    df = df[~df.astype(str).apply(lambda x: x.str.contains("관악고등학교", na=False)).any(axis=1)]

    # 이름 열 자동 탐색 (병합된 경우 대비)
    df.columns = [str(c) for c in df.columns]
    df = df.reset_index(drop=True)

    # 첫 번째 행에 과목명이 있을 수 있으니 확인
    if df.iloc[0].isnull().sum() < len(df.columns) / 2:
        df.columns = df.iloc[0]
        df = df[1:]

    # 번호 + 이름 열 추출 시도
    possible_name_cols = [col for col in df.columns if "이름" in str(col)]
    if not possible_name_cols:
        # 이름이 직접 컬럼명에 없을 경우 첫 3열 내에서 찾기
        df.columns = [str(c) for c in df.columns]
        df.rename(columns={df.columns[1]: "번호", df.columns[2]: "이름"}, inplace=True)
    else:
        df.rename(columns={possible_name_cols[0]: "이름"}, inplace=True)
    
    return df

def clean_exam(df):
    """지필고사 엑셀 정리"""
    df = df.dropna(subset=["이름"])
    # 총점, 평균 제외
    if "총점" in df.columns:
        df = df.drop(columns=["총점"])
    if "평균" in df.columns:
        df = df.drop(columns=["평균"])
    return df

if exam_files and name:
    all_data = []

    for file in exam_files:
        filename = file.name
        grade_in_file = extract_grade_from_filename(filename)

        # 파일 읽기
        try:
            if filename.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file, header=None)
        except Exception as e:
            st.error(f"❌ {filename} 불러오기 실패: {e}")
            continue

        # 모의고사/지필고사 자동 판별
        if "모의" in filename:
            df = clean_mock_exam(df)
        else:
            # 지필고사: 첫 행이 헤더일 수 있음
            try:
                df = pd.read_excel(file)
            except:
                pass
            df = clean_exam(df)

        df["학년"] = grade_in_file
        all_data.append(df)

    if not all_data:
        st.error("파일을 불러올 수 없습니다. 형식을 확인하세요.")
        st.stop()

    data = pd.concat(all_data, ignore_index=True)

    # 이름 기준 필터링
    student_data = data[data["이름"].astype(str).str.strip() == name.strip()]

    if student_data.empty:
        st.warning(f"'{name}' 학생 데이터를 찾을 수 없습니다.")
        st.stop()

    # 과목 컬럼 찾기
    exclude_cols = ["반", "번호", "이름", "학년"]
    subjects = [c for c in student_data.columns if c not in exclude_cols]

    # 학년별 평균 점수 계산
    grade_means = (
        student_data.groupby("학년")[subjects].mean().reset_index()
    )

    overall_means = (
        data.groupby("학년")[subjects].mean().mean(axis=1)
    )

    st.subheader(f"📈 {name} 학생의 성적 추이 (1학년~{grade}학년)")

    fig, ax = plt.subplots(figsize=(10, 6))

    for subj in subjects:
        ax.bar(grade_means["학년"], grade_means[subj], alpha=0.6, label=f"{subj} 점수")

    ax.plot(overall_means.index, overall_means.values, color="red", marker="o", linewidth=2, label="전체 평균")

    ax.set_xlabel("학년")
    ax.set_ylabel("점수")
    ax.set_title(f"{name} 학생 학년별 성적 추이")
    ax.legend()
    st.pyplot(fig)
