import json
import os

def carregar_dados():
    """Carrega os dados de funcionários e vagas a partir dos arquivos JSON."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    caminho_funcionarios = os.path.join(base_dir, 'data', 'funcionarios.json')
    caminho_vagas = os.path.join(base_dir, 'data', 'vagas.json')

    try:
        with open(caminho_funcionarios, 'r', encoding='utf-8') as f:
            funcionarios = json.load(f)
        with open(caminho_vagas, 'r', encoding='utf-8') as f:
            vagas = json.load(f)
        return funcionarios, vagas
    except FileNotFoundError:
        return None, None

def recomendar_vagas(id_funcionario):
    """
    Gera recomendações de vagas para um funcionário específico com base em suas habilidades.
    """
    funcionarios, vagas = carregar_dados()
    if funcionarios is None or vagas is None:
        return {"erro": "Arquivos de dados não encontrados."}

    funcionario_alvo = None
    for f in funcionarios:
        if f['id'] == id_funcionario:
            funcionario_alvo = f
            break

    if not funcionario_alvo:
        return {"erro": f"Funcionário com ID {id_funcionario} não encontrado."}

    # Combina habilidades declaradas e descobertas (e converte para minúsculas para comparação)
    habilidades_do_funcionario = set(
        [h.lower() for h in funcionario_alvo.get("habilidades_declaradas", [])] + 
        [h.lower() for h in funcionario_alvo.get("habilidades_descobertas", [])]
    )

    recomendacoes = []
    for vaga in vagas:
        habilidades_requeridas = set([h.lower() for h in vaga.get("habilidades_requeridas", [])])

        habilidades_compativeis = habilidades_do_funcionario.intersection(habilidades_requeridas)
        habilidades_faltantes = habilidades_requeridas.difference(habilidades_do_funcionario)

        if not habilidades_requeridas:  # Evita divisão por zero
            percentual_compatibilidade = 0
        else:
            percentual_compatibilidade = (len(habilidades_compativeis) / len(habilidades_requeridas)) * 100

        # Só recomenda se houver pelo menos alguma compatibilidade
        if percentual_compatibilidade > 0:
            recomendacoes.append({
                "vaga": vaga,
                "percentual_compatibilidade": round(percentual_compatibilidade, 2),
                "habilidades_compativeis": sorted([h.capitalize() for h in habilidades_compativeis]),
                "habilidades_faltantes": sorted([h.capitalize() for h in habilidades_faltantes])
            })

    # Ordena as recomendações da mais compatível para a menos compatível
    recomendacoes_ordenadas = sorted(recomendacoes, key=lambda x: x["percentual_compatibilidade"], reverse=True)

    return {
        "funcionario": funcionario_alvo,
        "recomendacoes": recomendacoes_ordenadas
    }

if __name__ == '__main__':
    # Exemplo de uso: Recomendações para a funcionária Ana Silva (ID 1)
    resultado_recomendacao = recomendar_vagas(1)
    print(json.dumps(resultado_recomendacao, indent=4, ensure_ascii=False))