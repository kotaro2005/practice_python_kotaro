import streamlit as st
import ollama
import pdfplumber

st.set_page_config(page_title="TranslateGemma", page_icon="🌐", layout="wide")
st.title("🌐 TranslateGemma 翻訳ツール")

LANGUAGES = {
    "Japanese (ja)": ("Japanese", "ja"),
    "English (en)": ("English", "en"),
    "German (de)": ("German", "de"),
    "French (fr)": ("French", "fr"),
    "Chinese (zh)": ("Chinese", "zh"),
    "Korean (ko)": ("Korean", "ko"),
    "Spanish (es)": ("Spanish", "es"),
}

col1, col2 = st.columns(2)
with col1:
    source_key = st.selectbox("翻訳元", list(LANGUAGES.keys()), index=1)
with col2:
    target_key = st.selectbox("翻訳先", list(LANGUAGES.keys()), index=0)

src_name, src_code = LANGUAGES[source_key]
tgt_name, tgt_code = LANGUAGES[target_key]

CHUNK_SIZE = 1500

def translate_chunk(text_chunk):
    system_prompt = (
        f"You are a professional {src_name} ({src_code}) to {tgt_name} ({tgt_code}) translator. "
        f"Your goal is to accurately convey the meaning and nuances of the original {src_name} text "
        f"while adhering to {tgt_name} grammar, vocabulary, and cultural sensitivities. "
        f"Produce only the {tgt_name} translation, without any additional explanations or commentary."
    )
    user_prompt = (
        f"Please translate the following {src_name} text into {tgt_name}: {text_chunk}"
    )
    response = ollama.chat(
        # model="translategemma:12b",
        model="translategemma:4b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        options={"temperature": 0.1},
    )
    return response["message"]["content"]

def split_chunks(text, size=CHUNK_SIZE):
    paragraphs = text.split("\n")
    chunks, current = [], ""
    for para in paragraphs:
        if len(current) + len(para) > size and current:
            chunks.append(current.strip())
            current = para + "\n"
        else:
            current += para + "\n"
    if current.strip():
        chunks.append(current.strip())
    return chunks

tab1, tab2 = st.tabs(["📝 テキスト入力", "📄 PDFアップロード"])
text = ""

with tab1:
    text = st.text_area("翻訳したいテキストを入力", height=200,
                         placeholder="ここにテキストを貼り付けてください...")

with tab2:
    uploaded = st.file_uploader("PDFをアップロード", type="pdf")
    if uploaded:
        with pdfplumber.open(uploaded) as pdf:
            pages = pdf.pages
            total = len(pages)
            p_from = st.number_input("開始ページ", min_value=1, max_value=total, value=1)
            p_to   = st.number_input("終了ページ", min_value=1, max_value=total, value=min(5, total))
            extracted = "\n".join(
                p.extract_text() for p in pages[int(p_from)-1:int(p_to)]
                if p.extract_text()
            )
        st.text_area("抽出されたテキスト", extracted, height=200)
        text = extracted

if st.button("🔄 翻訳する", type="primary", disabled=not text):
    chunks = split_chunks(text)
    st.info(f"全{len(chunks)}チャンクに分割して翻訳します")

    results = []
    progress = st.progress(0)
    status   = st.empty()

    for i, chunk in enumerate(chunks):
        status.text(f"翻訳中... ({i+1}/{len(chunks)})")
        try:
            results.append(translate_chunk(chunk))
        except Exception as e:
            results.append(f"[エラー: {e}]")
        progress.progress((i + 1) / len(chunks))

    status.text("完了！")
    final = "\n\n".join(results)

    st.subheader("翻訳結果")
    st.write(final)
    st.download_button("📥 結果をダウンロード", data=final,
                        file_name="translation.txt", mime="text/plain")
