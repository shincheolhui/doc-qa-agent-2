# 📘 README.md — doc-qa-agent-2

## 📖 프로젝트 개요

**doc-qa-agent-2**는 LangChain과 Gradio를 이용해
PDF 문서를 업로드하면 자동으로 다음 단계를 수행하는 AI 문서처리 에이전트입니다:

1. PDF 로딩 → 텍스트 청킹
2. OpenAI 임베딩 생성
3. FAISS 벡터 인덱스 저장

이후 이 인덱스를 이용해 **문서 기반 질의응답(RAG)** 기능으로 확장할 수 있습니다.

---

## 🧩 주요 기능

| 기능           | 설명                                              |
| ------------ | ----------------------------------------------- |
| PDF 업로드      | Gradio UI에서 PDF 파일 업로드                          |
| 텍스트 청킹       | LangChain TextSplitter로 자동 분할                   |
| 임베딩 생성       | OpenAI Embedding API (`text-embedding-3-small`) |
| FAISS 저장     | 문서 벡터 인덱스를 로컬에 저장 및 갱신                          |
| .env 관리      | API Key를 환경 변수로 분리                              |
| SSH over 443 | 회사망(포트 22 차단)에서도 GitHub에 안전하게 연결 가능             |

---

## 🏗️ 프로젝트 구조

```
doc-qa-agent-2/
│
├─ gradio_app.py              # Gradio UI (PDF 업로드 → FAISS 저장)
├─ vectorstore.py             # 청킹, 임베딩, FAISS 저장 로직
├─ .env                       # OpenAI API 키
├─ .gitignore                 # 업로드/인덱스/환경파일 제외
├─ requirements.txt           # 패키지 목록
└─ data/
    ├─ uploads/               # 업로드된 PDF (Git에 미포함)
    │   └─ .gitkeep
    └─ faiss_index/           # FAISS 인덱스 (Git에 미포함)
        └─ .gitkeep
```

---

## 🧰 1. 환경 설정

### ✅ 가상환경 생성

**Windows PowerShell**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### ✅ 패키지 설치

```bash
pip install -r requirements.txt
```

`requirements.txt`가 없다면 수동으로 설치:

```bash
pip install gradio langchain langchain-core langchain-community langchain-openai langchain-text-splitters faiss-cpu python-dotenv pypdf
```

---

## 🔑 2. 환경 변수 설정 (.env)

루트 폴더(`doc-qa-agent-2/.env`)에 아래 내용 추가:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🧠 3. 실행

```bash
python gradio_app.py
```

터미널에 아래 메시지가 나오면 정상입니다 👇

```
Running on local URL:  http://127.0.0.1:7860
```

→ 브라우저에서 링크를 열면 PDF 업로드 인터페이스가 표시됩니다.
업로드 시 자동으로
✅ 텍스트 청킹 → ✅ 임베딩 생성 → ✅ FAISS 저장
이 수행됩니다.

---

## 🗂️ 4. 데이터 저장 경로

| 폴더                  | 설명                       |
| ------------------- | ------------------------ |
| `data/uploads/`     | 업로드된 PDF 원본 (Git에 미포함)   |
| `data/faiss_index/` | FAISS 인덱스 저장소 (Git에 미포함) |

---

## 🧱 5. Git 설정 및 업로드 (SSH over 443)

회사망에서 **SSH 포트 22이 차단된 경우**,
GitHub는 **443 포트 기반 SSH 연결**을 지원합니다.
아래 단계대로 설정하면 보안망에서도 안전하게 push/pull이 가능합니다.

---

### 🧩 (1) SSH over 443 설정

1. SSH 설정 파일 열기

   ```bash
   notepad ~/.ssh/config
   ```
2. 아래 내용 추가

   ```bash
   Host github.com
     Hostname ssh.github.com
     Port 443
     User git
     IdentityFile ~/.ssh/id_ed25519
     TCPKeepAlive yes
     IdentitiesOnly yes
   ```

---

### 🔐 (2) SSH 키 생성 및 등록

#### SSH 키 생성

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

