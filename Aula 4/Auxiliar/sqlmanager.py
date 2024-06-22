from manage_sql import SQLITE


def criar_tabela(nomeTabela: str):
    
    database = SQLITE(nomeTabela)
    
    if nomeTabela == 'usuarios':
        database.criarTabela(
            nomeTabela=nomeTabela,
            Colunas=['nome', 'username', 'email', 'senha', 'cargo', 'status'],
            ColunasTipo=['TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT']
        )

def inserir_dados(nomeTabela: str, dados: list):
    
    database = SQLITE(nomeTabela)
    
    if nomeTabela == 'usuarios':
        database.inserirDados(
            nomeTabela=nomeTabela,
            Colunas=['nome', 'username', 'email', 'senha', 'cargo', 'status'],
            dados = dados
        )

def editar_dados(nomeTabela: str, dados: list):
    
    database = SQLITE(nomeTabela)
    
    if nomeTabela == 'usuarios':
        
        database.editarDados(
            nomeTabela=nomeTabela,
            Coluna=dados[0],
            Valor=dados[1],
            conditions=dados[2]
        )

def ver_dados(nomeTabela: str, conditions: str, colunas: list):
    
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