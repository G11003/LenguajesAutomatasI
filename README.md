# Lenguajes y Automatas I 
### Espinosa Antelis Gabriela Dyvheke
### 21200592


# Tarea 2.2 16 abril 2024
## Bot de Validación de Contraseñas

Este proyecto consiste en el desarrollo de un bot de Telegram para la verificación de contraseñas, realizado como parte del curso de Lenguajes y Autómatas por un estudiante de sistemas. El objetivo principal fue aplicar los conocimientos adquiridos en el aula, así como mejorar las habilidades en programación y desarrollo de aplicaciones.

## Paso a Paso en la Creación del Bot

### 1. Investigación y Planificación
Antes de comenzar con el desarrollo, se investigaron la API de Telegram y las bibliotecas de Python disponibles para interactuar con ella. Se definieron los objetivos y funcionalidades básicas del bot, como la verificación de contraseñas.

### 2. Configuración del Entorno de Desarrollo
Se configuró un entorno de desarrollo Python en la computadora del estudiante y se aseguró tener instaladas las bibliotecas necesarias, especialmente `python-telegram-bot`.

### 3. Obtención del Token de Acceso
Se registró el bot en Telegram y se obtuvo un token de acceso único, utilizado para autenticar todas las solicitudes realizadas al API de Telegram.

### 4. Desarrollo del Código
Se escribió el código del bot, dividiéndolo en funciones para manejar diferentes comandos y tipos de mensajes. Se incluyeron funciones para manejar los comandos `/start` y `/help`, así como la validación de contraseñas mediante expresiones regulares.

## Explicación de Partes Fundamentales del Código

### Token de Acceso
El token de acceso (`TOKEN`) se define como una variable global y se utiliza para autenticar las solicitudes del bot a la API de Telegram. Es crucial para el funcionamiento del bot y debe mantenerse seguro.

### Funciones de Manejo de Comandos
Se definen funciones como `start()` y `help()` para manejar los comandos `/start` y `/help` respectivamente. Estas funciones responden a los usuarios con mensajes específicos cuando se envían estos comandos.

### Función de Validación de Contraseña
La función `regex_reply()` utiliza expresiones regulares para validar las contraseñas proporcionadas por los usuarios. Un patrón regex específico se emplea para verificar criterios de seguridad como la presencia de letras mayúsculas, minúsculas, dígitos y caracteres especiales.

### Función de Respuesta a Mensajes
La función `reply_message()` maneja los mensajes que no son comandos ni contraseñas. Responde a saludos, solicitudes de ayuda y otros mensajes con respuestas predeterminadas.

### Configuración del Bot
En la función `main()`, se crea un objeto `Updater` que recibe actualizaciones de Telegram. Se agregan manejadores para diferentes tipos de eventos, como comandos, mensajes de texto y expresiones regulares.

## Conclusiones

Este proyecto de desarrollo de un bot de Telegram para la validación de contraseñas proporcionó una experiencia práctica invaluable al estudiante. Pudo aplicar los conceptos teóricos aprendidos en el curso de Lenguajes y Autómatas en un entorno de desarrollo real. Además, el proceso de investigación, planificación y desarrollo del bot le ayudó a mejorar sus habilidades en programación y resolución de problemas. Esta experiencia no solo fortaleció su comprensión de los conceptos de programación, sino que también le proporcionó una herramienta útil que podría compartir y mejorar en el futuro.

## Capturas del funcionamiento del bot
![Captura de pantalla 2024-04-15 235951](https://github.com/G11003/LenguajesAutomatasI/assets/160692077/c11d9e3b-dd3e-41ad-b260-0c491603978a)
![Captura de pantalla 2024-04-16 000153](https://github.com/G11003/LenguajesAutomatasI/assets/160692077/48b0e99f-0187-4ed0-afd5-3670dc05416a)




