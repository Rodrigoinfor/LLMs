import os
import json
import openai

# Configure sua chave da OpenAI
client = openai.OpenAI(api_key="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")
# Caminho para a pasta com os arquivos JSON
PASTA_JSON = "/Users/rodrigocarvalho1/Desktop/C/Estudos/clientes_json"

def carregar_todos_clientes():
    """Carrega todos os arquivos JSON de clientes"""
    clientes = []
    for filename in os.listdir(PASTA_JSON):
        if filename.endswith(".json"):
            filepath = os.path.join(PASTA_JSON, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                cliente = json.load(f)
                clientes.append(cliente)
    print(f"✅ {len(clientes)} clientes carregados.")
    return clientes

def query_llm(clientes, pergunta):
    """Envia os JSONs e a pergunta para o modelo da OpenAI"""
    prompt = f"""
Você está analisando os dados JSON de vários clientes:

{json.dumps(clientes, indent=2, ensure_ascii=False)}

Agora responda à seguinte pergunta com base nesses dados:
"{pergunta}"
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente que responde consultas sobre dados JSON de vários clientes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content

def main():
    print("=== Consulta sobre Clientes ===")
    clientes = carregar_todos_clientes()
    
    while True:
        pergunta = input("\nDigite sua pergunta (ou 'sair' para encerrar): ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("👋 Encerrando...")
            break
        resposta = query_llm(clientes, pergunta)
        print("\n📌 Resposta do modelo:")
        print(resposta)

if __name__ == "__main__":
    main()