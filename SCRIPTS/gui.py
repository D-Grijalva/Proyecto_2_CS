import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import logging
from typing import Optional, Dict, Callable

# Configuramos logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes
FONT_TITLE = ("Century Gothic", 12, "bold")
FONT_BODY = ("Century Gothic", 10)


# Pendientes

# 1. Remplazar el uso de Optional, por simplemente usar el simbolo de disyuncion "|"
# 2. En ventana inicial: Agregar un cuadro de texto que muestre el nombre del .csv seleccionado
# 3. En ventana de resultados: Agregar un menu de opciones para seleccionar tipo de analisis
#        - Simple impresion de valores de razones
#        - Razon 1: Analisis automatico
#        - ... Razon 6: Analisis automatico
# 4. Plantear GIU para ingesta de datos
# 5. Agregar ventana de arhivos incorrectos, con mesaje de que es lo que tienen incorrecto
#        - Por el momento, solo mensajes de archivo incorrecto y no permitir avanzar de ventana
# 6. Cambiar ventana incial a ventana de ingesta y definir una nueva ventana presentacion con hipervnculo al manual de usuario

# Funciones temporales - repreesntan funciones que se importaran de otros modulos no hechos

# Esta funcion es para probar la implementacion de la validacion en la GUI
def csv_validation(bg_path: str, er_path: str) -> Dict:
    return {"BG": (True, "El balance general no respeta la ecuacion contable A=P+C\nEl balance general no respeta regla 1\nEl balance general no respeta regla 2\n"), "ER": (True, "")}

# Esta funcion es para hacer los analisis automaticos de las razones financieras
def auto_analysis(results_dict: dict) -> Dict:
    return {"Raw results": "Raw results",
            "Razones de solvencia": "Tal y cual razon de solvencia esta muy alta\nTal y cual muy baja\nTal y cual en valores sanos para una aseguradora",
            "Razones de Liquidez":"Nada que comentar\nDe nuevo nada que comentar"}

# Clases
class PathAndResults:
    """Definir esta clase sustituye el uso de variables globales para los path y el diccionario de resultados"""
    def __init__(self):
        self.bg_csv_path: Optional[str] = None    # Type hint: Indica que el atributo bf_csv_path de la clase ApplicationState es string o None (sin asignar valor).
        self.er_csv_path: Optional[str] = None    # Type hint: Indica que el atributo er_csv_path de la clase ApplicationState es string o None (sin asignar valor).
        self.results: Dict = {}    # Type hint: Indica que el atributo results de la clase ApplicationState es un dict (sin asignar valor).
        
    def set_bg_path(self, path: str) -> None:
        self.bg_csv_path = path
    
    def set_er_path(self, path: str) -> None:
        self.er_csv_path = path
    
    def set_results(self, results: Dict) -> None:
        self.results = results

# Para la implementacion de validacion en la GUI hice cambios en las siguientes funciones:
# csv_validation: Funcion temporal. Esta funcion se importara del modulo de lectura,limpieza y validacion.
# - start_window : Cambie el comando que llama el boton siguiente; sigue siendo results_window, pero ahora con un argumento extra, por tanto ahora es una lambda function (el argumento es la funcion temporal csv_validation)
# - dashboard_window : Mismo cambio que en start_window
# - results_window: Cambios sustanciales
#       - Agregue un argumento con type hint dict asociado al diccionario de resultados de la validacion de los csv
#       - Agregue un condicional para mandar mensaje si no se paso la validacion, y continuar el programa si se paso con exito

# Para la implementacion de impresion de resultados automaticos en la GUI hice los siguientes cambios:
# auto_analysis: Funcion temporal. Esta funcion se importara del modulo de calculo de razones financieras.
# - results_window: Cambios sustanciales

