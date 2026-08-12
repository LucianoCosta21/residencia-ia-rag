from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter, NLTKTextSplitter
from sentence_transformers import SentenceTransformer
import json
import os 
import glob
import nltk

nltk.download('punkt')
nltk.download("punkt_tab")



arquivos_md = glob.glob("../aula_02/documentos_markdown/*.md")

testes = {
    1: {"strategy": "fixed","size": 200, "overlap": 0,"type": "fixed", "separators": None},
    2: {"strategy": "fixed","size": 500, "overlap": 0,"type": "fixed", "separators": None},
    3: {"strategy": "fixed","size": 1000, "overlap": 0,"type": "fixed", "separators": None},
    4: {"strategy": "fixed","size": 2000, "overlap": 0,"type": "fixed", "separators": None},
    5: {"strategy": "fixed_with_overlap","size": 500, "overlap": 50,"type": "fixed", "separators": None},
    6: {"strategy": "fixed_with_overlap","size": 500, "overlap": 200,"type": "fixed", "separators": None},
    7: {"strategy": "paragraph","size": 500, "overlap": 200, "type": "paragraph", "separators": ["\n\n"]},
    8: {"strategy": "sentence_grouped","size": 200, "overlap": 0,"type": "sentence", "separators": None},
    9: {"strategy": "recursive_hierarchical", "size": 500, "overlap": 0,"type": "fixed", "separators": ["\n\n", "\n", ". ", " ", ""]},
    10: {"strategy": "markdown_headers","size": 200, "overlap": 0,"type": "markdown", "separators": None},
}

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_embedding(texto: str):
    return model.encode(texto).tolist()

def gerar_chunks_teste_fixo(texto: str, config: dict):
     text_splitter = RecursiveCharacterTextSplitter(
             separators=config["separators"],
             chunk_size=config["size"],
             chunk_overlap=config["overlap"],
             add_start_index=True       
     )
     documentos = text_splitter.create_documents([texto]) 
     chunks = [d.page_content for d in documentos]
     metadatas = [d.metadata for d in documentos]             
     return chunks, metadatas

def gerar_chunks_sentenca(texto: str):
    text_splitter_nltk = NLTKTextSplitter(
                 language="portuguese",
                 chunk_size=800,
                 chunk_overlap=120,
                 add_start_index=True
             )
    todas_sentencas = []
    sentencas = text_splitter_nltk.split_text(texto)
    for bloco in sentencas:
         todas_sentencas.extend(bloco.split("\n"))

    todas_sentencas = [s.strip() for s in todas_sentencas if s.strip()]


    chunks = []
    metadatas = []
    for i in range(0, len(todas_sentencas), 3):
         grupo = todas_sentencas[i:i + 3]
         chunks.append(" ".join(grupo))
         metadatas.append({"sentencas_no_chunk": len(grupo)})
    return chunks, metadatas


def gerar_chunks_markdown(texto: str): 
    headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    documentos = markdown_splitter.split_text(texto)
    chunks = [d.page_content for d in documentos]
    metadatas = [d.metadata for d in documentos] 
    return chunks, metadatas

def gerar_chunks(texto: str, config: dict):
     tipo = config["type"]

     if tipo in ("fixed", "paragraph"):
          return gerar_chunks_teste_fixo(texto, config)
     if tipo == "sentence": 
          return gerar_chunks_sentenca(texto)
     if tipo == "markdown":
          return gerar_chunks_markdown(texto)


def montar_registros(chunks, metadatas, document_id, document_name, test_id, config):
     registros = []
     for i, texto_chunk in enumerate(chunks, start=1):
          chunk_id = f"{document_id}_test{test_id}_chunk{i:03d}"
          metadata = metadatas[i - 1] if metadatas else {} 

          registros.append({
            "chunk_id": chunk_id,
            "document_id": document_id,
            "document_name": document_name,
            "test_id": test_id,
            "strategy": config["strategy"],
            "chunk_size": config["size"],
            "chunk_overlap": config["overlap"],
            "text": texto_chunk,
            "embedding": get_embedding(texto_chunk),
            "metadata": metadata,
          })  
     return registros  

