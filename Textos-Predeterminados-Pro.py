import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, simpledialog, ttk
import json
import os
from tkinter import font

def crear_interfaz() -> None:
    ventana = tk.Tk()
    ventana.title("Editor de Textos Avanzado ++")
    ventana.geometry("900x650")
    ventana.resizable(True, True)
    
    # Paleta de colores mejorada
    COLOR_PRIMARIO = "#2B579A"
    COLOR_SECUNDARIO = "#FFFFFF"
    COLOR_BORDE = "#E1E1E1"
    COLOR_ACENTO = "#D83B01"
    COLOR_EXITO = "#00B050"
    COLOR_TEXTO = "#000000"
    COLOR_PLACEHOLDER = "#909090"
    COLOR_HOVER = "#1A365D"
    
    # Configuración de fuentes
    try:
        fuente_titulo = font.Font(family="Segoe UI", size=16, weight="bold")
        fuente_normal = font.Font(family="Segoe UI", size=10)
        fuente_boton = font.Font(family="Segoe UI", size=9)
    except:
        fuente_titulo = font.Font(size=16, weight="bold")
        fuente_normal = font.Font(size=10)
        fuente_boton = font.Font(size=9)
    
    # Configuración avanzada de estilos
    estilo = ttk.Style()
    estilo.theme_use('default')
    
    estilo.configure('TButton', 
                    font=fuente_boton,
                    background=COLOR_PRIMARIO,
                    foreground=COLOR_SECUNDARIO,
                    borderwidth=0,
                    focusthickness=3,
                    focuscolor=COLOR_PRIMARIO,
                    relief='flat')
    
    estilo.map('TButton',
              background=[
                  ('disabled', COLOR_PLACEHOLDER),
                  ('pressed', COLOR_ACENTO),
                  ('active', COLOR_HOVER)],
              foreground=[
                  ('disabled', COLOR_SECUNDARIO),
                  ('pressed', COLOR_SECUNDARIO),
                  ('active', COLOR_SECUNDARIO)],
              relief=[
                  ('pressed', 'sunken'),
                  ('!pressed', 'flat')])
    
    # Configuración de la ventana principal
    ventana.grid_rowconfigure(1, weight=1)
    ventana.grid_columnconfigure(0, weight=1)
    ventana.config(bg=COLOR_SECUNDARIO)
    
    # Barra de título
    barra_titulo = tk.Frame(ventana, bg=COLOR_PRIMARIO, height=40)
    barra_titulo.grid(row=0, column=0, sticky="ew")
    barra_titulo.grid_propagate(False)
    
    label_titulo = tk.Label(barra_titulo, 
                          text="Editor de Textos Avanzado ++", 
                          font=fuente_titulo, 
                          bg=COLOR_PRIMARIO, 
                          fg=COLOR_SECUNDARIO)
    label_titulo.pack(side=tk.LEFT, padx=16, pady=4)
    
    # Contenedor principal
    contenedor_principal = tk.Frame(ventana, bg=COLOR_SECUNDARIO, padx=8, pady=8)
    contenedor_principal.grid(row=1, column=0, sticky="nsew")
    contenedor_principal.grid_rowconfigure(1, weight=1)
    contenedor_principal.grid_columnconfigure(0, weight=1)
    
    # Frame para botones de textos
    frame_botones_texto = tk.Frame(contenedor_principal, bg=COLOR_SECUNDARIO)
    frame_botones_texto.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
    
    label_botones = tk.Label(frame_botones_texto, 
                           text="Textos Predeterminados", 
                           font=fuente_titulo,
                           fg=COLOR_PRIMARIO,
                           bg=COLOR_SECUNDARIO)
    label_botones.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 8), columnspan=4)
    
    # Área de texto principal
    frame_texto = tk.Frame(contenedor_principal, bg=COLOR_BORDE, bd=1, relief=tk.SOLID)
    frame_texto.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
    frame_texto.grid_rowconfigure(0, weight=1)
    frame_texto.grid_columnconfigure(0, weight=1)
    
    texto = scrolledtext.ScrolledText(
        frame_texto, 
        wrap="word", 
        font=fuente_normal,
        bg=COLOR_SECUNDARIO,
        fg=COLOR_TEXTO,
        insertbackground=COLOR_PRIMARIO,
        selectbackground=COLOR_PRIMARIO,
        selectforeground=COLOR_SECUNDARIO,
        padx=8,
        pady=8
    )
    texto.grid(row=0, column=0, sticky="nsew")
    
    # Frame para botones inferiores
    frame_botones_adicionales = tk.Frame(contenedor_principal, bg=COLOR_SECUNDARIO)
    frame_botones_adicionales.grid(row=2, column=0, sticky="ew", padx=8, pady=8)
    
    archivo_mensajes = "ETA.json"
    
    class ToolTip:
        def __init__(self, widget, text, color=COLOR_PRIMARIO):
            self.widget = widget
            self.text = text
            self.color = color
            self.tooltip = None
            self.widget.bind("<Enter>", self.show_tooltip)
            self.widget.bind("<Leave>", self.hide_tooltip)
        
        def show_tooltip(self, event=None):
            x, y, _, _ = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 25
            
            self.tooltip = tk.Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(self.tooltip, text=self.text, bg=self.color, fg=COLOR_SECUNDARIO,
                           font=fuente_normal, justify=tk.LEFT, padx=8, pady=4)
            label.pack()
        
        def hide_tooltip(self, event=None):
            if self.tooltip:
                self.tooltip.destroy()
                self.tooltip = None
    
    def nuevo_mensaje():
        limpiar_texto()
        texto.focus_set()
        mostrar_notificacion("Nuevo", "Listo para crear nuevo mensaje desde cero", COLOR_EXITO)
    
    def actualizar_texto(titulo: str, mensaje: str) -> None:
        contenido = f"--- {titulo} ---\n\n{mensaje}"
        texto.delete("1.0", tk.END)
        texto.insert(tk.END, contenido)
    
    def limpiar_texto() -> None:
        texto.delete("1.0", tk.END)
    
    def copiar_texto() -> None:
        try:
            ventana.clipboard_clear()
            ventana.clipboard_append(texto.get("1.0", tk.END))
            mostrar_notificacion("Copiado", "Contenido copiado al portapapeles.", COLOR_EXITO)
        except Exception as e:
            mostrar_notificacion("Error", f"Error al copiar: {str(e)}", COLOR_ACENTO)
    
    def mostrar_notificacion(titulo, mensaje, color=COLOR_PRIMARIO):
        notificacion = tk.Toplevel(ventana)
        notificacion.title("")
        notificacion.geometry("300x100")
        notificacion.resizable(False, False)
        notificacion.configure(bg=COLOR_SECUNDARIO)
        notificacion.transient(ventana)
        notificacion.grab_set()
        
        x = ventana.winfo_x() + (ventana.winfo_width() // 2) - 150
        y = ventana.winfo_y() + (ventana.winfo_height() // 2) - 50
        notificacion.geometry(f"+{x}+{y}")
        
        tk.Frame(notificacion, bg=color, height=5).pack(fill=tk.X)
        tk.Label(notificacion, text=titulo, font=fuente_titulo, bg=COLOR_SECUNDARIO, fg=color).pack(pady=(10, 0))
        tk.Label(notificacion, text=mensaje, bg=COLOR_SECUNDARIO, fg=COLOR_TEXTO, wraplength=280).pack(pady=5)
        
        btn_frame = tk.Frame(notificacion, bg=COLOR_SECUNDARIO)
        btn_frame.pack(pady=5, fill=tk.X)
        ttk.Button(btn_frame, text="Aceptar", style='TButton', command=notificacion.destroy).pack(side=tk.RIGHT, padx=10)
        notificacion.after(3000, notificacion.destroy)
    
    def guardar_mensaje(edicion=False, titulo_original=None) -> None:
        contenido = texto.get("1.0", tk.END).strip()
        if not contenido:
            mostrar_notificacion("Advertencia", "Contenido vacío.", COLOR_ACENTO)
            return
    
        lineas = contenido.split("\n")
        titulo_existente = lineas[0][4:-4] if lineas and lineas[0].startswith("--- ") and lineas[0].endswith(" ---") else ""
    
        titulo = simpledialog.askstring("Guardar mensaje", 
                                      "Introduce el título:",
                                      initialvalue=titulo_existente)
        if not titulo:
            return
    
        if lineas and lineas[0].startswith("--- ") and lineas[0].endswith(" ---"):
            mensaje = "\n".join(lineas[2:])
        else:
            mensaje = contenido
    
        mensajes = cargar_mensajes()
        
        if edicion and titulo_original:
            if titulo_original != titulo:
                del mensajes[titulo_original]
        
        mensajes[titulo] = mensaje
        
        try:
            with open(archivo_mensajes, 'w', encoding='utf-8') as f:
                json.dump(mensajes, f, ensure_ascii=False, indent=4)
            mostrar_notificacion("Guardado", f"Mensaje '{titulo}' guardado.", COLOR_EXITO)
            crear_botones_mensajes()
        except Exception as e:
            mostrar_notificacion("Error", f"Error al guardar: {str(e)}", COLOR_ACENTO)
    
    def cargar_mensajes() -> dict:
        if not os.path.exists(archivo_mensajes):
            return {titulo: mensaje for titulo, mensaje in botones_info_default}
        try:
            with open(archivo_mensajes, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {titulo: mensaje for titulo, mensaje in botones_info_default}
    
    def eliminar_mensaje() -> None:
        mensajes = cargar_mensajes()
        if not mensajes:
            mostrar_notificacion("Eliminar", "No hay mensajes.", COLOR_PRIMARIO)
            return
            
        dialogo = tk.Toplevel(ventana)
        dialogo.title("Eliminar mensaje")
        dialogo.geometry("350x350")
        dialogo.transient(ventana)
        dialogo.grab_set()
        dialogo.configure(bg=COLOR_SECUNDARIO)
        
        tk.Label(dialogo, text="Selecciona mensaje a eliminar", 
               font=fuente_titulo, bg=COLOR_SECUNDARIO, fg=COLOR_PRIMARIO).pack(pady=(15, 10))
        
        frame_lista = tk.Frame(dialogo, bg=COLOR_SECUNDARIO, bd=1, relief=tk.SOLID)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, font=fuente_normal,
                           bg=COLOR_SECUNDARIO, fg=COLOR_TEXTO,
                           selectbackground=COLOR_PRIMARIO, selectforeground=COLOR_SECUNDARIO)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for titulo in mensajes.keys():
            listbox.insert(tk.END, titulo)
            
        frame_botones = tk.Frame(dialogo, bg=COLOR_SECUNDARIO)
        frame_botones.pack(fill=tk.X, padx=15, pady=15)
        
        def confirmar_eliminar():
            seleccion = listbox.curselection()
            if not seleccion:
                mostrar_notificacion("Advertencia", "Selecciona un mensaje.", COLOR_ACENTO)
                return
                
            titulo = listbox.get(seleccion[0])
            confirmar = tk.Toplevel(dialogo)
            confirmar.title("Confirmar eliminación")
            confirmar.geometry("300x150")
            confirmar.transient(dialogo)
            confirmar.grab_set()
            confirmar.configure(bg=COLOR_SECUNDARIO)
            
            x = dialogo.winfo_x() + (dialogo.winfo_width() // 2) - 150
            y = dialogo.winfo_y() + (dialogo.winfo_height() // 2) - 75
            confirmar.geometry(f"+{x}+{y}")
            
            tk.Label(confirmar, text="¿Eliminar este mensaje?", 
                   font=fuente_normal, bg=COLOR_SECUNDARIO, fg=COLOR_TEXTO).pack(pady=(20, 5))
            tk.Label(confirmar, text=f"'{titulo}'", 
                   font=fuente_normal, bg=COLOR_SECUNDARIO, fg=COLOR_PRIMARIO).pack(pady=5)
            
            frame_btns = tk.Frame(confirmar, bg=COLOR_SECUNDARIO)
            frame_btns.pack(pady=15)
            
            def eliminar_confirmado():
                mensajes.pop(titulo)
                with open(archivo_mensajes, 'w', encoding='utf-8') as f:
                    json.dump(mensajes, f, ensure_ascii=False, indent=4)
                mostrar_notificacion("Eliminado", f"Mensaje '{titulo}' eliminado.", COLOR_EXITO)
                confirmar.destroy()
                dialogo.destroy()
                crear_botones_mensajes()
            
            ttk.Button(frame_btns, text="Sí, eliminar", style='TButton', command=eliminar_confirmado).pack(side=tk.LEFT, padx=5)
            ttk.Button(frame_btns, text="Cancelar", command=confirmar.destroy).pack(side=tk.LEFT, padx=5)
                
        ttk.Button(frame_botones, text="Eliminar", style='TButton', command=confirmar_eliminar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=dialogo.destroy).pack(side=tk.RIGHT, padx=5)
    
    def editar_mensaje() -> None:
        mensajes = cargar_mensajes()
        if not mensajes:
            mostrar_notificacion("Editar", "No hay mensajes.", COLOR_PRIMARIO)
            return
            
        dialogo = tk.Toplevel(ventana)
        dialogo.title("Edición Completa de Mensaje")
        dialogo.geometry("600x450")
        dialogo.transient(ventana)
        dialogo.grab_set()
        dialogo.configure(bg=COLOR_SECUNDARIO)
        
        # Frame principal
        frame_principal = tk.Frame(dialogo, bg=COLOR_SECUNDARIO)
        frame_principal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Selección de mensaje
        tk.Label(frame_principal, text="Seleccionar mensaje:", 
               font=fuente_normal, bg=COLOR_SECUNDARIO).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        combo_mensajes = ttk.Combobox(frame_principal, 
                                    values=list(mensajes.keys()),
                                    font=fuente_normal,
                                    state="readonly")
        combo_mensajes.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Campos de edición
        tk.Label(frame_principal, text="Nuevo título:", 
               font=fuente_normal, bg=COLOR_SECUNDARIO).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        entry_titulo = ttk.Entry(frame_principal, font=fuente_normal)
        entry_titulo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame_principal, text="Contenido:", 
               font=fuente_normal, bg=COLOR_SECUNDARIO).grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        
        texto_contenido = scrolledtext.ScrolledText(frame_principal,
                                                  wrap="word",
                                                  font=fuente_normal,
                                                  height=10)
        texto_contenido.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        
        # Botones de acción
        frame_botones = tk.Frame(frame_principal, bg=COLOR_SECUNDARIO)
        frame_botones.grid(row=3, column=0, columnspan=2, pady=10)
        
        def cargar_datos(event=None):
            titulo = combo_mensajes.get()
            if titulo:
                entry_titulo.delete(0, tk.END)
                entry_titulo.insert(0, titulo)
                texto_contenido.delete("1.0", tk.END)
                texto_contenido.insert(tk.END, mensajes[titulo])
        
        combo_mensajes.bind("<<ComboboxSelected>>", cargar_datos)
        
        def guardar_cambios():
            titulo_original = combo_mensajes.get()
            nuevo_titulo = entry_titulo.get().strip()
            nuevo_contenido = texto_contenido.get("1.0", tk.END).strip()
            
            if not nuevo_titulo or not nuevo_contenido:
                mostrar_notificacion("Error", "Todos los campos son requeridos", COLOR_ACENTO)
                return
                
            if titulo_original != nuevo_titulo and nuevo_titulo in mensajes:
                mostrar_notificacion("Error", "¡El título ya existe!", COLOR_ACENTO)
                return
                
            try:
                del mensajes[titulo_original]
                mensajes[nuevo_titulo] = nuevo_contenido
                
                with open(archivo_mensajes, 'w', encoding='utf-8') as f:
                    json.dump(mensajes, f, ensure_ascii=False, indent=4)
                
                crear_botones_mensajes()
                mostrar_notificacion("Éxito", "Mensaje actualizado correctamente", COLOR_EXITO)
                dialogo.destroy()
            except Exception as e:
                mostrar_notificacion("Error", f"Error al guardar: {str(e)}", COLOR_ACENTO)
        
        ttk.Button(frame_botones, text="Guardar Cambios", command=guardar_cambios).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=dialogo.destroy).grid(row=0, column=1, padx=5)
    
    def mostrar_ayuda():
        ayuda = tk.Toplevel(ventana)
        ayuda.title("Ayuda del Editor")
        ayuda.geometry("500x400")
        ayuda.transient(ventana)
        ayuda.grab_set()
        ayuda.configure(bg=COLOR_SECUNDARIO)
        
        tk.Label(ayuda, text="Ayuda del Editor de Textos", 
               font=fuente_titulo, bg=COLOR_SECUNDARIO, fg=COLOR_PRIMARIO).pack(pady=(15, 10))
        
        texto_ayuda = scrolledtext.ScrolledText(
            ayuda, wrap="word", font=fuente_normal,
            bg=COLOR_SECUNDARIO, fg=COLOR_TEXTO,
            width=50, height=15, padx=10, pady=10
        )
        texto_ayuda.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        info_ayuda = """
        FUNCIONES PRINCIPALES:
        
        1. Nuevo Mensaje:
           - Usa el botón 'Nuevo' para comenzar desde cero
           - Escribe tu contenido libremente
        
        2. Editar Existente:
           - Modifica título y contenido completo
        
        3. Eliminar Mensajes:
           - Elimina mensajes no deseados con confirmación
        
        4. Atajos:
           - Ctrl+N: Nuevo documento
           - Ctrl+S: Guardar
           - Ctrl+E: Editar mensaje
        
        Desarrollado por: J. Gabriel Calderón
        """
        
        texto_ayuda.insert(tk.END, info_ayuda)
        texto_ayuda.config(state="disabled")
        
        pie_frame = tk.Frame(ayuda, bg=COLOR_SECUNDARIO, height=30)
        pie_frame.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(pie_frame, text="© J. Gabriel Calderón", font=("Segoe UI", 8), bg=COLOR_SECUNDARIO, fg=COLOR_TEXTO).pack(side=tk.RIGHT, padx=15, pady=8)
        
        ttk.Button(ayuda, text="Cerrar", style='TButton', command=ayuda.destroy).pack(pady=(0, 15))
    
    botones_info_default = [
        ("Código Actualizado", "Entrégame el código actualizado en formato .txt..."),
        ("Análisis Exhaustivo", "Realiza un análisis exhaustivo del archivo..."),
        ("Instrucciones GUI", "Diseño de la Interfaz Gráfica de Usuario...")
    ]
    
    botones_creados = []
    
    def crear_botones_mensajes() -> None:
        for boton in botones_creados:
            boton.destroy()
        botones_creados.clear()
        
        mensajes = cargar_mensajes()
        botones_por_fila = 4
        
        for idx, (nombre, mensaje) in enumerate(mensajes.items()):
            fila = (idx // botones_por_fila) + 1
            columna = idx % botones_por_fila
            
            boton = ttk.Button(
                frame_botones_texto,
                text=nombre,
                width=20,
                style='TButton',
                command=lambda n=nombre, m=mensaje: actualizar_texto(n, m)
            )
            boton.grid(row=fila, column=columna, padx=5, pady=4)
            botones_creados.append(boton)
            ToolTip(boton, f"Cargar mensaje: {nombre}")
    
    crear_botones_mensajes()
    
    controles_frame = tk.Frame(frame_botones_adicionales, bg=COLOR_SECUNDARIO)
    controles_frame.pack(fill=tk.X, expand=True)
    
    botones_info = [
        ("Nuevo", nuevo_mensaje, "Crear nuevo mensaje desde cero"),
        ("Limpiar", limpiar_texto, "Borrar todo el contenido"),
        ("Copiar", copiar_texto, "Copiar al portapapeles"),
        ("Guardar", guardar_mensaje, "Guardar nuevo mensaje"),
        ("Editar", editar_mensaje, "Modificar mensaje existente"),
        ("Eliminar", eliminar_mensaje, "Borrar mensaje guardado"),
        ("Ayuda", mostrar_ayuda, "Mostrar ayuda de uso")
    ]
    
    for idx, (texto_btn, comando, tooltip) in enumerate(botones_info):
        boton = ttk.Button(controles_frame, text=texto_btn, style='TButton', command=comando)
        boton.grid(row=0, column=idx, padx=8, pady=5)
        ToolTip(boton, tooltip)
    
    # Configurar atajos de teclado
    ventana.bind("<Control-n>", lambda e: nuevo_mensaje())
    ventana.bind("<Control-s>", lambda e: guardar_mensaje())
    ventana.bind("<Control-e>", lambda e: editar_mensaje())
    
    pie_pagina = tk.Frame(ventana, bg=COLOR_BORDE, height=30)
    pie_pagina.grid(row=3, column=0, sticky="ew")
    tk.Label(pie_pagina, text="© J. Gabriel Calderón", font=("Segoe UI", 8), bg=COLOR_BORDE, fg=COLOR_TEXTO).pack(side=tk.RIGHT, padx=16, pady=5)
    
    def add_hover_effect():
        for boton in botones_creados:
            boton.bind("<Enter>", lambda e, b=boton: b.configure(cursor="hand2"))
            boton.bind("<Leave>", lambda e, b=boton: b.configure(cursor=""))
    
    ventana.after(500, add_hover_effect)
    
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'+{x}+{y}')
    
    ventana.mainloop()

if __name__ == "__main__":
    crear_interfaz()
