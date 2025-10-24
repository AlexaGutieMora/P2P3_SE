import json
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def base(archivo="hxhdatabase.json"):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def guardar(data, archivo="hxhdatabase.json"):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def encadenamiento(datos, conocimiento):
    posibles = []
    for personaje, caracteristicas in conocimiento.items():
        contradicho = False
        for p_respondida, valor_respondido in datos.items():
            if p_respondida in caracteristicas and caracteristicas[p_respondida] != valor_respondido:
                contradicho = True
                break
        if not contradicho:
            posibles.append(personaje)
    return posibles

class AkinatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HUNTERPEDIA")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.conocimiento = base()
        self.preguntas_total = set()
        for caracteristicas in self.conocimiento.values():
            self.preguntas_total.update(caracteristicas.keys())
        self.preguntas_total = list(self.preguntas_total)  
        self.datos = {}
        self.indice_pregunta = 0
        self.posibles = []

        self.bg_photo = None

        self.mostrar_portada()

    def poner_fondo(self, nombre_imagen):
        for w in self.root.winfo_children():
            w.destroy()
        try:
            img = Image.open(nombre_imagen)
            img = img.resize((700, 500), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(img)
            label = tk.Label(self.root, image=self.bg_photo)
            label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"No se pudo cargar {nombre_imagen}: {e}")
            self.root.configure(bg="black")

    def mostrar_portada(self):
        self.poner_fondo("fotoportada.png")
        intro = tk.Label(self.root, text="BIENVENIDO A LA HUNTERPEDIA \n Piensa en un personaje de Hunter x Hunter.\nYo sabré cuál es.",
                         font=("Courier New", 20, "bold"), bg="#00BFFF", fg="black", wraplength=600, justify="center")
        intro.place(relx=0.5, rely=0.25, anchor="center")

        btn_start = tk.Button(self.root, text="Comenzar", font=("Courier New", 18, "bold"),
                              bg="#8A2BE2", fg="white", width=12, command=self.iniciar_preguntas)
        btn_start.place(relx=0.5, rely=0.55, anchor="center")

    def iniciar_preguntas(self):
        self.datos = {}
        self.indice_pregunta = 0
        self.posibles = []

        if not self.preguntas_total:
            self.mostrar_aprender()
            return

        self.poner_fondo("fotod.png")
        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        self.poner_fondo("fotod.png")

        if self.indice_pregunta < len(self.preguntas_total):
            pregunta_actual = self.preguntas_total[self.indice_pregunta]

            frame_preg = tk.Frame(self.root, bg="#2874A6", padx=10, pady=20)
            frame_preg.place(relx=0.5, rely=0.25, anchor="center", width=620)

            label = tk.Label(frame_preg, text=f"¿Tu personaje {pregunta_actual}?",
                             font=("Courier New", 16, "bold"), bg="#2874A6", fg="white", wraplength=580)
            label.pack()

            frame_btn = tk.Frame(self.root, bg="", pady=10)
            frame_btn.place(relx=0.5, rely=0.55, anchor="center")

            btn_si = tk.Button(frame_btn, text="Sí", width=12, font=("Courier New", 12, "bold"),
                               bg="#1E8449", fg="white", command=lambda: self.responder("s"))
            btn_si.grid(row=0, column=0, padx=20)

            btn_no = tk.Button(frame_btn, text="No", width=12, font=("Courier New", 12, "bold"),
                               bg="#922B21", fg="white", command=lambda: self.responder("n"))
            btn_no.grid(row=0, column=1, padx=20)
        else:
            self.mostrar_aprender()

    def responder(self, resp):
        if self.indice_pregunta < len(self.preguntas_total):
            pregunta_actual = self.preguntas_total[self.indice_pregunta]
            self.datos[pregunta_actual] = True if resp == "s" else False
            self.posibles = encadenamiento(self.datos, self.conocimiento)

            if len(self.posibles) == 1:
                self.mostrar_adivinanza(self.posibles[0])
                return
            elif len(self.posibles) > 1:
                self.indice_pregunta += 1
                self.mostrar_pregunta()
                return
            else:
                if self.indice_pregunta + 1 < len(self.preguntas_total):
                    self.indice_pregunta += 1
                    self.mostrar_pregunta()
                else:
                    self.mostrar_aprender()
                return
        else:
            self.mostrar_aprender()

    def mostrar_adivinanza(self, personaje_predicho):
        for w in self.root.winfo_children():
            w.destroy()
        self.poner_fondo("foto_adivinanza.png")

        label = tk.Label(self.root, text=f"¡Ja! ¡Lo tengo! ¿Acaso estás pensando en {personaje_predicho}?",
                         font=("Courier New", 16, "bold"), bg="#FF1493", fg="white", wraplength=600, justify="center")
        label.place(relx=0.5, rely=0.25, anchor="center")

        frame_btn = tk.Frame(self.root, bg="#000000")
        frame_btn.place(relx=0.5, rely=0.55, anchor="center")

        btn_si = tk.Button(frame_btn, text="Sí", width=12, font=("Courier New", 12, "bold"),
                           bg="#1E8449", fg="white", command=lambda: self.mostrar_ganadora(personaje_predicho))
        btn_si.grid(row=0, column=0, padx=20)

        btn_no = tk.Button(frame_btn, text="No", width=12, font=("Courier New", 12, "bold"),
                           bg="#922B21", fg="white", command=self.mostrar_aprender)
        btn_no.grid(row=0, column=1, padx=20)

    def mostrar_ganadora(self, personaje_predicho):
        for w in self.root.winfo_children():
            w.destroy()
        self.poner_fondo("ganadora.png")

        label = tk.Label(self.root, text=f"Jo, jo, jo. Por supuesto, ¡soy increíble! Conozco muy bien a {personaje_predicho}",
                         font=("Courier New", 18, "bold"), bg="#32CD32", fg="white", wraplength=600, justify="center")
        label.place(relx=0.5, rely=0.5, anchor="center")

        self.root.after(2500, self.root.destroy)

    def mostrar_aprender(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.poner_fondo("aprender.png")

        header = tk.Label(self.root, text="Hmmm. Parece que puedo leer tu mente...",
                          font=("Courier New", 14, "bold"), bg="#9400D3", fg="white")
        header.place(relx=0.5, rely=0.12, anchor="center")

        lbl_name = tk.Label(self.root, text="Dime, ¿en qué personaje pensabas?", bg="#9400D3", fg="white")
        lbl_name.place(relx=0.5, rely=0.22, anchor="center")
        entry_name = tk.Entry(self.root, width=40)
        entry_name.place(relx=0.5, rely=0.27, anchor="center")

        lbl_feat = tk.Label(self.root, text="Ya veo... por favor, dime una característica única sobre tu personaje (que puedas responder con sí o no):", bg="#9400D3", fg="white")
        lbl_feat.place(relx=0.5, rely=0.34, anchor="center")
        entry_feat = tk.Entry(self.root, width=40)
        entry_feat.place(relx=0.5, rely=0.39, anchor="center")

        resp_var = tk.StringVar(value="s")
        rb_si = tk.Radiobutton(self.root, text="Sí", variable=resp_var, value="s", bg="#000000", fg="white")
        rb_si.place(relx=0.42, rely=0.46, anchor="center")
        rb_no = tk.Radiobutton(self.root, text="No", variable=resp_var, value="n", bg="#000000", fg="white")
        rb_no.place(relx=0.58, rely=0.46, anchor="center")

        def guardar_nuevo():
            nuevo_personaje = entry_name.get().strip()
            nueva_pregunta = entry_feat.get().strip().lower()
            resp = resp_var.get()

            if not nuevo_personaje or not nueva_pregunta:
                messagebox.showwarning("Hunterpedia", "Por favor, completa la información.")
                return

            nuevas_caracteristicas = {}
            for pregunta in self.preguntas_total:
                nuevas_caracteristicas[pregunta] = self.datos.get(pregunta, False)
            nuevas_caracteristicas[nueva_pregunta] = True if resp == "s" else False

            self.conocimiento[nuevo_personaje] = nuevas_caracteristicas
            guardar(self.conocimiento)

         #   messagebox.showinfo("Hunterpedia", f"Perfecto. Ahora sé todo sobre {nuevo_personaje}.")
         #   self.root.destroy()

        btn_save = tk.Button(self.root, text="Guardar", bg="#1E8449", fg="white",
                             font=("Courier New", 12, "bold"), command=guardar_nuevo)
        btn_save.place(relx=0.5, rely=0.58, anchor="center")

if __name__ == "__main__":
    root = tk.Tk()
    app = AkinatorGUI(root)
    root.mainloop()
