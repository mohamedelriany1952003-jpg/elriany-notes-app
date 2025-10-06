import streamlit as st
import pdfplumber
from fpdf import FPDF
import io

st.title("📚 تطبيق تلخيص المحاضرات - Elriany Smart Notes")

uploaded_file = st.file_uploader("📂 اختر ملف PDF للمحاضرة", type=["pdf"])

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    paragraphs = text.split("\n\n")

    st.write("✅ اختر الجمل أو الفقرات التي تريد إضافتها إلى الملخص:")
    selected = []
    for p in paragraphs:
        if st.checkbox(p.strip()[:200] + "...", key=p):
            selected.append(p.strip())

    if st.button("📄 إنشاء ملف الملخص"):
        if selected:
            pdf_buffer = io.BytesIO()
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            for item in selected:
                pdf.multi_cell(0, 10, item)
                pdf.ln()
            pdf.output(pdf_buffer)
            st.success("تم إنشاء الملخص بنجاح ✅")
            st.download_button(
                label="⬇️ تحميل الملخص",
                data=pdf_buffer.getvalue(),
                file_name="ملخص_المحاضرة.pdf",
                mime="application/pdf",
            )
        else:
            st.warning("من فضلك اختر على الأقل فقرة واحدة.")
