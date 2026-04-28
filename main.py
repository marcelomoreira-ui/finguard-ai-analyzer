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
    
    while True:
        mensagem = input("\nDigite a reclamação (ou 'sair' para encerrar): ")
        
        if mensagem.lower() == 'sair':
            generate_report(historico_finguard)
            break
        
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

            # Debug: Exibe o histórico atualizado
            # for key, historico in enumerate(historico_finguard):
            #     print(f"{key}: {historico}")

# Inicialização do programa
if __name__ == "__main__":
    # main_tests()
    main_finguard()