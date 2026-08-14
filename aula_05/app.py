import glob
from aula_04 import rodar_pipeline




if __name__ == "__main__":
    arquivos_md = glob.glob("../aula_02/documentos_markdown/*.md")
    rodar_pipeline(arquivos_md)