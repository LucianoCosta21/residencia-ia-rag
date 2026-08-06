from groq import Groq
from pydantic import BaseModel
from pdf_para_md import extrator_pdf
import glob
import json
import getpass
import os

extrator_pdf()

if not os.getenv("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for GROQ: ")

os.makedirs("arquivos_json", exist_ok=True)

arquivos_md = glob.glob("documentos_markdown/*.md")


client = Groq()

class ExatracaoMarkdown(BaseModel):
    titulo: str
    autores: list[str]
    ano_publicacao: str
    

if arquivos_md:
    for caminho in arquivos_md: 
         try: 
            with open(caminho, "r", encoding="utf-8") as arquivo:
                texto_extrat = arquivo.read()
                texto_inicial = texto_extrat[:1000]
                texto_final = texto_extrat[-1000:]

                conteudo = texto_inicial + texto_final

                chat_completion = client.chat.completions.create(
                    model = "openai/gpt-oss-120b",
                    max_tokens=800,  
                    temperature=0,
                    messages=[{
                        "role": "system",
                        "content":" - Extraia com precisão os seguintes campos quando presentes:* Título (title)* Autor(es) (author / authors)* Ano de publicação ou data (date / year)* Descrição ou resumo (description)- Retorne sempre os dados organizados em formato JSON limpo ou em lista estruturada, conforme solicitado pelo usuário."
                        },
                        {
                            "role": "user",
                            "content": conteudo
                        }],
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "schema_name",
                            "strict": False,
                            "schema": ExatracaoMarkdown.model_json_schema()
                        }
                        }        
                )
                result = json.loads(chat_completion.choices[0].message.content)

                nome_do_arquivo = os.path.basename(caminho).replace(".md" , ".json")

                output_file = os.path.join("arquivos_json", nome_do_arquivo)

                with open(output_file, "w", encoding="utf-8") as json_file:
                    json.dump(result, json_file, ensure_ascii=False,indent=4)

                print(f"Conversão concluída! O arquivo foi salvo como '{output_file}'.")
          
         except Exception as e: 
                print(f"Falha ao encontrar o caminho '{caminho}'! Erro: {e}")