import boto3
import json
import pandas as pd

def analisar_com_nova(texto_usuario: str) -> dict:
    """Envia o texto para o modelo Nova Lite na AWS Bedrock."""

    # --- CONFIGURAÇÃO AWS ---
    # Substitua pela sua região se for diferente
    bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

    # Este é o "Prompt" que ensina o modelo a se comportar
    prompt_sistema = """
    Você é o motor de classificação do FinGuard. 
    Analise a reclamação do cliente e retorne APENAS um JSON no formato, sem blocos de código markdown, 
    sem aspas triplas e sem explicações. Comece a resposta diretamente com '{'":
    {
      "Categoria": "string",
      "Produto": "string",
      "Sentimento": "Positivo/Negativo/Neutro",
      "Urgencia": "Baixa/Media/Alta/Critica",
      "Resumo": "resumo de 2-3 linhas"
    }
    Se houver palavrões, substitua-os por **** no campo Resumo.
    """

    print("\n🔍 Enviando para AWS Nova Lite...")#Debug

    corpo_requisicao = json.dumps(
        {
            "inferenceConfig": {"max_new_tokens": 1000, "temperature": 0},
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": f"{prompt_sistema}\n\nTexto do cliente: {texto_usuario}"
                        }
                    ],
                }
            ],
        }
    )
    # print(f"Corpo da Requisição: {corpo_requisicao}")#Debug

    try:
        # Chamada ao modelo Nova Lite (Verifique o ID exato do modelo no console AWS)
        response = bedrock_runtime.invoke_model(
            modelId="us.amazon.nova-lite-v1:0", 
            body=corpo_requisicao ,
            contentType="application/json",
            accept="application/json"
        )

        # print(f"Resposta do Modelo: {response}")#Debug

        # 1. Leia o StreamingBody e decodifique para string
        response_body = response['body'].read().decode('utf-8')

        # 2. Agora sim, transforme em um dicionário Python
        response_json = json.loads(response_body)

        # 3. Acesse o conteúdo (o formato da resposta do Nova Lite)
        texto_gerado = response_json['output']['message']['content'][0]['text']

        # print(f"Texto Gerado: {texto_gerado}")#Debug

        return json.loads(texto_gerado)

    except Exception as e:
        return {"Erro": str(e)}


def orquestrador_finguard(dados_classificados: dict):
    """Aplica as regras de negócio baseadas na classificação."""

    print("\n--- Processando Regras de Orquestração ---")

    # Regra: Urgência Crítica (Salto de etapas)
    if dados_classificados.get("Urgencia") == "Critica":
        print("🚨 ALERTA: Urgência CRÍTICA detectada!")
        print(
            "⏭️  Ação: Saltando etapas burocráticas. Enviando direto para Análise de Risco."
        )
    else:
        print("✅ Fluxo padrão: Seguindo para análise de conformidade.")


def mostrar_apresentacao() -> None:
    print("=" * 40)
    print("      FINGUARD - PROVA DE CONCEITO")
    print("   Proteção e Análise Financeira Inteligente")
    print("=" * 40)
