from sentence_transformers import SentenceTransformer
import numpy as np
import glob
import re
import json
import os

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_embeddings(texto):
    embedding_textos = model.encode(texto).tolist()
    return embedding_textos

def distancia_euclidiana(embedding_a, embedding_b) -> float:
  p1 = np.array(embedding_a)
  p2 = np.array(embedding_b)
  distancia = np.linalg.norm(p1 - p2)
  return float(distancia)


def similaridade_cosseno(vec1: np.ndarray, vec2: np.ndarray) -> float:
  norm_v1 = np.linalg.norm(vec1)
  norm_v2 = np.linalg.norm(vec2)
  if norm_v1 == 0 or norm_v2 == 0:
      return 0.0
  return float(np.dot(vec1, vec2) / (norm_v1 * norm_v2))


def distancia_cosseno(vec1: np.ndarray, vec2: np.ndarray) -> float:
  #similaridade
  cos_sim = similaridade_cosseno(vec1, vec2)
  #distancia do coseno
  cos_dist = 1.0 - cos_sim
  return float(cos_dist)

def dividir_por_linhas(texto: str):
   linhas = texto.split("\n")
   return [linha.strip() for linha in linhas if linha.strip() != ""] 

def dividir_por_paragrafo(texto: str):
    paragrafos = texto.split("\n\n")
    return [p.strip() for p in paragrafos if p.strip() != ""] 

def dividir_por_capitulo(texto: str):
    linhas = texto.split("\n")
    capitulos = []
    capitulo_atual = []

    for linha in linhas:
       if linha.startswith("#"):
          capitulos.append("\n".join(capitulo_atual).strip())

       capitulo_atual = [linha]
    else:
       capitulo_atual.append(linha)

    if capitulo_atual:
       capitulos.append("\n".join(capitulo_atual).strip())

    return [c for c in capitulos if c.strip() != ""]

def gerar_embeddings(precisao: str):
   arquivos_md = glob.glob("../aula_02/documentos_markdown/*.md")

   divisao = {
      "linha": dividir_por_linhas,
      "paragrafo": dividir_por_paragrafo,
      "capitulo": dividir_por_capitulo,
   }[precisao]

   registros = []
     
   for caminho in arquivos_md:
      with open(caminho, "r", encoding="utf-8") as f:
         texto = f.read()

      trechos = divisao(texto)  

      for trecho in trechos:
         registros.append({
            "texto": trecho,
            "origem": caminho,
            "embedding": get_embeddings(trecho),
      })
         
   os.makedirs("arquivos_json", exist_ok=True)   
   caminho_de_saida = os.path.join("arquivos_json",  f"embeddings_{precisao}.json")
   if not os.path.exists(caminho_de_saida):
    with open(caminho_de_saida, "w", encoding="utf-8") as f:
       json.dump(registros, f, ensure_ascii=False, indent=2)

       print(f"[{precisao}] {len(registros)} trechos indexados -> {caminho_de_saida}")
   else:
       print(f"O arquivo já existe e não foi sobrescrito: {caminho_de_saida}") 




def buscar_semantica(query: str, precisao:str, top_n: int = 3):
    caminho_de_entrada = os.path.join("arquivos_json", f"embeddings_{precisao}.json" )

    with open(caminho_de_entrada, "r", encoding="utf-8") as f:
       registros = json.load(f)

    embeddings_query = get_embeddings(query)

    for registro in registros:
       registro["score"] = similaridade_cosseno(embeddings_query, registro["embedding"])

    registros_ordenados = sorted(registros, key=lambda r: r["score"], reverse=True)

    print(f"\n=== Top {top_n} ({precisao}) para: '{query}' ===")
    for r in registros_ordenados[:top_n]:
        print(f"score={r['score']:.4f} | origem={r['origem']}")
        print(f"  {r['texto'][:200]}...\n")

for granularidade in ["linha", "paragrafo", "capitulo"]:
    gerar_embeddings(granularidade)

perguntas = [
        "O que é Autonomia e opacidade algorítmica?",
        "O que é o diário de bordo da IA?",
    ]

for pergunta in perguntas:
   for granularidade in ["linha", "paragrafo", "capitulo"]:
    buscar_semantica(pergunta, granularidade, top_n=3)


"""
texto_limpo = []
for caminho in arquivos_md:
    with open(caminho, "r", encoding="utf-8") as arquivo_file:
       textos = arquivo_file.read()
       textos_em_linhas = dividir_por_linhas(textos)
       texto_limpo.append(textos_em_linhas) 

print(texto_limpo[0])

def limpar_arquivos(arquivos) -> list:
    texto_limpo = []
    for caminho in arquivos:
        linhas_limpas = []
        with open(caminho, "r", encoding="utf-8") as arquivo_file:
            linhas = arquivo_file.readlines()
            for linha_limpa in linhas:
                l = re.sub(r'<!--.*?-->', '', linha_limpa)
                l = re.sub(r'^[#]+\s*', '', l)
                l = re.sub(r'^[-]{2,}\s*', '', l)
                l = l.strip()
                if l:
                   linhas_limpas.append(l)
        texto_limpo.append(linhas_limpas)
    return texto_limpo
             
      
#print(vec_md)
arquivos = limpar_arquivos(arquivos_md)
"""
            


