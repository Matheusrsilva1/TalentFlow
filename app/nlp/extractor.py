import re
import json
import os
from datetime import datetime

# Lista de skills conhecidas (pode ser expandida e gerenciada em um arquivo separado)
SKILLS_CONHECIDAS = [
    "python", "pandas", "power bi", "bi", "sql", "otimização", "api", "rest",
    "flask", "java", "spring", "microserviços", "gestão de estoque", "transporte",
    "sap", "excel", "análise financeira", "contabilidade", "gestão de projetos",
    "logística", "supply chain management", "liderança", "comunicação", "docker", "django"
]

def extrair_skills_dos_projetos():
    """
    Lê os arquivos de projetos e funcionários, extrai as skills das tarefas
    usando regex e atualiza o JSON de funcionários com as novas habilidades descobertas.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    caminho_projetos = os.path.join(base_dir, 'data', 'projetos.json')
    caminho_funcionarios = os.path.join(base_dir, 'data', 'funcionarios.json')

    try:
        with open(caminho_projetos, 'r', encoding='utf-8') as f:
            projetos = json.load(f)
        with open(caminho_funcionarios, 'r', encoding='utf-8') as f:
            funcionarios_data = json.load(f)
    except FileNotFoundError:
        print("Arquivos de dados não encontrados.")
        return

    funcionarios = funcionarios_data.get('funcionarios', [])
    mapa_funcionarios = {func['id']: func for func in funcionarios}

    # Cria uma expressão regular a partir da lista de skills (case-insensitive)
    regex_skills = r"\b(" + "|".join(re.escape(skill) for skill in SKILLS_CONHECIDAS) + r")\b"

    def normalizar_skill(s):
        s = s or ''
        s = re.sub(r"\s*\(.*?\)\s*", '', s)
        return s.strip().lower()

    hoje = datetime.utcnow().strftime('%Y-%m-%d')

    for projeto in projetos:
        for participante_id in projeto.get("participantes", []):
            if participante_id in mapa_funcionarios:
                funcionario = mapa_funcionarios[participante_id]
                existentes = funcionario.get("habilidades_descobertas", [])
                existentes_map = {normalizar_skill(item.get("skill")) for item in existentes if isinstance(item, dict)}

                novos = set()
                for tarefa in projeto.get("tarefas", []):
                    texto_tarefa = tarefa.get("descricao", "").lower()
                    skills_encontradas = re.findall(regex_skills, texto_tarefa, re.IGNORECASE)
                    for skill in skills_encontradas:
                        k = normalizar_skill(skill)
                        if k and k not in existentes_map:
                            novos.add(k)

                for k in sorted(novos):
                    existentes.append({
                        "skill": k.capitalize(),
                        "origem": "NLP (projetos.json)",
                        "data": hoje
                    })

                funcionario["habilidades_descobertas"] = existentes

    try:
        with open(caminho_funcionarios, 'w', encoding='utf-8') as f:
            json.dump({"funcionarios": funcionarios}, f, indent=4, ensure_ascii=False)
        print("Habilidades extraídas e atualizadas com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar o arquivo de funcionários: {e}")

if __name__ == '__main__':
    extrair_skills_dos_projetos()
