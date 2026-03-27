# Script principal - Interfaz

import pandas as pd
import numpy as numpy
import re
import sys

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog, messagebox

# Importar modulos ____________________________________________________

from csv_processing import csv_processing
# from calculo_razones import calculo_razones

# _____________________________________________________________________

# Definicion de variables globales y funciones basicas ________________

global_font_title = ("Century Gothic", 12, "bold")
global_font_body = ("Century Gothic", 10)

BG_csv_file_path = None
ER_csv_file_path = None

# Definicion de funciones no para la gui ______________________________

# Checked
def csv_get_filename(ef = str):    # Funcion comando que le da funcionalidad a los botones de la primera ventana, desplegando el explorador de archivos para seleccionarlos
    if ef == "BG":
        global BG_csv_file_path
        BG_csv_file_path = askopenfilename()
    elif ef == "ER":
        global ER_csv_file_path
        ER_csv_file_path = askopenfilename()
    return

# Checked
def results_to_str(results = dict):    # Funcion que genera un string con el nombre de la razon y el valor; uno por linea, a partir del diccionario que contiene dichos valores.
    results_str = ""
    try:
        for key in results.keys():
            if results_str == "":
                results_str = str(key) + ": " + str(results[key])
            else:
                results_str = results_str + "\n" + str(key) + ": " + str(results[key])
    except Exception as e:
        print(f"Ocurrio un error al aplicar la funcion results_to_str\nEl error en cuestion es: {e}")
        sys.exit()
    return results_str

def one_line_str_to_multiline(string = str):   # Pendiente
    for index in range(len(string)):
        None
    return None


# Definicion de funciones para la gui ________________________________

def start_window(root=None, results_dict=dict):
    try:
        root.destroy() if root else None
        root = tk.Tk()

        # Botones
        csv_intake_button = tk.Button(root, text="Presiona aqui si cuentas con\n archivos .csv con la\n informacion de los estados financieros?", command=lambda: csv_intake_window(root=root, results_dict=results_dict), font=global_font_body)
        manual_intake_button = tk.Button(root, text = "Presiona aqui si buscas ingresar\n manualmente los datos para el calculo\n de las razones financieras", command=lambda: manual_intake_window(root=root), font=global_font_body)

        # Texto
        main_label = tk.Label(root, text="lorem ipsum blabla\nSelecciona la opcion adecuada", font=global_font_title)

        # Posicionamiento de los widgets
        main_label.grid(row=0, column=1, columnspan=3)
        csv_intake_button.grid(row=2, column=1, columnspan=1)
        manual_intake_button.grid(row=2, column=3, columnspan=1)

        root.mainloop()
    except Exception as e:
        print(f"Ocurrio un error al correr la funcion asociada a la ventana inicial, el error es: {e}")
        sys.exit()


def manual_intake_window(root=None):
    try:
        root.destroy() if root else None
        root = tk.Tk()

        # Botones
        back_button = tk.Button(root, text="Regresar", command=lambda: start_window(root=root, results_dict=None), font=global_font_body)
        next_button = tk.Button(root, text="Siguiente", command=None, font=global_font_body)

        # Text
        main_label = tk.Label(root, text="En esta ventana el usuario podra escoger\n las razones de su interes, y posteriormente \nle permitira ingresar los valores necesarios\n para hacer dichos calculos", font=global_font_title)

        # Menu de opciones
        options = ["razon 1", "razon 2", "razon 3"]
        option_chosen = tk.StringVar()
        option_chosen.set("Selecciona una opcion")

        options_menu = tk.OptionMenu(root, option_chosen, *options)
        options_menu.config(font=global_font_body)

        # Posicionamiento de widgets

        main_label.grid(row=0,column=0, columnspan=3)
        back_button.grid(row=2, column=0, columnspan=1, padx=15, pady=10)
        next_button.grid(row=2, column=3, columnspan=1, padx=15, pady=10)
        options_menu.grid(row=1,column=1)

        root.mainloop()

    except Exception as e:
        print(f"Ocurrio un error al correr la funcion asociada a la ventana inicial, el error es: {e}")
        sys.exit()

