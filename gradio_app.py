import gradio as gr
from vectorstore import process_pdf_and_save


def handle_pdf_upload(pdf_file):
    """
    Gradio File 컴포넌트에서 넘어온 파일을 받아
    vectorstore.process_pdf_and_save 함수에 넘기고
    결과 메시지를 문자열로 반환
    """
    if pdf_file is None:
        return "먼저 pdf 파일을 업로드해주세요."

    # Gradio의 File 객체는 .name(또는 .path)에 임시 파일 경로가 들어있습니다.
    tmp_path = pdf_file.name # 또는 pdf_file.name / pdf_file.path (버전에 따라 변경)
    original_filename = pdf_file.orig_name if hasattr(pdf_file, "orig_name") else None

    result = process_pdf_and_save(tmp_path, original_filename=original_filename)

    msg = (
        f"처리 완료!\n\n"
        f"- 저장된 PDF 경로: {result['saved_pdf_path']}\n"
        f"- 생성된 텍스트 청크 개수: {result['chunk_count']} 개\n"
        f"- FAISS 인덱스 디렉토리: {result['faiss_dir']}\n"
    )
    return msg


with gr.Blocks() as demo:
    gr.Markdown("## PDF 업로드 → 청킹 → 임베딩 → FAISS 인덱스 생성")

    with gr.Row():
        pdf_input = gr.File(
            label="PDF 파일 업로드",
            file_types=[".pdf"],
        )

    output_box = gr.Textbox(
        label="처리 결과",
        lines=8,
        interactive=False,
    )

    # 파일이 업로드될 때마다 자동으로 처리
    pdf_input.change(
        fn=handle_pdf_upload,
        inputs=pdf_input,
        outputs=output_box,
    )

if __name__ == "__main__":
    # 필요하면 서버용 host/port 지정 가능
    # demo.launch(server_name="0.0.0.0", server_port=7860)
    demo.launch()