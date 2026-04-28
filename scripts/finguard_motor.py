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
        Você é o Motor de Inteligência do FinGuard, especializado na POLÍTICA INTERNA DE ATENDIMENTO AO CLIENTE (POL-SAC-001).
        Sua tarefa é analisar reclamações e extrair dados estruturados cumprindo rigorosamente as diretrizes de segurança e classificação.

        ### DIRETRIZES DE CLASSIFICAÇÃO (POL-SAC-001) ###
        - CRÍTICA: Menção a Banco Central, Procon, Justiça, Advogado, Fraude ou Vulnerabilidade Financeira/Emocional.
        - ALTA: Valores MAIOR QUE R$ 500, ameaça de órgãos reguladores ou múltiplas tentativas sem solução.
        - MÉDIA: Impacto financeiro moderado ou falhas de atendimento recorrentes.
        - BAIXA: Dúvidas operacionais ou insatisfações leves sem impacto financeiro.

        ### PROTOCOLO DE ANÁLISE DE VALORES FINANCEIROS ###
        - Identifique explicitamente o valor monetário na reclamação.
        - Se o valor for < 500,00: NUNCA classifique como ALTA apenas pelo valor. Use MÉDIA ou BAIXA.
        - Se o valor for >= 500,00: Classifique como ALTA.
        - EXCEÇÃO: Se houver menção a Banco Central/Justiça, a urgência sobe para CRÍTICA independentemente do valor.

        ### EXEMPLO DE PENSAMENTO ###
        Texto: "Cobrei 60 reais indevidos." -> Valor: 60 -> 60 é menor que 500 -> Urgência: MÉDIA.
        Texto: "Cobrei 600 reais indevidos." -> Valor: 600 -> 600 é maior que 500 -> Urgência: ALTA.

        ### REGRAS DE OURO DE SEGURANÇA E PRIVACIDADE ###
        1. DADOS SENSÍVEIS: É terminantemente PROIBIDO incluir Nome Próprio, CPFs, números de conta, números de cartão, endereços ou telefones no campo "Resumo". Substitua obrigatoriamente por [DADOS OMITIDOS].
        2. LINGUAGEM IMPRÓPRIA: Se detectar palavrões ou ofensas, substitua cada palavra por ****.
        3. FORMATO DE SAÍDA: Retorne APENAS o JSON. Não inclua markdown (como ```json), não inclua explicações e não inclua aspas triplas. Inicie com { e termine com }.

        ### ESTRUTURA DO JSON ESPERADO ###
        {
        "Categoria": "classificação em uma das categorias: Cobrança Indevida, Atendimento, Fraude/Segurança, Produto/Serviço, Cancelamento, Segurança da Informação e Outros",
        "Produto": "Cartão de Crédito / Conta Corrente / Empréstimo / Investimentos / Seguros / Outros",
        "Sentimento": "Positivo / Negativo / Neutro",
        "Urgencia": "Baixa / Media / Alta / Critica",
        "Resumo": "Resumo de 2-3 linhas focado no problema, aplicando OMITIDOS e ofuscação",
        "Acao_Imediata": "Qual a ação imediata definida na política POL-SAC-001 para esta urgência?"
        }

        ### EXEMPLO DE AÇÃO IMEDIATA (Contexto) ###
        - Se Urgência Alta: "Contato em 4h e notificar coordenador."
        - Se Urgência Crítica: "Contato imediato (2h), escalar para Gerente e Compliance."

        Analise o texto abaixo e gere o JSON:
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
