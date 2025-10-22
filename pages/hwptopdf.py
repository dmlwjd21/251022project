import streamlit as st
import pdfkit
from PyPDF2 import PdfMerger
import tempfile
import os
os.system("apt-get update -y && apt-get install -y hwp5 wkhtmltopdf")
import subprocess

st.set_page_config(page_title="HWP to PDF 병합기", layout="wide")

st.title("📄 여러 한글파일(HWP)을 하나의 PDF로 병합하기")
st.write("여러 개의 HWP 파일을 업로드하면 자동으로 PDF로 변환 후 하나로 합쳐드립니다.")

uploaded_files = st.file_uploader("HWP 파일 업로드", type=["hwp"], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("변환 중입니다..."):
        temp_dir = tempfile.mkdtemp()
        pdf_paths = []

        for file in uploaded_files:
            input_path = os.path.join(temp_dir, file.name)
            with open(input_path, "wb") as f:
                f.write(file.read())

            # hwp → html 변환
            html_path = os.path.splitext(input_path)[0] + ".html"
            try:
                subprocess.run(["hwp5html", input_path, "-o", html_path], check=True)
            except Exception as e:
                st.error(f"{file.name} 변환 중 오류 발생: {e}")
                continue

            # html → pdf 변환
            pdf_path = os.path.splitext(input_path)[0] + ".pdf"
            pdfkit.from_file(html_path, pdf_path)
            pdf_paths.append(pdf_path)

        if pdf_paths:
            # PDF 병합
            merger = PdfMerger()
            for pdf in pdf_paths:
                merger.append(pdf)
            merged_path = os.path.join(temp_dir, "merged.pdf")
            merger.write(merged_path)
            merger.close()

            with open(merged_path, "rb") as f:
                st.download_button(
                    label="📥 병합된 PDF 다운로드",
                    data=f,
                    file_name="merged.pdf",
                    mime="application/pdf",
                )
            st.success("모든 파일이 성공적으로 병합되었습니다!")
        else:
            st.warning("변환된 PDF가 없습니다. HWP 파일이 손상되었을 수 있습니다.")
