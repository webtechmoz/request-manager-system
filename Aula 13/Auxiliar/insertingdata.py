from sqlmanager import *

# Dados para as requisições
requisicoes = [
    ('Tecnologia', 'Hardware', 'Notebook', 'Dell Inspiron 15', 10, '06/07/24', 'Pendente', 'wtech'),
    ('Tecnologia', 'Software', 'Licença Windows', 'Licença Windows 10 Pro', 20, '06/07/24', 'Pendente', 'wtech'),
    ('Tecnologia', 'Acessórios', 'Mouse', 'Mouse Logitech', 50, '06/07/24', 'Pendente', 'wtech'),
    ('Tecnologia', 'Hardware', 'Monitor', 'Monitor Samsung 24"', 15, '06/07/24', 'Pendente', 'wtech'),
    ('Tecnologia', 'Software', 'Antivírus', 'Licença Norton', 30, '06/07/24', 'Pendente', 'wtech'),
    ('Marketing', 'Mídia', 'Câmera', 'Câmera Canon EOS', 5, '06/07/24', 'Pendente', 'cinezoidy'),
    ('Marketing', 'Software', 'Adobe Premiere', 'Licença Adobe Premiere Pro', 10, '06/07/24', 'Pendente', 'cinezoidy'),
    ('Marketing', 'Acessórios', 'Tripé', 'Tripé Manfrotto', 25, '06/07/24', 'Pendente', 'cinezoidy'),
    ('Marketing', 'Hardware', 'Iluminação', 'Kit de iluminação LED', 8, '06/07/24', 'Pendente', 'cinezoidy'),
    ('Marketing', 'Software', 'Final Cut Pro', 'Licença Final Cut Pro X', 15, '06/07/24', 'Pendente', 'cinezoidy')
]

criar_tabela('pendentes')

for req in requisicoes:
    
    dados = {
        'departamento': req[0],
        'categoria': req[1],
        'produto': req[2],
        'descricao': req[3],
        'quantidades': req[4],
        'dataRequisicao': req[5],
        'status': req[6],
        'usuario': req[7]
    }
    
    inserir_dados(
        nomeTabela='pendentes',
        dados=dados
    )