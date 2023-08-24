import tkinter as tk
from tkinter import messagebox
from plyer import notification
import time
from datetime import datetime


# Estructura de datos para almacenar los recordatorios
recordatorios = {}

def crear_recordatorio():
    tarea = tarea_entry.get()
    hora = str(hora_spinbox.get()).zfill(2)  # Formatea las horas con dos dígitos
    minuto = str(minuto_spinbox.get()).zfill(2)  # Formatea los minutos con dos dígitos
    am_pm = am_pm_var.get()  # Obtiene el valor de AM/PM

    # Convierte la hora a formato de 12 horas con ceros iniciales
    hora = f"{hora}:{minuto} {am_pm}"

    # Obtiene la fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    # Almacena el recordatorio en la estructura de datos
    recordatorios[len(recordatorios) + 1] = {
        'tarea': tarea,
        'hora': hora,
        'fecha': fecha_actual
    }

    # Borra los campos después de agregar el recordatorio
    tarea_entry.delete(0, 'end')
    hora_spinbox.delete(0, 'end')
    minuto_spinbox.delete(0, 'end')

    messagebox.showinfo('Éxito', 'Recordatorio creado con éxito')

def verificar_recordatorios():
    hora_actual = datetime.now().strftime("%I:%M %p")  # Formato de 12 horas con AM/PM
    print('Hora Actual:', hora_actual)
    for _, recordatorio in recordatorios.items():
        tarea = recordatorio['tarea']
        hora = recordatorio['hora']
        fecha = recordatorio['fecha']

        # Parsea la hora del recordatorio a un objeto de tiempo
        hora_recordatorio = datetime.strptime(hora, "%I:%M %p").strftime("%I:%M %p")

        # Compara solo las horas y los minutos, excluyendo AM/PM
        if hora_actual[:-6] == hora_recordatorio[:-6]:
            mensaje = f"Tarea: {tarea}\nHora: {hora}\nFecha: {fecha}"
            notification.notify(
                title='Recordatorio',
                message=mensaje,
                timeout=10
            )
        print('Hora Actual:', hora_recordatorio)

            
# Función para actualizar el reloj
def actualizar_reloj():
    hora_actual = time.strftime("%I:%M:%S %p")  # Formato de 12 horas con AM/PM
    reloj_label.config(text=hora_actual)
    ventana.after(1000, actualizar_reloj)

# Crear una ventana
ventana = tk.Tk()
ventana.title('Bot de Recordatorios')
ventana.geometry('400x350')  # Tamaño personalizado

# Etiquetas y campos de entrada
tarea_label = tk.Label(ventana, text='Tarea:')
tarea_label.pack()
tarea_entry = tk.Entry(ventana)
tarea_entry.pack()

hora_label = tk.Label(ventana, text='Horas : Minutos')
hora_label.pack()

# Crear un contenedor para los Spinbox de hora y minuto
hora_frame = tk.Frame(ventana)
hora_frame.pack()

hora_spinbox = tk.Spinbox(hora_frame, from_=1, to=12, width=2)
hora_spinbox.pack(side=tk.LEFT)  # Al lado izquierdo

minuto_spinbox = tk.Spinbox(hora_frame, from_=0, to=59, width=2)
minuto_spinbox.pack(side=tk.RIGHT)  # Al lado derecho

# Selector de AM/PM
am_pm_var = tk.StringVar(value="AM")  # Valor inicial AM
am_pm_menu = tk.OptionMenu(ventana, am_pm_var, "AM", "PM")
am_pm_menu.pack()

# Etiqueta y campo de entrada para la fecha actual
fecha_actual_label = tk.Label(ventana, text='Fecha Actual:')
fecha_actual_label.pack()
fecha_actual_entry = tk.Entry(ventana)
fecha_actual_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
fecha_actual_entry.pack()

# Botones para crear y mostrar recordatorios
crear_button = tk.Button(ventana, text='Crear Recordatorio', command=crear_recordatorio)
crear_button.pack()

mostrar_button = tk.Button(ventana, text='Mostrar Recordatorios', command=verificar_recordatorios)
mostrar_button.pack()

# Configurar un temporizador para verificar recordatorios cada minuto
ventana.after(60000, verificar_recordatorios) 

# Crear una etiqueta para mostrar la hora actual
reloj_label = tk.Label(ventana, text='', font=('Helvetica', 20))
reloj_label.pack()

# Actualizar el reloj cada segundo
actualizar_reloj()

ventana.mainloop()
