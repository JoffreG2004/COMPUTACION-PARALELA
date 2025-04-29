import subprocess
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Archivo CSV donde se guardarán los resultados
CSV_FILE = "resultados.csv"
# Carpeta donde se guardarán los informes
REPORTS_FOLDER = "informes"

def ejecutar_programa():
    # Ejecuta el programa main.exe
    result = subprocess.run(["main.exe"], capture_output=True, text=True)
    return result.stdout

def extraer_datos(salida):
    lines = salida.splitlines()
    tiempo_secuencial = float([l for l in lines if "Tiempo suma secuencial" in l][0].split(":")[1].split()[0])
    tiempo_simd = float([l for l in lines if "Tiempo suma SIMD" in l][0].split(":")[1].split()[0])
    aceleracion = float([l for l in lines if "Aceleracion SIMD" in l][0].split(":")[1].replace("x", ""))
    return tiempo_secuencial, tiempo_simd, aceleracion

def guardar_en_csv(tiempo_secuencial, tiempo_simd, aceleracion):
    archivo_existe = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not archivo_existe:
            writer.writerow(["Fecha", "Tiempo Secuencial", "Tiempo SIMD", "Aceleracion"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tiempo_secuencial, tiempo_simd, aceleracion])

def graficar():
    fechas, tiempos_secuenciales, tiempos_simd = [], [], []

    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            fechas.append(row["Fecha"])
            tiempos_secuenciales.append(float(row["Tiempo Secuencial"]))
            tiempos_simd.append(float(row["Tiempo SIMD"]))

    plt.figure(figsize=(10,6))
    plt.plot(fechas, tiempos_secuenciales, label="Tiempo Secuencial", linestyle='-', color='b')  # Línea azul
    plt.plot(fechas, tiempos_simd, label="Tiempo SIMD", linestyle='-', color='r')  # Línea roja
    plt.xticks(rotation=45)
    plt.xlabel("Fecha")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Comparación de Tiempos: Secuencial vs SIMD")
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.savefig("grafica_tiempos.png")
    plt.show()

def generar_informe(tiempo_secuencial, tiempo_simd, aceleracion):
    if not os.path.exists(REPORTS_FOLDER):
        os.makedirs(REPORTS_FOLDER)

    filename = f"{REPORTS_FOLDER}/informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, "w") as file:
        file.write(f"Informe de Ejecución\n")
        file.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Tiempo suma secuencial: {tiempo_secuencial:.5f} segundos\n")
        file.write(f"Tiempo suma SIMD (SSE): {tiempo_simd:.5f} segundos\n")
        file.write(f"Aceleración obtenida: {aceleracion:.2f}x\n")
        file.write("\nGráfico de Tiempos (Secuencial vs SIMD):\n")
        file.write(f"Se ha generado una imagen gráfica en: {os.path.abspath('grafica_tiempos.png')}\n")
    
    print(f"Informe guardado en: {filename}")

def main():
    salida = ejecutar_programa()
    print("Salida del programa:\n", salida)

    tiempo_secuencial, tiempo_simd, aceleracion = extraer_datos(salida)
    guardar_en_csv(tiempo_secuencial, tiempo_simd, aceleracion)
    graficar()
    generar_informe(tiempo_secuencial, tiempo_simd, aceleracion)
    print("Todo completado correctamente.")

if __name__ == "__main__":
    main()
