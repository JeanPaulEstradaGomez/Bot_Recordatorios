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
    minuto_spinbox.delete(0, 'end')

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

# ...

# Función para actualizar el reloj
def actualizar_reloj():
    hora_actual = time.strftime("%I:%M:%S %p")  # Formato de 12 horas con AM/PM
    reloj_label.config(text=hora_actual)
    verificar_recordatorios()  # Verificar recordatorios cada vez que se actualiza el reloj
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

# Botón para crear recordatorios
crear_button = tk.Button(ventana, text='Crear Recordatorio', command=crear_recordatorio)
crear_button.pack()

# Crear una etiqueta para mostrar la hora actual
reloj_label = tk.Label(ventana, text='', font=('Helvetica', 20))
reloj_label.pack()

# Actualizar el reloj cada segundo
actualizar_reloj()

ventana.mainloop()
