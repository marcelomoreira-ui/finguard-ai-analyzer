import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_report(historico_finguard: list):
    """Gera um relatório gerencial em HTML e um gráfico a partir do histórico de classificações."""
    print("\n📊 Gerando relatório gerencial...")

    if not historico_finguard:
        print("⚠️ Histórico vazio. Nenhum relatório gerado.")
        return
    
    # Criar pasta de relatório se não existir
    if not os.path.exists('./report'):
        os.makedirs('./report')
    
    # 1. Criar o DataFrame (Tabela Pandas)
    df = pd.DataFrame(historico_finguard)
    
    # 2. Exportar para CSV e JSON (Requisito 3)
    df.to_csv("./report/resultados_finguard.csv", index=False, encoding='utf-8-sig')
    df.to_json("./report/resultados_finguard.json", orient="records", force_ascii=False, indent=4)
    print("\n✅ Arquivos CSV e JSON gerados com sucesso!")

    # 3. Gerar Gráfico e Relatório HTML (Requisito 2)
    # Vamos contar quantas reclamações por categoria
    contagem_categorias = df['Categoria'].value_counts()
    
    # Criar um gráfico simples
    plt.figure(figsize=(10, 6))
    contagem_categorias.plot(kind='bar', color='skyblue')
    plt.title('Reclamações por Categoria')
    plt.ylabel('Quantidade')
    plt.tight_layout()
    plt.savefig('./report/grafico_resultados.png') # Salva o gráfico como imagem
    
    # 4. Gerar o HTML
    # O Pandas tem um método que transforma a tabela direto em HTML
    html_tabela = df.to_html(classes='table table-striped', index=False)
    
    html_final = f"""
    <html>
        <head>
            <title>Relatório FinGuard</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        </head>
        <body class="container">
            <h1 class="mt-4">Relatório Gerencial FinGuard</h1>
            <hr>
            <h3>Resumo Visual</h3>
            <img src="grafico_resultados.png" width="600">
            <h3 class="mt-4">Dados Detalhados</h3>
            {html_tabela}
        </body>
    </html>
    """
    
    with open("./report/relatorio_finguard.html", "w", encoding="utf-8") as f:
        f.write(html_final)
    print("✅ Relatório HTML com gráfico gerado!")