> 기본 경로: `C:\Users\<사용자명>\.ssh\id_ed25519`
> (비밀번호는 Enter로 생략 가능)

#### SSH 에이전트 시작 및 키 등록

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

#### 🔎 공개키 확인

```bash
cat ~/.ssh/id_ed25519.pub
```

#### GitHub에 등록

1. GitHub → **Settings → SSH and GPG keys → New SSH key**
2. 제목 예: `office-laptop`
3. 위 명령에서 복사한 공개키를 붙여넣기

---

### 🔗 (3) SSH 연결 테스트

```bash
ssh -T git@github.com
```

성공 시 출력:

```
Hi your-username! You've successfully authenticated, but GitHub does not provide shell access.
```

---

### 👤 (4) Git 사용자 정보 설정

Git 커밋에는 작성자의 이름과 이메일이 필요합니다:

```bash
git config --global user.name "your_name"
git config --global user.email "your_email@example.com"
```

설정 확인:

```bash
git config --list
```

> ※ 회사 계정 환경에서는 사내 이메일 주소 사용을 권장합니다.

---

### 🚀 (5) Git 초기화 및 업로드

#### 기존 Git 제거 (복제된 프로젝트일 경우)

```bash
rm -rf .git
```

#### 새 Git 초기화

```bash
git init
git add .
git commit -m "Initial commit: PDF → FAISS Gradio pipeline"
```

#### 원격 저장소 연결 (SSH over 443)

```bash
git remote add origin git@github.com:<your-username>/doc-qa-agent-2.git
git branch -M master
git push -u origin master
```

> ⚙️ SSH 설정이 올바르면 `ssh.github.com:443` 포트로 자동 연결됩니다.

---

## 🧾 6. .gitignore 설정 (보안 데이터 제외)

민감한 데이터(`uploads/`, `faiss_index/`, `.env`)는 **절대 커밋하지 않습니다.**

### `.gitignore` 예시

```gitignore
# === Python 기본 무시 목록 ===
__pycache__/
*.pyc
*.pyo
*.pyd
*.log
*.sqlite3
.env

# === 가상환경 ===
.venv/
venv/
env/

# === IDE / OS 파일 ===
.idea/
.vscode/
.DS_Store
Thumbs.db

# === 데이터 디렉토리 ===
data/uploads/*
!data/uploads/.gitkeep   # uploads 폴더는 유지하고 내부 파일만 제외
data/faiss_index/*
!data/faiss_index/.gitkeep

# === 기타 ===
*.pdf
```

### `.gitkeep` 파일 생성

```bash
echo "" > data/uploads/.gitkeep
echo "" > data/faiss_index/.gitkeep
```

### 커밋

```bash
git add .gitignore data/uploads/.gitkeep data/faiss_index/.gitkeep
git commit -m "Add .gitignore and .gitkeep for data folders"
```

---

## ⚙️ 7. requirements.txt 예시

```txt
# === Core OpenAI & LangChain Stack ===
openai==2.7.1
langchain==1.0.4
langgraph==1.0.2
langchain-openai==1.0.2
langchain-community==0.4.1
langchain-text-splitters==1.0.0

# === Vector Store (FAISS) ===
faiss-cpu==1.12.0

# === Web Framework & Server ===
fastapi==0.121.0
uvicorn[standard]==0.38.0

# === UI (Gradio) ===
gradio==5.49.1

# === PDF & 문서 처리 ===
pypdf==6.1.3

# === Tokenization ===
tiktoken==0.12.0

# === 기타 유틸 ===
python-dotenv==1.0.1
```

---

## 💡 8. 확장 아이디어

| 확장 기능            | 설명                 |
| ---------------- | ------------------ |
| Q&A 챗봇 탭 추가      | 업로드된 문서 기반 질의응답    |
| 여러 PDF 관리        | 문서별 인덱스 분리         |
| RAG 파이프라인 완성     | LLM + Retriever 연결 |
| Slack / Teams 연동 | 사내 문서검색 챗봇 구현      |

---

## 🧾 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.
자유롭게 수정 및 재배포 가능합니다.

---

## ✨ Author

**신철희**

---