class ProgramaGui:
    """Clase principal de la GUI del programa"""

    def __init__(self, results_dict: Optional[Dict] = None, csv_validation_results_dict: Optional[Dict] = None):
        self.state = PathAndResults()    # El atributo .state de la clase ProgramGui es una instancia de la clase PathAndResults
        if results_dict:
            self.state.set_results(results_dict)
        if csv_validation_results_dict:
            self.state.set_csv_validation_results(csv_validation_results_dict)
        self.root: Optional[tk.Tk] = None    # El atributo .root de la clase ProgramGui es una ventana de tkinter o None
    
    def _create_window(self) -> tk.Tk:
        """Crear y retornar una nueva ventana de Tkinter"""
        if self.root:
            self.root.destroy()
        self.root = tk.Tk()
        return self.root

    def _show_error(self, message: str) -> None:
        """Muestra mensaje de error al usuario"""
        logger.error(message)    # No se que hace esto, lo saque de internet
        messagebox.showerror("Error", message)
    
    def _show_info(self, title: str, message: str) -> None:
        """Muestra mensaje de informacion al usuario"""
        messagebox.showinfo(title, message)

    def _select_csv_file(self, file_type: str) -> None:
        """Abre explorador de archivos y guarda el exact path del archivo en el atributo adecuado de la instancia de la clase PathAndResults "self.state" 

        Argumentos: file_type: "BG" (Balance General) o "ER" (Estado de Resultados)
        """
        try:
            path = askopenfilename(title=f"Escoge el archivo .csv de {file_type}",
                                   initialdir="../INPUTS",
                                   filetypes=[("CSV files", "*.csv")])
            if path:
                if file_type == "BG":
                    self.state.set_bg_path(path)
                    self._show_info("Exito", "Se cargo el archivo del Balance General exitosamente")
                elif file_type == "ER":
                    self.state.set_er_path(path)
                    self,self._show_info("Exito", "Se cargo el archivo del Estado de Resultados exitosamente")
        except Exception as e:
            self._show_error(f"Error en la seleccion del archivo: {str(e)}")

    @staticmethod    # A partir de aqui se definen metodos dentro de la clase que no requieren acceso a 'self' u otros datos de la clase
    def _dict_to_string(data: Dict) -> str:
        """Convierte diccionarios a un string formateado"""
        if not data:
            return "No hay datos disponibles"
        return "\n".join(f"{key}: {value}" for key, value in data.items())
    
    def start_window(self) -> None:
        """Ventana INICIAL - Donde el usuario ingresa los archivos .csv de los estados financieros"""
        try:
            self._create_window()

            # Definicion de widgets de la ventana

            # Texto
            title_label = tk.Label(self.root, text="Carga los archivos CSV de los estados financieros", font=FONT_TITLE)

            # Botones
            bg_button = tk.Button(self.root, text="Selecciona el csv del Balance General", command=lambda: self._select_csv_file("BG"), font = FONT_BODY)
            er_button = tk.Button(self.root, text="Selecciona el csv del Estado de Resultados", command=lambda: self._select_csv_file("ER"), font = FONT_BODY)
            next_button = tk.Button(self.root, text="Siguiente", command=lambda: self.results_window(csv_validation(bg_path=self.state.bg_csv_path, er_path=self.state.er_csv_path)), font=FONT_BODY)
            
            # Posicionamiento de widgets
            title_label.grid(row=0, column=0, columnspan=4, padx=20, pady=20)
            bg_button.grid(row=1, column=1, padx=10, pady=20)
            er_button.grid(row=1, column=3, padx=10, pady=20)
            next_button.grid(row=3, column=3, padx=15, pady=10)

            self.root.mainloop()
        except Exception as e:
            self._show_error(f"Error en la ventana inicial: {str(e)}")
            logger.exception("Excepcion en la ventana de ingesta de csv")

    def results_window(self, csv_validation_results: Dict) -> None:
        """Visualizacion de resultados"""
        try:

            # Antes de crear una nueva ventana y cerrar la actual, se tienen que analizar los resultados de la validacion de los csv
            
            if csv_validation_results:
                error_dict = {}
                for key, value in csv_validation_results.items():    # Esto se puede hacer con list comprehension
                    if value[0] == False:   # No paso la validacion
                        error_dict[key]=value[1]
                
                if error_dict:
                    self._show_info("Ops. Los archivos .csv no son validos",self._dict_to_string(error_dict))
                    return None

            self._create_window()
            
            # Definicion de widgest de la ventana

            # Menu de opciones
            analysis_options = ["Raw results", "Razones de solvencia", "Razones de liquidez"]
            chosen_analysis = tk.StringVar()
            chosen_analysis.set("Selecciona tipo de analisis")
            analysis_menu = tk.OptionMenu(self.root, chosen_analysis, *analysis_options, command=None)
            analysis_menu.config(font=FONT_BODY)

            # Texto
            title_label = tk.Label(self.root, text="Resultado del calculo de las razones financieras", font=FONT_TITLE  )
            results_text = self._dict_to_string(self.state.results)
            results_label = tk.Label(self.root, text=results_text, font=FONT_BODY, justify="left")

            # Botones
            back_button = tk.Button(self.root, text="Regresar", command=self.start_window, font=FONT_BODY)
            next_button = tk.Button(self.root, text="Siguiente", command=self.dashboard_window, font=FONT_BODY)

            # Posicionamiento de widgets
            title_label.grid(row=0, column=0, columnspan=4, padx=20, pady=20)
            results_label.grid(row=2, column=0, columnspan=4, padx=50, pady=50)
            analysis_menu.grid(row=1, column=2, padx=20, pady=20)
            back_button.grid(row=3, column=0, padx=15, pady=10)
            next_button.grid(row=3, column=3, padx=15, pady=10)

            self.root.mainloop()
        except Exception as e:
            self._show_error(f"Error en la ventana de resultados: {str(e)}")
            logger.exception("Excepcion en la ventana de resultados")

    def dashboard_window(self) -> None:
        """Ventana temporal - Representa la ventana del dashboard (no implementado aun)"""
        try:
            self._create_window()

            message_label = tk.Label(self.root, text="Dashboard\n(No implementado aun)", font=FONT_TITLE)
            back_button = tk.Button(self.root, text="Regresar", command=lambda: self.results_window(None), font=FONT_BODY )

            message_label.pack(padx=20, pady=20)
            back_button.pack(padx=15, pady=10)
            
            self.root.mainloop()
        except Exception as e:
            self._show_error(f"Error en la ventana del dashboard: {str(e)}")
            logger.exception("Error en la ventana del dashboard")

    def get_paths(self) -> tuple:
        """Get file paths for processing by other modules"""
        return (self.state.bg_csv_path, self.state.er_csv_path)