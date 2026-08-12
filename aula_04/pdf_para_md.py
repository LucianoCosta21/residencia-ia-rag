from docling.document_converter import DocumentConverter
import glob
import os

os.makedirs("documentos_markdown", exist_ok=True)

arquivos_pdf = glob.glob("documentos/*.pdf")
#print(arquivos_pdf)

converter = DocumentConverter()

def extract_pdf():
    for doc in arquivos_pdf:
        try:
            result = converter.convert(doc)
            markdown_content = result.document.export_to_markdown()

            nome_arquivo = os.path.basename(doc)
            nome_markdown = nome_arquivo.replace(".pdf", ".md")
            output_file = os.path.join("documentos_markdown", nome_markdown)

            with open(output_file, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_content)
                print(f"Conversão concluída! O arquivo foi salvo como '{output_file}'.")

        except Exception as e: 
                    print(f"Falha ao converter '{doc}'! Erro: {e}")

extract_pdf()

