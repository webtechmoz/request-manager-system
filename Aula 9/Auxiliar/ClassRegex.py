import re

class REGEX:

    def verificar_email(self, email: str):
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        
        return re.match(regex, email) is not None


    def verificar_telefone(self, telefone: str):
        regex = r"^\+?(258)?\s?8[23456789]\d{7}$"

        return re.match(regex, telefone) is not None

    def validar_senha(self, senha: str):
        # Expressão regular para validar a senha
        regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^\w\d\s]).{6,}$'
        
        # Verifica se a senha corresponde à expressão regular
        return re.match(regex, senha) is not None

    def validar_nome(self, nome: str):
        regex = r'^[A-Za-zÀ-ú\s]+$'
        return re.match(regex, nome) is not None
