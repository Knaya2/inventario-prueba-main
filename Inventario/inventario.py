import json
import os

# Nombre del archivo donde se guardará el inventario
ARCHIVO = "inventario.json"

# Cargar inventario si existe, si no crear uno vacío
if os.path.exists(ARCHIVO):
    with open(ARCHIVO, "r") as f:
        inventario = json.load(f)
else:
    inventario = {}

def guardar_inventario():
    with open(ARCHIVO, "w") as f:
        json.dump(inventario, f, indent=4)

def agregar_producto():
    nombre = input("Nombre del producto: ").strip()
    if nombre in inventario:
        print("Ese producto ya existe. Se actualizará la cantidad.")
        inventario[nombre]["cantidad"] += int(input("Cantidad a agregar: "))
    else:
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
        inventario[nombre] = {"cantidad": cantidad, "precio": precio}
    guardar_inventario()
    print("✅ Producto agregado/actualizado con éxito.")

def eliminar_producto():
    nombre = input("Nombre del producto a eliminar: ").strip()
    if nombre in inventario:
        del inventario[nombre]
        guardar_inventario()
        print("🗑️ Producto eliminado.")
    else:
        print("❌ Ese producto no existe en el inventario.")

def mostrar_inventario():
    if not inventario:
        print("📦 El inventario está vacío.")
    else:
        print("\n--- INVENTARIO ---")
        for producto, datos in inventario.items():
            print(f"{producto} - Cantidad: {datos['cantidad']}, Precio: {datos['precio']}")
        print("------------------\n")

# Menú principal
while True:
    print("\n1. Agregar producto")
    print("2. Eliminar producto")
    print("3. Mostrar inventario")
    print("4. Salir")
    opcion = input("Elige una opción: ")

    if opcion == "1":
        agregar_producto()
    elif opcion == "2":
        eliminar_producto()
    elif opcion == "3":
        mostrar_inventario()
    elif opcion == "4":
        print("👋 Saliendo...")
        break
    else:
        print("❌ Opción inválida.")
