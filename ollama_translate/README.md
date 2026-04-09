# TranslateGemma ローカル翻訳環境 セットアップマニュアル

Mac mini M4（Apple Silicon）環境での構築手順です。

---

## 構成概要

```
Ollama（モデル管理・推論サーバー）
  └─ translategemma:12b（翻訳モデル 8.1GB）
       └─ Streamlit（ブラウザGUI）
            ├─ テキスト入力翻訳
            └─ PDFアップロード翻訳（ページ範囲指定）
```

---

## 1. Ollamaのインストール

```bash
brew install ollama
```

インストール確認：

```bash
ollama --version
```

---

## 2. TranslateGemmaモデルのダウンロード

### 12Bモデル（推奨・高品質）
```bash
ollama run translategemma:12b
```
- サイズ：約8.1GB
- M4 24GBメモリで快適に動作

### 4Bモデル（軽量・高速）
```bash
ollama run translategemma:4b
```
- サイズ：約3.3GB
- 速度重視の場合はこちら

ダウンロード済みモデルの確認：

```bash
ollama list
```

---

## 3. Pythonパッケージのインストール

```bash
pip install streamlit ollama pdfplumber
```

---

## 4. アプリの起動

### Ollamaサーバーを起動（別ターミナル）

```bash
ollama serve
```

### Streamlitアプリを起動

```bash
streamlit run translate_app.py
```

ブラウザが自動で開きます → `http://localhost:8501`

---

## 5. 使い方

### 翻訳元・翻訳先の選択

ドロップダウンから言語を選択します。対応言語：
- Japanese (ja)
- English (en)
- German (de)
- French (fr)
- Chinese (zh)
- Korean (ko)
- Spanish (es)

### テキスト入力翻訳

「テキスト入力」タブにテキストを貼り付けて「翻訳する」ボタンを押す。

### PDF翻訳

1. 「PDFアップロード」タブを選択
2. PDFファイルをドラッグ＆ドロップ
3. 開始・終了ページを指定（全ページ一括は時間がかかるため範囲指定推奨）
4. 「翻訳する」ボタンを押す
5. 完了後「結果をダウンロード」でtxtファイルを保存

> **目安：** 1ページあたり約30秒（12Bモデル・M4環境）

---

## 6. CLIで直接使う場合

Streamlitを使わずターミナルから直接翻訳することも可能です。

```bash
ollama run translategemma:12b
```

プロンプト形式（これをそのまま入力）：

```
You are a professional English (en) to Japanese (ja) translator.
Your goal is to accurately convey the meaning and nuances of the original English text
while adhering to Japanese grammar, vocabulary, and cultural sensitivities.
Produce only the Japanese translation, without any additional explanations or commentary.
Please translate the following English text into Japanese: [ここに翻訳したいテキスト]
```

> **重要：** プロンプトは改行せず1行で入力すること（改行すると汎用チャット応答になる場合あり）

---

## 7. モデルのアンインストール

### 個別モデルの削除

```bash
# 12Bモデルを削除
ollama rm translategemma:12b

# 4Bモデルを削除
ollama rm translategemma:4b

# 削除確認
ollama list
```

---

## 8. Ollamaのアンインストール

```bash
# Ollamaプロセスを停止
ollama stop

# アプリ本体を削除
sudo rm -rf /usr/local/bin/ollama

# モデルデータをすべて削除（~/.ollamaフォルダごと削除）
rm -rf ~/.ollama
```

容量確認してから削除したい場合：

```bash
du -sh ~/.ollama
```

---

## トラブルシューティング

### 翻訳されず説明文が返ってくる場合

→ プロンプトが正しい形式になっていない可能性があります。`translate_app.py` の system/user 分離形式を使っていることを確認してください。

### `ollama: command not found` が出る場合

```bash
brew install ollama
```

### Streamlitが起動しない場合

```bash
pip install streamlit ollama pdfplumber
streamlit run translate_app.py
```

### PDFのテキスト抽出がおかしい場合

スキャンPDF（画像PDF）は `pdfplumber` では抽出できません。テキストPDFのみ対応しています。

---

## 参考情報

| 項目 | 内容 |
|------|------|
| TranslateGemma公式 | https://blog.google/innovation-and-ai/technology/developers-tools/translategemma/ |
| Hugging Face | https://huggingface.co/google/translategemma-12b-it |
| Ollama公式 | https://ollama.com/library/translategemma |
| 技術論文 | https://arxiv.org/abs/2601.09012 |
| 対応言語数 | 55言語 |
| モデルサイズ | 4B / 12B / 27B |
