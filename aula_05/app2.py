from langchain_core.documents import Document


documentos = [
    Document(
        page_content="Embeddings são representações vetoriais densas de texto.",
        metadata={
            "fonte": "arquivo_01.md",
            "pagina": 1,
            "tipo": "teoria",
            "tema": "embeddings",
            "autor": "Nome do autor",
            "temas": ["embeddings", "chunking"],
            "revisao": {"data": "2024", "status": "ok"}
        }
    ),
    Document(
        page_content="Modelos de embedding transformam palavras em listas de números.",
        metadata={
            "fonte": "arquivo_01.md",
            "pagina": 2,
            "tipo": "teoria",
            "tema": "embeddings",
            "autor": "Ana Silva",
            "temas": ["embeddings", "chunking"],
            "revisao": {"data": "2024", "status": "ok"}
        }
    ),
    Document(
        page_content="Chunking consiste em dividir textos longos em blocos menores.",
        metadata={
            "fonte": "arquivo_02.md",
            "pagina": 1,
            "tipo": "pratica",
            "tema": "chunking",
            "autor": "Bruno Costa",
            "temas": ["embeddings", "chunking"],
            "revisao": {"data": "2024", "status": "ok"}
        }
    ),
    Document(
        page_content="O tamanho do chunk afeta diretamente a recuperação no RAG.",
        metadata={
            "fonte": "arquivo_02.md",
            "pagina": 2,
            "tipo": "pratica",
            "tema": "chunking",
            "autor": "Bruno Costa",
            "temas": ["embeddings", "chunking"],
            "revisao": {"data": "2024", "status": "ok"}   
        }
    ),
    Document(
        page_content="Sistemas RAG combinam busca de documentos com geração de texto.",
        metadata={
            "fonte": "arquivo_03.md",
            "pagina": 1,
            "tipo": "arquitetura",
            "tema": "RAG",
            "autor": "Carlos Eduardo",
            "temas": ["embeddings", "chunking"],
            "revisao": {"data": "2024", "status": "ok"}
        }
    )
]

for i, doc in enumerate(documentos,  start=1):
    print(f"\n[Documentos {i}]")
    print(f"Conteúdo: {doc.page_content}")
    print(f"Metadados: {doc.metadata}")

print(f"Total de documentos na lista: {len(documentos)}")
print(documentos)
