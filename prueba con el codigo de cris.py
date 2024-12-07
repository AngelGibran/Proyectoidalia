from openai import OpenAI
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
#Utilizamos datetime para obtener la fecha y hora actual de esta forma el modelo entenderá instrucciones mas complejas como "el proximo martes" o "en 3 días"
fecha_hora_actual = datetime.now()

#Como se utilizo una variable de entorno para la clave del Api no es necesario colocarla aquí
client = OpenAI()


# Inicializar la ventana de Tkinter
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal

# Abrir cuadro de diálogo para seleccionar un archivo de texto
#esto se va a modificar cuando el pozos me diga que pedo
file_path = filedialog.askopenfilename(title="Seleccionar un archivo de texto", filetypes=[("Archivos de texto", "*.txt")])

# Verificar si se seleccionó un archivo
if file_path:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print("Ocurrió un error al leer el archivo:", e)
else:
    print("No se seleccionó ningún archivo.")

# se utiliza el role para que gpt entienda que hacer y content es el contenido del archivo que seleccionamos  
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system",
         "content": f"Eres un asistente muy util y perspicaz que toma notas en reuniones. Recuerda que la fecha de hoy es {fecha_hora_actual} en caso de no tener fecha de inicio asume que empieza en este momento, lee detalladamente la reunion y para cada tarea asignada en la reunión devuelve un diccionario JSON con el formato: {{'tipo': 'tarea','accion': 'valor','nombre_proyecto': 'valor', 'nombre_tarea':'valor', 'nombre_persona': 'valor', 'estado' : 'valor', 'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'valor', 'resumen': 'valor'}}, accion indica si se desea eliminar o crear, prioridad solo puede tomar valores baja media y alta, el nombre de la persona debe ser el nombre de la persona a la que se le asigno la tarea. Para cada proyecto debes devolver un json con el siguiente formato{{'tipo':'proyecto', 'accion':'valor', 'nombre_proyecto': 'valor','estado':'valor',  'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'valor', 'resumen': 'valor'}} s  si se desea hacer un nuevo sprint devuelve un diccionario json con el formato: {{ tipo : sprint, nombre : valor, fecha_inicio : YYYY-MM-DD, fecha_fin : YYYY-MM-DD}} si alguno de los valores no viene en el texto, trata de inferirlo solo con la informacion del texto, si no se puede dejalo vacío. únicamente devuelve el JSON sin comentarios ni explicación"
         },
        
        {
            "role": "user",
            "content": content
        }
    ]
)
response_dict = completion.to_dict()

# Capturar el mensaje de salida
output_message = response_dict['choices'][0]['message']['content']

# Guardar el mensaje en una variable
resultado = output_message

# Imprimir el resultado
print("Resultado:", resultado)

#print(completion.choices[0].message) esta otra madre es para imprimir el mensaje en consola, pero no te deja interactuar con el mensaje
#print(fecha_hora_actual) ajaj esta madre era para ver si si inferia las fechas chido Xd (si jala)


