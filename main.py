from scripts.rag_local_test import rag_local_test
from scripts.nova_lite_test import nova_lite_test
from scripts.finguard_motor import *
from scripts.report_generator import generate_report
import pandas as pd

# Função principal para rodar os testes ou o FinGuard
def main_tests():
    print("Running RAG local test...")
    rag_local_test()

    print("\nRunning Nova Lite test...")
    nova_lite_test()

# Função principal para rodar o FinGuard
def main_finguard():

    mostrar_apresentacao()

    historico_finguard: list = []  # Simulação de um dataset em memória

    path_csv = "./dataset/dataset_finguard_desafio_3.csv"
    try:
        df = pd.read_csv(path_csv, encoding='utf-8-sig')
       
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return
    
 # Iterar sobre cada linha do DataFrame
    for index, row in df.iterrows():
        mensagem = row.get('texto_reclamacao', None)
        if not mensagem or pd.isna(mensagem):
            print(f"\nLinha {index}: texto_reclamacao vazio ou inválido, pulando...")
            continue

        print(f"\nProcessando reclamação {index + 1}:")
        print(f"Texto: {mensagem}")

        print("\n🔍 Analisando com AWS Nova Lite...")
        resultado = analisar_com_nova(mensagem)

        if resultado is None:
            print("❌ Erro: Não foi possível processar a resposta do modelo.")
        elif isinstance(resultado, str) and "Erro" in resultado:
            print(f"❌ Erro na comunicação: {resultado}")
        else:
            # Exibe o resultado formatado
            print("\n--- Resultado da Classificação ---")
            print(json.dumps(resultado, indent=4, ensure_ascii=False))

            # Orquestração (Nível 2)
            orquestrador_finguard(resultado)

            historico_finguard.append(resultado)

    # Após processar todas as reclamações, gera o relatório
    generate_report(historico_finguard)

# Inicialização do programa
if __name__ == "__main__":
    # main_tests()
    main_finguard()