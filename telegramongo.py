from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging
import os
from dotenv import load_dotenv
import pymongo
from telethon import TelegramClient

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém as credenciais do arquivo .env
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
mongo_uri = os.getenv('MONGO_URI')  # URI do MongoDB
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')  # Token do bot do Telegram

# Conexão com o MongoDB
client_mongo = pymongo.MongoClient(mongo_uri)
db = client_mongo['Mongotelegram']  # Nome do seu banco de dados
collection = db['mensagens']  # Nome da coleção

# Cria uma instância do cliente do Telegram
client = TelegramClient('sessao_telegram', api_id, api_hash)

# Definição dos grupos
grupos_vagas_ti = [
    ("Vagas de TI para Todos", -1001052992679),
    ("Vagas TI Pleno e Sênior🇧🇷🤝🏻", -1001899966696),
    ("vagasprajr", -1001822167516),
    ("Vagas Para Tecnologia", -1001266916012),
    ("Tem Vaga Pra Jr.", -1001584468892),
    ("Vagas TI [Remoto]", -1001431382018),
]

async def coletar_mensagens():
    """Coleta mensagens dos grupos e atualiza no MongoDB."""
    logger.info("Iniciando a coleta de mensagens dos grupos.")
    
    # Limpa as mensagens anteriores
    logger.info("Limpando mensagens antigas no banco de dados.")
    collection.delete_many({})
    
    # Loop através dos grupos
    for nome_grupo, grupo_id in grupos_vagas_ti:
        logger.info(f"Coletando mensagens do grupo: {nome_grupo} (ID: {grupo_id})")
        mensagens = []

        # Obtém o histórico de mensagens do grupo usando async for
        async for message in client.iter_messages(grupo_id, limit=10):
            if message.text:
                mensagens.append({"type": "text", "content": message.text})
            else:
                media_type = "unknown"
                if message.photo:
                    media_type = "photo"
                elif message.video:
                    media_type = "video"
                elif message.document:
                    media_type = "document"
                elif message.voice:
                    media_type = "voice"
                elif message.audio:
                    media_type = "audio"
                
                mensagens.append({"type": media_type, "content": f"{media_type.capitalize()} not available"})
        
        # Salva as mensagens no MongoDB
        if mensagens:
            logger.info(f"Salvando {len(mensagens)} mensagens do grupo {nome_grupo} no MongoDB.")
            collection.insert_one({"grupo": nome_grupo, "mensagens": mensagens})
        else:
            logger.warning(f"Nenhuma mensagem encontrada no grupo {nome_grupo}.")

async def resetar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para atualizar mensagens no MongoDB."""
    logger.info("Comando /resetar recebido. Atualizando mensagens.")
    await coletar_mensagens()  # Chama a função coletar_mensagens() usando await
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Mensagens atualizadas com sucesso!")

async def exibir_mensagens_por_grupo(update: Update, context: ContextTypes.DEFAULT_TYPE, nome_grupo):
    """Exibe as mensagens de um grupo específico numeradas da mais recente para a mais antiga."""
    logger.info(f"Exibindo mensagens do grupo: {nome_grupo}")
    
    # Busca as mensagens do grupo específico
    documento = collection.find_one({"grupo": nome_grupo})
    
    if not documento:
        resposta = f"Nenhuma mensagem encontrada para o grupo {nome_grupo}."
        logger.warning(resposta)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resposta)
        return
    
    # Monta a resposta com as mensagens do grupo
    resposta = f"Mensagens do grupo: {nome_grupo}\n\n"
    
    # Numerar as mensagens da mais recente para a mais antiga
    total_mensagens = len(documento['mensagens'])
    for i, msg in enumerate(reversed(documento['mensagens']), start=1):
        numero_mensagem = total_mensagens - i + 1  # Mensagem 1 é a mais recente, 10 a mais antiga
        resposta += f"Mensagem {numero_mensagem}: ===============\n{msg['content']} \n"
        resposta += f"Tipo: {msg['type']}\n\n"
    
    # Envia a resposta em partes se necessário
    max_length = 4096
    for i in range(0, len(resposta), max_length):
        parte = resposta[i:i + max_length]
        await context.bot.send_message(chat_id=update.effective_chat.id, text=parte)


# Funções de comandos para cada grupo
async def vagas_todos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await exibir_mensagens_por_grupo(update, context, "Vagas de TI para Todos")

async def vagas_pleno_senior(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await exibir_mensagens_por_grupo(update, context, "Vagas TI Pleno e Sênior🇧🇷🤝🏻")

async def vagas_jr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await exibir_mensagens_por_grupo(update, context, "vagasprajr")

async def vagas_tecnologia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await exibir_mensagens_por_grupo(update, context, "Vagas Para Tecnologia")

async def vagas_remoto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await exibir_mensagens_por_grupo(update, context, "Vagas TI [Remoto]")

async def vagas_jr_tem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await exibir_mensagens_por_grupo(update, context, "Tem Vaga Pra Jr.")

# Função para listar comandos no /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde com uma lista de comandos disponíveis."""
    logger.info("Comando /start recebido.")
    comandos = (
        "/start - Lista todos os comandos disponíveis\n"
        "/resetar - Atualiza as mensagens de todos os grupos\n"
        "/vagas_todos - Exibe as ultimas 10 mensagens do grupo 'Vagas de TI para Todos'\n"
        "/vagas_pleno_senior - Exibe as ultimas 10 mensagens do grupo 'Vagas TI Pleno e Sênior'\n"
        "/vagas_jr - Exibe as ultimas 10 mensagens do grupo 'vagasprajr'\n"
        "/vagas_tecnologia - Exibe as ultimas 10 mensagens do grupo 'Vagas Para Tecnologia'\n"
        "/vagas_remoto - Exibe as ultimas 10 mensagens do grupo 'Vagas TI [Remoto]'\n"
        "/vagas_jr_tem - Exibe as ultimas 10 mensagens do grupo 'Tem Vaga Pra Jr.'\n"
    )
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Bem-vindo ao bot de vagas de TI! Aqui estão os comandos disponíveis:\n\n{comandos}")

def main():
    """Função principal para iniciar o bot."""
    client.start()  # Inicia o cliente do Telegram
    logger.info("Cliente do Telegram iniciado com sucesso.")
    application = ApplicationBuilder().token(telegram_bot_token).build()

    # Comandos do bot
    application.add_handler(CommandHandler('start', start))  # Comando /start
    application.add_handler(CommandHandler('resetar', resetar))
    application.add_handler(CommandHandler('vagas_todos', vagas_todos))
    application.add_handler(CommandHandler('vagas_pleno_senior', vagas_pleno_senior))
    application.add_handler(CommandHandler('vagas_jr', vagas_jr))
    application.add_handler(CommandHandler('vagas_tecnologia', vagas_tecnologia))
    application.add_handler(CommandHandler('vagas_remoto', vagas_remoto))
    application.add_handler(CommandHandler('vagas_jr_tem', vagas_jr_tem))

    # Inicia o bot
    logger.info("Bot iniciado e escutando comandos.")
    application.run_polling()

# Verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    main()
