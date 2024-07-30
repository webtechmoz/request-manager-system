from manage_sql import SQLITE

def criar_tabela(nomeTabela: str):
    
    database = SQLITE(nomeTabela)
    
    if nomeTabela == 'usuarios':
        colunas = {
            'nome': 'TEXT',
            'usename': 'TEXT',
            'email': 'TEXT',
            'senha': 'TEXT',
            'cargo': 'TEXT',
            'status': 'TEXT'
        }
    
    elif nomeTabela == 'pendentes':
        colunas = {
            'departamento': 'TEXT',
            'categoria': 'TEXT',
            'produto': 'TEXT',
            'descricao': 'TEXT',
            'quantidades': 'NUMERIC',
            'dataRequisicao': 'TEXT',
            'status': 'TEXT',
            'usuario': 'TEXT'
        }
    
    elif nomeTabela == 'arquivadas':
        colunas = {
            'indice': 'INTEGER',
            'departamento': 'TEXT',
            'categoria': 'TEXT',
            'produto': 'TEXT',
            'descricao': 'TEXT',
            'quantidades': 'NUMERIC',
            'precoUnitario': 'NUMERIC',
            'valor': 'NUMERIC',
            'dataRequisicao': 'TEXT',
            'status': 'TEXT',
            'usuario': 'TEXT',
            'dataDecisao': 'TEXT',
            'notas': 'TEXT',
            'fornecedor': 'TEXT',
            'cidade': 'TEXT',
            'morada': 'TEXT',
            'nuit': 'INTEGER',
            'iva': 'NUMERIC'
        }
    
    database.criarTabela(
        nomeTabela=nomeTabela,
        Colunas=[col for col in colunas.keys()],
        ColunasTipo=[col for col in colunas.values()]
    )

def inserir_dados(nomeTabela: str, dados: dict):
    
    database = SQLITE(nomeTabela)
    
    database.inserirDados(
        nomeTabela=nomeTabela,
        Colunas=[col for col in dados.keys()],
        dados = [data for data in dados.values()]
    )

def editar_dados(nomeTabela: str, dados: list):
    
    database = SQLITE(nomeTabela)
        
    database.editarDados(
        nomeTabela=nomeTabela,
        Coluna=dados[0],
        Valor=dados[1],
        conditions=dados[2]
    )

def apagar_dados(nomeTabela: str, conditions: str):
    
    database = SQLITE(nomeTabela)
    
    database.apagarDados(
        nomeTabela=nomeTabela,
        conditions=conditions
    )


def ver_dados(nomeTabela: str, conditions: str = '', colunas: str = '*'):
    
    database = SQLITE(nomeTabela)
    
    dados = database.verDados(
        nomeTabela=nomeTabela,
        conditions=conditions,
        colunas=colunas
    )
    
    return dados

def encriptar_valor(value: str):
    
    database = SQLITE('usuarios')
    encrypted = database.encryptPass(value)
    
    return encrypted