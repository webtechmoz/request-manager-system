# Recuperar Senha

Este projeto é uma aplicação para recuperação de senha. O código está organizado em várias pastas para manter uma estrutura modular e fácil de entender.

## Índice

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Utilização](#utilização)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Estrutura do Projeto

- **main.py**: Arquivo principal que inicia a aplicação.
- **.vscode/settings.json**: Configurações específicas para o Visual Studio Code.
- **Auxiliar/controls.py**: Contém funções auxiliares e controles utilizados na aplicação.
- **Views/recuperarSenha.py**: Define a interface de usuário para a recuperação de senha.

## Instalação

1. Clone o repositório para o seu ambiente local:
    ```bash
    git clone https://github.com/webtechmoz/request-manager-system.git
    ```

2. Navegue até o diretório do projeto:
    ```bash
    cd recuperar-senha
    ```

3. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use: venv\Scripts\activate
    ```

4. Instale as dependências necessárias:
    ```bash
    pip install flet
    ```

## Utilização

1. Execute o arquivo principal para iniciar a aplicação:
    ```bash
    python main.py
    ```

## Estrutura de Pastas

- **Recuperar Senha/**: Diretório principal do projeto.
  - **main.py**: Arquivo de inicialização da aplicação.
  - **.vscode/**: Configurações do editor.
    - **settings.json**: Configurações específicas do Visual Studio Code.
  - **Auxiliar/**: Funções auxiliares.
    - **controls.py**: Controles e funções auxiliares.
  - **Views/**: Interfaces de usuário.
    - **recuperarSenha.py**: Interface de recuperação de senha.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma nova branch com as suas alterações:
    ```bash
    git checkout -b minha-feature
    ```

3. Faça commit das suas alterações:
    ```bash
    git commit -m 'Minha nova feature'
    ```

4. Envie as suas alterações para a branch principal:
    ```bash
    git push origin minha-feature
    ```

5. Crie um novo Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
