# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 23:53:15 2025

@author: k
"""

import json
import os

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
        if all(datos.get(p, None) == v for p, v in caracteristicas.items()):
            posibles.append(personaje)
    return posibles

def aprender(conocimiento, preguntas_total):
    nuevo_personaje = input("Dime, ¿en qué personaje pensabas? ").strip()
    nuevas_caracteristicas = {}
    print(f"Ya veo... cuéntame más sobre {nuevo_personaje}")
    for pregunta in preguntas_total:
        respuesta = input(f"¿{nuevo_personaje} {pregunta}? (s/n): ").strip().lower()
        nuevas_caracteristicas[pregunta] = True if respuesta == "s" else False
    nueva_pregunta = input(f"Interesante... dime una característica que haga único a {nuevo_personaje}: ").strip().lower()
    resp = input(f"¿{nuevo_personaje} {nueva_pregunta}? (s/n): ").strip().lower()
    nuevas_caracteristicas[nueva_pregunta] = True if resp == "s" else False
    conocimiento[nuevo_personaje] = nuevas_caracteristicas
    guardar(conocimiento)

def akinator():  
    conocimiento = base()
    print("BIENVENIDO A LA HUNTERPEDIA.")
    print("Piensa en un personaje de la obra HunterxHunter, yo sabré cuál es.")
    preguntas_total = set()
    for caracteristicas in conocimiento.values():
        preguntas_total.update(caracteristicas.keys())

    datos = {}
    
    for pregunta in preguntas_total:
        respuesta = input(f"¿Tu personaje {pregunta}? (s/n): ").strip().lower()
        datos[pregunta] = True if respuesta == "s" else False
        posibles = encadenamiento(datos, conocimiento)
        if len(posibles) == 1:
            personaje_predicho = posibles[0]
            print(f"\n¡Ya lo tengo! Estás pensando en: {personaje_predicho} ")
            personaje_adivinado = input("¿He acertado? (s/n): ").strip().lower()
            if personaje_adivinado == "s":
                print("Por supuesto, soy el mejor.")
                return
            else:
                aprender(conocimiento, preguntas_total)
                return
        elif len(posibles) > 1:
            print(f"Todavía hay {len(posibles)} posibles coincidencias...")   
    print("\nHummm, creo que no puedo leer tu mente...")
    aprender(conocimiento, preguntas_total)

if __name__ == "__main__":
    akinator()
