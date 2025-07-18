import os
import json
import openai

# Configure sua chave da OpenAI
# Caminho para a pasta com os arquivos JSON
PASTA_JSON = "/Users/rodrigocarvalho1/Desktop/C/Estudos/clientes_json"
client = openai.OpenAI(api_key="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")

def carregar_cliente(id_cliente):
    """Carrega o JSON de um cliente pelo ID"""
    filename = os.path.join(PASTA_JSON, f"{id_cliente}.json")
    if not os.path.isfile(filename):
        print(f"Cliente {id_cliente} não encontrado.")
        return None
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def query_llm(json_cliente, pergunta):
    """Envia o JSON e a pergunta para o modelo da OpenAI"""
    prompt = f"""
Você está analisando os dados JSON de um cliente:

{json.dumps(json_cliente, indent=2, ensure_ascii=False)}

Agora responda à seguinte pergunta com base nesses dados:
"{pergunta}"
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente que responde consultas sobre dados JSON de clientes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content

def main():
    print("=== Consulta de Clientes ===")
    id_cliente = input("Digite o ID do cliente (ex: 00001): ").strip()
    cliente = carregar_cliente(id_cliente)
    if not cliente:
        return
    
    while True:
        pergunta = input("\nDigite sua pergunta sobre o cliente (ou 'sair' para encerrar): ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            break
        resposta = query_llm(cliente, pergunta)
        print("\n📌 Resposta do modelo:")
        print(resposta)

if __name__ == "__main__":
    main()