# Pendiente de evaluar funcionalidad
# Boton siguiente: FUNCIONA
# Boton Estado de Resultados: FUNCIONA
# Boton Balance general: FUNCIONA
def csv_intake_window(root=None, results_dict=dict):
    try:
        root.destroy() if root else None    # Tkinter funciona con ventanas. Dentro de las ventanas se ponen widgets (botones, texto, etc). Para poder regresar del dashboard
                                            # o de la ventana de resultado a la primera ventana, tenemos que agregar una opcion que nos permita destruir la ventana anterior.
        root = tk.Tk()    # Creamos una nueva ventana vacia

        # Botones
        BG_button = tk.Button(root, text="Presiona para ingresar el \n .csv del Balance General", command=lambda: csv_get_filename("BG"), font = global_font_body)
        ER_button = tk.Button(root, text="Presiona para ingresar el \n .csv del Estado de Resultados", command=lambda: csv_get_filename("ER"), font = global_font_body)
        next_button = tk.Button(root, text="Siguiente", command=lambda: results_window(root=root, results_dict=results_dict), font=global_font_body)
        back_button = tk.Button(root, text="Regresar", command=lambda: start_window(root=root, results_dict=None), font=global_font_body)
        
        # Checkbox
        manual_entry_checkbox = tk.Checkbutton(root, text="Tambien quieres ingresar/sustituir datos manualmente?", var=None, font=global_font_body)

        # Texto
        title_label = tk.Label(root, text="Ingresa los archivos .csv de los estados\n financieros (vease el manual de usuario para ver\n el formato de los archivos de entrada)", font=global_font_title)

        # Posicionamiento de widgets
        title_label.grid(row=0, column=0, columnspan=4, padx=30, pady=20)
        BG_button.grid(row=1, column=2, columnspan=1, padx=10, pady=20)
        ER_button.grid(row=1, column=3, columnspan=1, padx=10, pady=20)
        manual_entry_checkbox.grid(row=2, column=2, padx=15, pady=10)
        next_button.grid(row=3, column=3, padx=15, pady=10)
        back_button.grid(row=3, column=1, padx=15, pady=10)
        
        root.mainloop()
    except Exception as e:
        print(f"La funcion que genera la 1ra ventana fue la que ocaciono el error; el error es: {e}")
        sys.exit()


# Pendiente de evuluar funcionalidad
# Boton siguiente: FUNCIONA
# Boton regresar: FUNCIONA
def results_window(root=None, results_dict=dict):
    try:
        root.destroy() if root else None
        root = tk.Tk()

        # Botones
        back_button = tk.Button(root, text="Regresar", command=lambda: csv_intake_window(root=root, results_dict=results_dict), font=global_font_body)
        next_button = tk.Button(root, text="Siguiente", command=lambda: dashboard_window(root=root, results_dict=results_dict), font=global_font_body)

        # Texto
        title_label = tk.Label(root, text="Los valores de las razones financieras son:", font=global_font_title)
        results_label =tk.Label(root, text=results_to_str(results_dict), font=global_font_body)

        # Posicionamiento de widgets
        title_label.grid(row=0, column=0, columnspan=4, padx=30, pady=20)
        results_label.grid(row=1, column=0, columnspan=4, padx=50, pady=100)
        back_button.grid(row=2, column=0, columnspan=1, padx=15, pady=10)
        next_button.grid(row=2, column=3, columnspan=1, padx=15, pady=10)

        root.mainloop()
    except Exception as e:
        print(f"La funcion que genera la 2da ventana fue la que ocaciono el error; el error es: {e}")
        sys.exit()

# Pendiente de evaluar funcionalidad
# Boton regresar: FUNCIONA
def dashboard_window(root, results_dict=dict):
    try:
        root.destroy()
        root = tk.Tk()

        # Botones
        back_button = tk.Button(root, text="Regresar", command=lambda: results_window(root=root, results_dict=results_dict), font=global_font_body)

        # Texto
        message_label = tk.Label(root, text="No se ha implementado esto :(", font=global_font_title)

        # Posicionamiento de los widgets
        message_label.pack()
        back_button.pack()

        root.mainloop()
    except Exception as e:
        print(f"La funcion que genera la 3ra ventana fue la que ocaciono el error; el error es: {e}")
        sys.exit()

#_________________________________________________________________________________


# Seccion de pruebas _____________________________________________________________

resultados_de_prueba = {"cuenta 1": 100,
                         "llave 2": 95,
                         "llave 3": 90,
                         "llave 4": 85}

#print(results_to_str(diccionario_de_prueba))

#archivo_temp = "ER"
#csv_get_filename(archivo_temp)
#print(ER_csv_file_path)

#________________________________________________________________________________


# Seccion de ejecucion del codigo principal______________________________________

start_window(results_dict=resultados_de_prueba)
print(BG_csv_file_path, ER_csv_file_path)



# Pendientes

# 1. Comentar partes del codigo
# 2. Optimizar funciones
#       - No estar cargando con los argumentos entre funciones para ventanas