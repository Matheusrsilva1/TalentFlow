from flask import Blueprint, render_template, request, abort
import json

main = Blueprint('main', __name__)

def load_data():
    with open('app/data/funcionarios.json', 'r', encoding='utf-8') as f:
        funcionarios = json.load(f)['funcionarios']
    with open('app/data/vagas.json', 'r', encoding='utf-8') as f:
        vagas = json.load(f)
    return funcionarios, vagas

@main.route('/')
@main.route('/dashboard')
def dashboard():
    funcionarios, _ = load_data()
    query = request.args.get('busca_habilidade', '')
    
    if query:
        funcionarios_filtrados = []
        for f in funcionarios:
            habilidades_declaradas = f.get('habilidades_declaradas', [])
            habilidades_descobertas = [h['skill'] for h in f.get('habilidades_descobertas', [])]
            habilidades = habilidades_declaradas + habilidades_descobertas
            if any(query.lower() in habilidade.lower() for habilidade in habilidades):
                funcionarios_filtrados.append(f)
        funcionarios = funcionarios_filtrados

    return render_template('dashboard.html', funcionarios=funcionarios, query=query)

@main.route('/perfil/<int:id>')
def perfil(id):
    funcionarios, vagas = load_data()
    funcionario = next((f for f in funcionarios if f['id'] == id), None)
    
    if funcionario is None:
        abort(404)

    habilidades_funcionario = set(funcionario.get('habilidades_declaradas', [])) | set(h['skill'] for h in funcionario.get('habilidades_descobertas', []))
    
    recomendacoes = []
    for vaga in vagas:
        habilidades_vaga = set(vaga.get('habilidades_requeridas', []))
        habilidades_em_comum = habilidades_funcionario.intersection(habilidades_vaga)
        
        if habilidades_em_comum:
            compatibilidade = round((len(habilidades_em_comum) / len(habilidades_vaga)) * 100) if habilidades_vaga else 0
            if compatibilidade > 30: # Limiar de compatibilidade
                recomendacoes.append({
                    "id": vaga['id'],
                    "titulo": vaga['titulo'],
                    "compatibilidade": compatibilidade,
                    "habilidades_em_comum": list(habilidades_em_comum),
                    "habilidades_a_desenvolver": list(habilidades_vaga - habilidades_funcionario)
                })
    
    recomendacoes.sort(key=lambda x: x['compatibilidade'], reverse=True)
    
    funcionario['recomendacoes_vagas'] = recomendacoes

    return render_template('perfil.html', funcionario=funcionario)

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404