def calcular_estatisticas(textos, chunk_overlap):
     tamanhos = [ len(t) for t in textos]
     num_chunks = len(textos)

     tamanho_medio =  sum(tamanhos) / num_chunks if num_chunks else 0
     tamanho_minimo =  min(tamanhos) if tamanhos else 0
     tamanho_maximo =  max(tamanhos) if tamanhos else 0
 
     chunks_sobrepostos = num_chunks - 1 if (chunk_overlap and num_chunks > 1) else 0
     percentual_overlap = round((chunk_overlap / tamanho_medio) * 100, 2) \
        if (chunk_overlap and tamanho_medio) else 0.0

     tokens_aproximados = sum(len(t.split()) for t in textos)

     return {
        "num_chunks": num_chunks,
        "tamanho_medio": round(tamanho_medio, 2),
        "tamanho_minimo": tamanho_minimo,
        "tamanho_maximo": tamanho_maximo,
        "chunks_sobrepostos": chunks_sobrepostos,
        "percentual_overlap": percentual_overlap,
        "tokens_aproximados": tokens_aproximados,
    }

def salvar_json(caminho, dados):
     os.makedirs(os.path.dirname(caminho), exist_ok=True) 
     with open(caminho, "w", encoding="utf-8") as f:
          json.dump(dados, f, ensure_ascii=False, indent=2)
           
def rodar_pipeline():
     arquivos_md = glob.glob("documentos_markdown/*.md")
     summary_por_documento = {}

     for caminho in arquivos_md:
          document_name = os.path.basename(caminho)
          document_id =  os.path.splitext(document_name)[0]
          print(document_id)
          with open(caminho, "r", encoding="utf-8") as f:
               texto = f.read()
          pasta_doc = os.path.join("results", document_id)

          pasta_md_destino = os.path.join(pasta_doc, "markdown")
          os.makedirs(pasta_md_destino, exist_ok=True)

          with open(os.path.join(pasta_md_destino, document_name), "w", encoding="utf-8") as f:
               f.write(texto)

          summary_por_documento.setdefault(document_name, [])

          for test_id, config in testes.items():
               caminho_saida = os.path.join(pasta_doc, f"test_{test_id}", "chunks_embeddings.json")

               if os.path.exists(caminho_saida):
                    print(f"[{document_id}] Teste {test_id} já existe, reaproveitando.")
                    with open(caminho_saida, "r", encoding="utf-8") as f:
                         registros = json.load(f)
               else:
                    chunks, metadatas = gerar_chunks(texto, config)
                    registros = montar_registros(chunks, metadatas, document_id, document_name, test_id, config)
                    salvar_json(caminho_saida, registros)
                    print(f"[{document_id}] Teste {test_id} ({config['strategy']}): "
                              f"{len(registros)} chunks salvos -> {caminho_saida}")


               textos = [r["text"] for r in registros]
               embedding_dimension = len(registros[0]["embedding"]) if registros else 0
               stats = calcular_estatisticas(textos, config["overlap"])     

               summary_por_documento[document_name].append({
                         "test_id": test_id,
                         "strategy": config["strategy"],
                         "chunk_size": config["size"],
                         "chunk_overlap": config["overlap"],
                         "num_chunks": stats["num_chunks"],
                         "avg_chunk_size": stats["tamanho_medio"],
                         "min_chunk_size": stats["tamanho_minimo"],
                         "max_chunk_size": stats["tamanho_maximo"],
                         "chunks_sobrepostos": stats["chunks_sobrepostos"],
                         "percentual_overlap": stats["percentual_overlap"],
                         "tokens_aproximados": stats["tokens_aproximados"],
                         "embedding_dimension": embedding_dimension,
                    })

     summary_final = [
        {"document": nome_doc, "experiments": experimentos}
        for nome_doc, experimentos in summary_por_documento.items()
    ]
     
     salvar_json(os.path.join("results", "summary.json"), summary_final)
     print(f"\nsummary.json gerado -> {os.path.join("results", 'summary.json')}")


if __name__ == "__main__":
    rodar_pipeline()



