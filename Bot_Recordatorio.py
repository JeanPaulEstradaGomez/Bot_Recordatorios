import tkinter as tk
from tkinter import messagebox
from plyer import notification

# Estructura de datos para almacenar los recordatorios
recordatorios = {}

# Función para crear un nuevo recordatorio
def crear_recordatorio():
    tarea = tarea_entry.get()
    hora = hora_entry.get()
    fecha = fecha_entry.get()

    # Almacena el recordatorio en la estructura de datos
    recordatorios[len(recordatorios) + 1] = {
        'tarea': tarea,
        'hora': hora,
        'fecha': fecha
    }

    # Borra los campos después de agregar el recordatorio
    tarea_entry.delete(0, 'end')
    hora_entry.delete(0, 'end')
    fecha_entry.delete(0, 'end')

    messagebox.showinfo('Éxito', 'Recordatorio creado con éxito')

# Función para mostrar recordatorios activos y notificar
def mostrar_recordatorios():
    for _, recordatorio in recordatorios.items():
        tarea = recordatorio['tarea']
        hora = recordatorio['hora']
        fecha = recordatorio['fecha']
        mensaje = f"Tarea: {tarea}\nHora: {hora}\nFecha: {fecha}"
        notification.notify(
            title='Recordatorio',
            message=mensaje,
            timeout=10
        )

# Crear una ventana
ventana = tk.Tk()
ventana.title('Bot de Recordatorios')

# Etiquetas y campos de entrada
tarea_label = tk.Label(ventana, text='Tarea:')
tarea_label.pack()
tarea_entry = tk.Entry(ventana)
tarea_entry.pack()

hora_label = tk.Label(ventana, text='Hora:')
hora_label.pack()
hora_entry = tk.Entry(ventana)
hora_entry.pack()

fecha_label = tk.Label(ventana, text='Fecha:')
fecha_label.pack()
fecha_entry = tk.Entry(ventana)
fecha_entry.pack()

# Botones para crear y mostrar recordatorios
crear_button = tk.Button(ventana, text='Crear Recordatorio', command=crear_recordatorio)
crear_button.pack()

mostrar_button = tk.Button(ventana, text='Mostrar Recordatorios', command=mostrar_recordatorios)
mostrar_button.pack()

ventana.mainloop()
