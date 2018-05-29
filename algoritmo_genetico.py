'''
* Marco Antonio Aguilar Licona
* Algoritmo Genético
* FI,UNAM
'''

import random

modelo_inversion = {
0:[0,0,0,0],
1:[0.28,0.25,0.15,0.20],
2:[0.45,0.41,0.25,0.33],
3:[0.65,0.55,0.40,0.42],
4:[0.78,0.65,0.50,0.48],
5:[0.90,0.75,0.62,0.53],
6:[1.02,0.80,0.73,0.56],
7:[1.13,0.85,0.82,0.58],
8:[1.23,0.88,0.90,0.60],
9:[1.32,0.90,0.96,0.60],
10:[1.38,0.90,1.00,0.60]
}

tam_cromosoma = 16
tam_poblacion = 50

num_beneficios = 4

num_sol_seleccionadas = 3

prob_mutacion = 0.01
prob_cruza = 0.8

num_generaciones = 20

def solucionCandidata(min, max):
    return[random.randint(min, max) for i in range(tam_cromosoma)]
  
def crearPoblacion():
    return [solucionCandidata(0,1) for i in range(tam_poblacion)]

def obtenerMillones(inversion):
    cadena_inversion = ""
    for i in range(len(inversion)):
        cadena_inversion += str(inversion[i])
    num_millones = int(cadena_inversion,2)
    return num_millones

def obtenerBeneficio(num_millones,num_beneficio):
    if num_millones > 10:
        num_millones = 0
    return modelo_inversion[num_millones][num_beneficio]

def obtenerAptitud(solucion_candidata):
    suma_inversion = 0
    suma_beneficios = 0
    for i in range(num_beneficios):
        indice_ini = i * num_beneficios
        indice_fin = (i + 1) * num_beneficios
        inversion = solucion_candidata[indice_ini:indice_fin]
        num_millones = obtenerMillones(inversion)
        suma_beneficios += obtenerBeneficio(num_millones,i)
        suma_inversion += num_millones
    v = abs(suma_inversion - 10)
    aptitud = suma_beneficios / (500 * v + 1)
    return aptitud

def ordernarAptitudes(poblacion):
    selecciones = [ (obtenerAptitud(i), i) for i in poblacion]
    selecciones = [i[1] for i in sorted(selecciones)]
    return selecciones

def seleccion(poblacion_ordenada):
    soluciones_seleccionadas =  poblacion_ordenada[(len(poblacion_ordenada)-num_sol_seleccionadas):]
    return soluciones_seleccionadas

def cruza(poblacion_ordenada,poblacion_seleccionada):
    poblacion_cruza = poblacion_ordenada
    div_cromosoma = int(tam_cromosoma/2)
    for i in range(len(poblacion_cruza)-num_sol_seleccionadas):
        for j in range(2):
            if random.random() <= prob_cruza:
                indice_ini = j * div_cromosoma
                indice_fin = (j + 1) * div_cromosoma
                padres = random.sample(poblacion_seleccionada, 2)
                padre_1 = padres[0][indice_ini:indice_fin]
                padre_2 = padres[1][indice_ini:indice_fin]

                poblacion_cruza[i][indice_ini:indice_ini+2] = padre_2[0:2]
                poblacion_cruza[i][indice_ini+2:indice_ini+6] = padre_1[2:6]
                poblacion_cruza[i][indice_ini+6:indice_ini+8] = padre_2[6:8]   
    return poblacion_cruza 

def mutacion(poblacion_cruza):
    poblacion_mutada = poblacion_cruza
    for i in range(len(poblacion_mutada)-num_sol_seleccionadas):
        if random.random() <= prob_mutacion:
            punto_mutacion = random.randint(0,tam_cromosoma-1)
            valor_mutacion = random.randint(0,1)
  
            while valor_mutacion == poblacion_mutada[i][punto_mutacion]:
                valor_mutacion = random.randint(0,1)

            poblacion_mutada[i][punto_mutacion] = valor_mutacion 
    return poblacion_mutada

def obtenerInversionFinal(poblacion_final):
    beneficio_total = 0
    solucion_inversion = ordernarAptitudes(poblacion_final)[tam_poblacion-1]
    print("------ Cadena Solución -----")
    print(solucion_inversion)
    print("")
    for i in range(num_beneficios):
        indice_ini = i * num_beneficios
        indice_fin = (i + 1) * num_beneficios
        inversion = solucion_inversion[indice_ini:indice_fin]
        num_millones = obtenerMillones(inversion)
        print("Inversión en Zona "+str(i+1)+": "+str(num_millones)+" millones")
        beneficio_total += obtenerBeneficio(num_millones,i)
    print("\nBeneficio Total: "+str(round(beneficio_total,2))+" millones")

poblacion_inicial = crearPoblacion()

for i in range(num_generaciones):
    poblacion_ordenada = ordernarAptitudes(poblacion_inicial)
    poblacion_seleccionada = seleccion(poblacion_ordenada)
    poblacion_cruza = cruza(poblacion_ordenada,poblacion_seleccionada)
    poblacion_final = mutacion(poblacion_cruza)

obtenerInversionFinal(poblacion_final)