import glob
import os
import json
import datetime
from langchain_core.documents import Document


def salvar_json(caminho, dados):
     pastas = os.path.dirname(caminho)
     if pastas:
        os.makedirs(pastas, exist_ok=True)

     with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def schema_metadata():

    arquivos_json = glob.glob(os.path.join("../aula_04/results", "*", "test_*", "chunks_embeddings.json"))
    caminhos = arquivos_json

    for caminho in caminhos:
        with open(caminho, "r" , encoding="utf-8") as f:
            registro = json.load(f)
        
        caminho_de_saida = os.path.join("documentos_json", registro[0]['document_id'], f"{registro[0]['document_id']}_teste_{registro[0]["test_id"]}.json")

        documetos_langchain = []

        for i ,item in enumerate(registro, start=1):
            documetos_langchain.append(
                Document(
                id=i,
                page_content=item["text"], 
                metadata = {
                "chunk_id": item["chunk_id"],
                "documento_id": item["document_id"],
                "fonte": item["document_name"],
                "chunk_index": int(item["chunk_id"].split("chunk")[-1]) - 1,
                "estrategia": item["strategy"],
                "chunk_size": item["chunk_size"],
                "chunk_overlap": item["chunk_overlap"],
                "n_caracteres": len(item["text"]),
                #"secao": secao,
                "modelo_embedding": "SentenceTransformer",
                "data_processamento": datetime.datetime.now().isoformat(timespec="seconds"),
                "text": item["text"],
                "embedding": item["embedding"],
                }
                )
            )
        documetos_langchain = [doc.dict() for doc in documetos_langchain ]   
        salvar_json(caminho_de_saida, documetos_langchain)   
        print(f"Salvo: {caminho_de_saida} ({len(documetos_langchain)} chunks)")

    print("Todos os documentos foram salvos!")

schema_metadata()



