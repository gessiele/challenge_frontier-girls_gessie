from foundry.functions import function, String
# Importe o tipo específico para arquivos
from foundry.functions.types import MediaReference 
import pypdf
import io

@function
def extrair_texto_pdf(arquivo_pdf: MediaReference) -> String:
    """
    Lê o conteúdo de texto de um arquivo PDF fornecido via MediaReference.
    """
    try:
        # 1. Abrir o stream do arquivo (o Foundry baixa os dados aqui)
        with arquivo_pdf.open() as f:
            # O 'f' é um stream, precisamos ler os bytes para o pypdf
            pdf_bytes = io.BytesIO(f.read())
            
            # 2. Ler o PDF com pypdf
            reader = pypdf.PdfReader(pdf_bytes)
            texto_completo = []
            
            for page in reader.pages:
                texto_extraido = page.extract_text()
                if texto_extraido:
                    texto_completo.append(texto_extraido)
            
            return "\n".join(texto_completo)

    except Exception as e:
        return f"Erro ao processar o arquivo: {str(e)}"
