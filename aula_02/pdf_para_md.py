from docling.document_converter import DocumentConverter
import os

source = ["bioetica_e_ia.pdf","escrita_academica_ia.pdf","twitter_algoritmo.pdf"]

os.makedirs("documentos_markdowm", exist_ok=True)
converter = DocumentConverter()

for doc in source:
    try:
        result = converter.convert("documentos/"+doc)
        markdown_content = result.document.export_to_markdown()
        output_file = "documentos_markdowm/"+doc.replace(".pdf", ".md")

        with open(output_file, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
        print(f"Conversão concluída! O arquivo foi salvo como '{output_file}'.")

    except Exception as e: 
        print(f"Falha ao converter '{doc}'! Erro: {e}")
