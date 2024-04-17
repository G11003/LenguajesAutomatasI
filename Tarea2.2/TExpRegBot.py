import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Token de acceso del bot
TOKEN = '7131017056:AAHX1B4c9Hk03OO2H66boyAMIWrJv5Yh-a0'

# Función para manejar el comando /start
def start(update, context):
    update.message.reply_text('Hola! Soy un bot de Telegram para la tarea 2.2 de 21200592.')

# Función para manejar el comando /help
def help(update, context):
    update.message.reply_text("""Puedo ayudarte a identificar si tu contraseña cumple los estándares básicos de seguridad.""")

# Función para manejar mensajes que coincidan con expresiones regulares
def regex_reply(update, context):
    # Texto del mensaje recibido
    text = update.message.text
    
    # Expresión regular para validar la contraseña
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!"#$%&/()=?¡¿\-_*+<>])[A-Za-z\d!"#$%&/()=?¡¿\-_*+<>]{8,15}$'
    
    # Verifica si la contraseña cumple con la expresión regular
    match = re.match(pattern, text)
    if match:
        response_text = "¡Tu contraseña es segura :)!"
    else:
        response_text = """¡Tu contraseña no es segura :(!
        Te recomiendo verifiques lo siguiente:
        Debe contener al menos una letra minúscula.
        Debe contener al menos una letra mayúscula.
        Debe contener al menos un dígito.
        Debe contener al menos un carácter especial.
        No debe tener más de tres números consecutivos.
        Debe tener al menos 8 caracteres de longitud."""
    
    # Envía la respuesta al usuario
    update.message.reply_text(response_text)

# Función para manejar el mensaje de saludo, ayuda y contraseña
def reply_message(update, context):
    # Texto del mensaje recibido
    text = update.message.text.lower()

    # Verifica si el mensaje es un saludo
    if text in ['hola', 'holi', 'ola', 'hi', 'hello']:
        response_text = "¡Hola! Ingresa el comando /help para saber mi función."
    elif text in ['contraseña', 'ayuda', 'aiuda']:
        response_text = "¡Con gusto! Ingresa la contraseña que deseas probar."
    elif text in ['gracias', 'adios', 'Gracias', 'Adios']:
        response_text = "¡Hasta luego! Si necesitas más ayuda, aquí estaré."
    else:
        response_text = "Perdona, no te he entendido :("
    
    # Envía la respuesta al usuario
    update.message.reply_text(response_text)

# Función principal para iniciar el bot
def main():
    # Crea el objeto Updater y pasa el token
    updater = Updater(TOKEN, use_context=True)

    # Obtiene el despachador para registrar manejadores
    dp = updater.dispatcher

    # Agrega un manejador para el comando /start
    dp.add_handler(CommandHandler("start", start))

    # Agrega un manejador para el comando /help
    dp.add_handler(CommandHandler("help", help))

    # Agrega un manejador para responder a expresiones regulares
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command & ~Filters.regex(r'^[!"#$%&/()=?¡¿\-_*+<>A-Za-z\d]{8,15}$'), reply_message))

    # Agrega un manejador para responder a la contraseña
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command & Filters.regex(r'^[!"#$%&/()=?¡¿\-_*+<>A-Za-z\d]{8,15}$'), regex_reply))

    # Inicia el bot
    updater.start_polling()

    # Espera a que el bot reciba una señal para detenerse
    updater.idle()

if __name__ == '__main__':
    main()