import json
from pathlib import Path
from openpyxl import Workbook

base = Path(__file__).resolve().parent.parent
json_path = base / 'app' / 'data' / 'funcionarios.json'
out_path = base / 'app' / 'data' / 'funcionarios_modelo.xlsx'

with json_path.open('r', encoding='utf-8') as f:
    data = json.load(f)
funcionarios = data.get('funcionarios', [])

wb = Workbook()
ws = wb.active
ws.title = 'Funcionarios'
ws.append(['id', 'nome', 'cargo', 'email', 'habilidades_declaradas'])

for f in funcionarios:
    habilidades = ', '.join(f.get('habilidades_declaradas', []))
    ws.append([f.get('id'), f.get('nome'), f.get('cargo'), f.get('email'), habilidades])

wb.save(out_path)
