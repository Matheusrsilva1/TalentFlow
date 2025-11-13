import re
import json
import os

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
            funcionarios = json.load(f)
    except FileNotFoundError:
        print("Arquivos de dados não encontrados.")
        return

    mapa_funcionarios = {func['id']: func for func in funcionarios}

    # Cria uma expressão regular a partir da lista de skills (case-insensitive)
    regex_skills = r"\b(" + "|".join(re.escape(skill) for skill in SKILLS_CONHECIDAS) + r")\b"

    for projeto in projetos:
        for participante_id in projeto.get("participantes", []):
            if participante_id in mapa_funcionarios:
                funcionario = mapa_funcionarios[participante_id]
                habilidades_descobertas = set(funcionario.get("habilidades_descobertas", []))

                for tarefa in projeto.get("tarefas", []):
                    texto_tarefa = tarefa.get("descricao", "").lower()
                    
                    # Encontra todas as skills no texto da tarefa
                    skills_encontradas = re.findall(regex_skills, texto_tarefa, re.IGNORECASE)
                    
                    for skill in skills_encontradas:
                        habilidades_descobertas.add(skill.capitalize())
                
                funcionario["habilidades_descobertas"] = sorted(list(habilidades_descobertas))

    try:
        with open(caminho_funcionarios, 'w', encoding='utf-8') as f:
            json.dump(funcionarios, f, indent=4, ensure_ascii=False)
        print("Habilidades extraídas e atualizadas com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar o arquivo de funcionários: {e}")

if __name__ == '__main__':
    extrair_skills_dos_projetos()