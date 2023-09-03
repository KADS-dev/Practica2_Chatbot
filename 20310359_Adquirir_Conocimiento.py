import sqlite3

# Crear o conectar a la base de datos
conn = sqlite3.connect('temas.db')
cursor = conn.cursor()

# Crear la tabla para almacenar temas y respuestas si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS temas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tema TEXT,
        respuesta TEXT
    )
''')
conn.commit()

# Respuestas predeterminadas
respuestas_predeterminadas = [
    ("Hola, ¿Cómo estas?", "Estoy bien, gracias. ¿De qué te gustaría hablar?"),
    ("¿De qué te gustaría hablar?", "Puedo hablar de muchos temas. ¿Tienes alguna pregunta en particular?"),
]

# Función para buscar una respuesta en la base de datos o agregar una nueva respuesta
def buscar_respuesta(pregunta):
    # Buscar en la base de datos
    cursor.execute("SELECT respuesta FROM temas WHERE tema=?", (pregunta,))
    resultado = cursor.fetchone()
    
    if resultado:
        return resultado[0]
    else:
        # Si no se encuentra una respuesta, preguntar al usuario y guardar en la base de datos
        nueva_respuesta = input(f"No tengo una respuesta para '{pregunta}'. ¿Qué debería responder? ")
        cursor.execute("INSERT INTO temas (tema, respuesta) VALUES (?, ?)", (pregunta, nueva_respuesta))
        conn.commit()
        return nueva_respuesta

# Función principal del chatbot
def chatbot():
    print("¡Hola! Soy un chatbot. Puedes preguntarme cualquier cosa.")
    while True:
        entrada_usuario = input("Usuario: ")
        
        # Salir del bucle si el usuario ingresa 'salir'
        if entrada_usuario.lower() == 'salir':
            break
        
        # Buscar una respuesta predeterminada
        for pregunta, respuesta in respuestas_predeterminadas:
            if pregunta.lower() in entrada_usuario.lower():
                print("Chatbot:", respuesta)
                break
        else:
            # Si no se encuentra una respuesta predeterminada, buscar en la base de datos
            respuesta = buscar_respuesta(entrada_usuario)
            print("Chatbot:", respuesta)

# Ejecutar el chatbot
if __name__ == "__main__":
    chatbot()

# Cerrar la conexión a la base de datos
conn.close()