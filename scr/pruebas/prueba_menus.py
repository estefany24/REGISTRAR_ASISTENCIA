import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Gestión")
root.geometry("800x600")

# Crear el contenedor de pestañas
tabControl = ttk.Notebook(root)

# Crear las pestañas
tab_dashboard = ttk.Frame(tabControl)
tab_almacen = ttk.Frame(tabControl)
tab_ventas = ttk.Frame(tabControl)
tab_compras = ttk.Frame(tabControl)
tab_clientes = ttk.Frame(tabControl)
tab_reportes = ttk.Frame(tabControl)
tab_proveedores = ttk.Frame(tabControl)

# Agregar las pestañas al contenedor
tabControl.add(tab_dashboard, text="DASHBOARD")
tabControl.add(tab_almacen, text="ALMACEN")
tabControl.add(tab_ventas, text="VENTAS")
tabControl.add(tab_compras, text="COMPRAS")
tabControl.add(tab_clientes, text="CLIENTES")
tabControl.add(tab_reportes, text="REPORTES")
tabControl.add(tab_proveedores, text="PROVEEDORES")

# Posicionar el contenedor de pestañas
tabControl.pack(expand=1, fill="both")

# Crear un Treeview en la pestaña "ALMACEN"
columns = ("#0", "codigo", "producto", "precio_compra", "precio_venta", "stock", "proveedor", "categoria")

tree = ttk.Treeview(tab_almacen, columns=columns, show='headings')

# Definir encabezados
for col in columns:
    tree.heading(col, text=col)

# Insertar datos de ejemplo
data = [
    ("1", "camisa", "10", "15", "100", "Proveedor1", "Ropa"),
    ("2", "pantalon", "20", "30", "150", "Proveedor2", "Ropa"),
    ("3", "zapatos", "25", "40", "80", "Proveedor3", "Calzado"),
    # Agrega más filas de datos según sea necesario
]

for row in data:
    tree.insert("", tk.END, values=row)

# Empaquetar el Treeview
tree.pack(expand=True, fill='both')

# Crear los campos de entrada y los botones en la pestaña "ALMACEN"
frame = tk.Frame(tab_almacen)
frame.pack(pady=10)

# Etiquetas y entradas
labels = ["Productos:", "Precio Compra:", "Precio Venta:", "Stock:", "Proveedor:", "Categoria:"]
entries = []

for i, label in enumerate(labels):
    tk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5)
    entry = tk.Entry(frame)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

# Botones
buttons = ["ELIMINAR", "VACIAR CAMPOS", "ACTUALIZAR", "AGREGAR"]
for i, button in enumerate(buttons):
    tk.Button(frame, text=button).grid(row=i, column=2, padx=5, pady=5)

root.mainloop()
