import os
from typing import List

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
# from langchain.schema import Document
from langchain_core.documents import Document

# .env 파일 로드
load_dotenv()

# 디렉터리 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
FAISS_DIR = os.path.join(DATA_DIR, "faiss_index")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FAISS_DIR, exist_ok=True)


def load_and_split_pdf(pdf_path: str) -> List[Document]:
    """
    PDF 파일 경로를 받아서
    - 문서를 로딩하고
    - 텍스트를 청크 단위로 나눈 뒤
    - langchain Document 리스트로 반환
    """
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # 청킹 전략: 1000자 단위, 200자 겹침
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    split_docs = splitter.split_documents(docs)
    return split_docs


def get_embeddings():
    """
    OpenAI 임베딩 인스턴스 생성
    (원하면 model 이름만 바꾸면 됨)
    """
    return OpenAIEmbeddings(
        model="text-embedding-3-small", # 비용 저렴 & 성능 무난
    )


def save_or_updates_faiss(docs: List[Document]) -> int:
    """
    Document 리스트를 받아서
    - 기존 FAISS 인덱스가 있으면 불러와서 add_documents
    - 없으면 새로 from_documents 생성
    - 최종적으로 FAISS_DIR에 저장
    반환값: 추가/저장된 청크 개수
    """
    embeddings = get_embeddings()

    # 기존 인덱스가 있는지 확인
    index_files_exist = any(
        name.endswith(".faiss") or name.endswith(".pkl")
        for name in os.listdir(FAISS_DIR)
    )

    if index_files_exist:
        # 기존 인덱스 로드
        vectorstore = FAISS.load_local(
            FAISS_DIR,
            embeddings,
            allow_dangerous_deserialization=True,
        )
        vectorstore.add_documents(docs)
    else:
        # 새로운 인덱스 생성
        vectorstore = FAISS.from_documents(docs, embeddings)

    # 로컬에 저장
    vectorstore.save_local(FAISS_DIR)
    return len(docs)

    
def process_pdf_and_save(pdf_tmp_path: str, original_filename: str | None = None) -> dict:
    """
    Gradio에서 전달받은 PDF 임시경로를 받아서
    - uploads 폴더에 복사(백업용, 선택)
    - load_and_split_pdf로 청킹
    - save_or_update_faiss로 FAISS 저장/갱신
    - 처리 결과 정보를 dict로 반환
    """
    # 업로드 파일을 저장(선택 사항이지만, 나중에 다시 쓸 수 있어 편함)
    if original_filename:
        save_name = original_filename
    else:
        save_name = os.path.basename(pdf_tmp_path)

    saved_pdf_path = os.path.join(UPLOAD_DIR, save_name)

    # 단순 파일 복사
    if pdf_tmp_path != saved_pdf_path:
        with open(pdf_tmp_path, "rb") as src, open(saved_pdf_path, "wb") as dst:
            dst.write(src.read())

    # PDF -> 문서 -> 청킹
    split_docs = load_and_split_pdf(saved_pdf_path)

    # FAISS 저장/갱신
    chunk_count = save_or_updates_faiss(split_docs)

    return {
        "saved_pdf_path": saved_pdf_path,
        "chunk_count": chunk_count,
        "faiss_dir": FAISS_DIR,
    }