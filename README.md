# Telegram Job Bot - Vagas de TI

Este é um bot do Telegram desenvolvido em Python que coleta mensagens de grupos de vagas de TI e as armazena em um banco de dados MongoDB. O bot permite exibir as mensagens mais recentes numeradas de cada grupo de vagas via comandos do Telegram.

## Funcionalidades

- Coleta mensagens dos grupos de vagas de TI e as armazena no MongoDB.
- Exibe as mensagens mais recentes numeradas (da mais nova para a mais antiga).
- Comandos para reiniciar a coleta de mensagens e exibir as mensagens armazenadas.

## Requisitos

- **Python 3.10+**
- Conta no Telegram para criar um bot (usando o [BotFather](https://core.telegram.org/bots#botfather))
- API do Telegram (ID e Hash)
- MongoDB para armazenar as mensagens
- Variáveis de ambiente configuradas

## Instalação

1. Clone o repositório para o seu ambiente local:

    ```bash
    git clone https://github.com/seu-usuario/telegram-job-bot.git
    cd telegram-job-bot
    ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. Instale as dependências do projeto:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure as variáveis de ambiente. Crie um arquivo `.env` com base no arquivo de exemplo `.env.example`:

    ```bash
    cp .env.example .env
    ```

5. Edite o arquivo `.env` e adicione suas credenciais (API do Telegram, telefone, MongoDB, etc.):

    ```env
    API_ID=1234567
    API_HASH=abcd1234efgh5678ijkl9012mnopqrst
    PHONE_NUMBER=+5511999999999
    TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abc
    MONGO_URI=mongodb://localhost:27017
    ```

6. Inicie o bot:

    ```bash
    python main.py
    ```

## Comandos do Bot

- `/start` — Exibe uma lista de comandos disponíveis.
- `/resetar` — Atualiza as mensagens dos grupos de vagas no MongoDB.
- `/exibir` — Exibe as mensagens coletadas de todos os grupos armazenados no MongoDB.
- `/grupo_nome` — Exibe as mensagens do grupo específico (exemplo: `/Vagas_TI_Pleno`).

## Como Obter Credenciais do Telegram

1. Registre-se como desenvolvedor no [My Telegram](https://my.telegram.org) para obter seu **API ID** e **API Hash**.
2. Crie um bot no Telegram usando o [BotFather](https://core.telegram.org/bots#botfather) para obter o **TOKEN** do bot.

## Estrutura do Projeto

