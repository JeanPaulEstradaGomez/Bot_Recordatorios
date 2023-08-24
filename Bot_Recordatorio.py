import tkinter as tk
from plyer import notification
import time
from datetime import datetime
from tkinter import messagebox

# Estructura de datos para almacenar los recordatorios
recordatorios = {}

def crear_recordatorio():
    tarea = tarea_entry.get()
    hora = str(hora_spinbox.get()).zfill(2)  # Formatea las horas con dos dígitos
    minuto = str(minuto_spinbox.get()).zfill(2)  # Formatea los minutos con dos dígitos
    am_pm = am_pm_var.get()  # Obtiene el valor de AM/PM

    # Convierte la hora a formato de 12 horas con ceros iniciales
    hora = f"{hora}:{minuto} {am_pm}"

    # Almacena el recordatorio en la estructura de datos
    recordatorios[len(recordatorios) + 1] = {
        'tarea': tarea,
        'hora': hora
    }

    # Borra los campos después de agregar el recordatorio
    tarea_entry.delete(0, 'end')
    hora_spinbox.delete(0, 'end')
    hora_spinbox.insert(0, '0')
    minuto_spinbox.delete(0, 'end')
    minuto_spinbox.insert(0, '0')

    messagebox.showinfo('Éxito', 'Recordatorio creado con éxito')

# Lista para almacenar los índices de los recordatorios que deben eliminarse
recordatorios_a_eliminar = []

def verificar_recordatorios():
    hora_actual = datetime.now().strftime("%I:%M %p")  # Formato de 12 horas con AM/PM
    for indice, recordatorio in recordatorios.items():
        tarea = recordatorio['tarea']
        hora = recordatorio['hora']

        # Compara la hora actual y la hora del recordatorio sin tener en cuenta AM/PM
        if hora_actual == hora:
            mensaje = f"Tarea: {tarea}\nHora: {hora_actual}"
            notification.notify(
                title='Recordatorio',
                message=mensaje,
                timeout=10
            )
            print(f'Notificación para {tarea} mostrada a las {hora_actual}')

            # Agrega el índice del recordatorio a la lista de eliminación
            recordatorios_a_eliminar.append(indice)

    # Elimina los recordatorios marcados para eliminación
    for indice in recordatorios_a_eliminar:
        del recordatorios[indice]

    # Limpia la lista de eliminación
    recordatorios_a_eliminar.clear()

# Función para actualizar el reloj
def actualizar_reloj():
    hora_actual = time.strftime("%I:%M:%S %p")  # Formato de 12 horas con AM/PM
    reloj_label.config(text=hora_actual)
    verificar_recordatorios()  # Verificar recordatorios cada vez que se actualiza el reloj
    ventana.after(1000, actualizar_reloj)

# Crear una ventana
ventana = tk.Tk()
ventana.title('Recordatorios')

# Un Frame principal para organizar los elementos
main_frame = tk.Frame(ventana)
main_frame.pack(padx=20, pady=20)

# Etiquetas y campos de entrada
tarea_label = tk.Label(main_frame, text='Tarea:')
tarea_label.grid(row=0, column=0, sticky='w')

tarea_entry = tk.Entry(main_frame, width=30)
tarea_entry.grid(row=0, column=1)

hora_label = tk.Label(main_frame, text='Horas : Minutos')
hora_label.grid(row=1, column=0, sticky='w')

# Un LabelFrame para los selectores de hora y minutos
hora_frame = tk.LabelFrame(main_frame, text='Hora:')
hora_frame.grid(row=1, column=1, padx=10, pady=5, sticky='w')

# Selector de hora
hora_spinbox = tk.Spinbox(hora_frame, from_=0, to=12, width=2)
hora_spinbox.grid(row=0, column=0, padx=5, pady=5, sticky='w')

# Selector de minuto
minuto_spinbox = tk.Spinbox(hora_frame, from_=0, to=59, width=2)
minuto_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky='w')

# Selector AM/PM
am_pm_var = tk.StringVar(value="Seleccione")
am_pm_menu = tk.OptionMenu(hora_frame, am_pm_var,'Ninguno', "AM", "PM")
am_pm_menu.grid(row=0, column=2, padx=5, pady=5, sticky='w')

# Posicionar el reloj al inicio
reloj_label = tk.Label(ventana, text='', font=('Helvetica', 20))
reloj_label.pack()

# Función para mostrar u ocultar la lista de tareas
mostrar_lista = False

def toggle_lista_tareas():
    global mostrar_lista
    if mostrar_lista:
        lista_tareas_frame.pack_forget()
        mostrar_lista = False
        mostrar_tareas_button.config(text="Mostrar Lista de Tareas")
    else:
        mostrar_lista_tareas()
        mostrar_lista = True
        mostrar_tareas_button.config(text="Cerrar Lista de Tareas")

# Marco para la lista de tareas
lista_tareas_frame = tk.Frame(ventana)

# Función para mostrar la lista de tareas
def mostrar_lista_tareas():
    lista_tareas_frame.pack()
    lista_tareas.delete(0, tk.END)  # Borra cualquier entrada previa en la lista
    for tarea, info in recordatorios.items():
        lista_tareas.insert(tk.END, f"Tarea: {tarea}, Hora: {info['hora']}")

# Crear una lista desplegable para mostrar las tareas
lista_tareas = tk.Listbox(lista_tareas_frame, width=40)
lista_tareas.pack()

# Botones para crear recordatorios y mostrar/ocultar lista de tareas
crear_button = tk.Button(main_frame, text='Crear Recordatorio', command=crear_recordatorio)
crear_button.grid(row=3, column=0, columnspan=3, pady=10)

mostrar_tareas_button = tk.Button(main_frame, text='Mostrar Lista de Tareas', command=toggle_lista_tareas)
mostrar_tareas_button.grid(row=4, column=0, columnspan=3)

# Actualizar el reloj cada segundo
actualizar_reloj()

ventana.mainloop()
