from scripts.rag_local_test import rag_local_test
from scripts.nova_lite_test import nova_lite_test
from scripts.finguard_motor import *
import pandas as pd


def main_tests():
    print("Running RAG local test...")
    rag_local_test()

    print("\nRunning Nova Lite test...")
    nova_lite_test()

def main_finguard():

    mostrar_apresentacao()
    
    while True:
        mensagem = input("\nDigite a reclamação (ou 'sair' para encerrar): ")
        
        if mensagem.lower() == 'sair':
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
            
            # Simulação de salvamento no Dataset com Pandas
            df = pd.DataFrame([resultado])
            # Aqui você poderia salvar em um CSV: df.to_csv('registros.csv', mode='a', index=False)

if __name__ == "__main__":
    # main_tests()
    main_finguard()

