from openpyxl import Workbook
import os

def main():
    path = os.path.join('app', 'data', 'usuarios_exemplo.xlsx')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = 'Funcionarios'
    ws.append(['id', 'nome', 'cargo', 'email', 'habilidades_declaradas'])
    rows = [
        [None, 'Ana Souza', 'Analista de Dados', 'ana.souza@example.com', 'Python, SQL, Power BI'],
        [None, 'Bruno Lima', 'Desenvolvedor Back-end', 'bruno.lima@example.com', 'Node.js, MongoDB, Docker'],
        [None, 'Carla Mendes', 'Cientista de Dados', 'carla.mendes@example.com', 'Python, Pandas, Scikit-learn'],
        [None, 'Diego Alves', 'Engenheiro DevOps', 'diego.alves@example.com', 'AWS, Terraform, CI/CD'],
        [None, 'Eduarda Nunes', 'Desenvolvedora Front-end', 'eduarda.nunes@example.com', 'React, TypeScript, CSS'],
    ]
    for r in rows:
        ws.append(r)
    wb.save(path)
    print(path)

if __name__ == '__main__':
    main()