import psycopg2
import tkinter as tk
import pandas as pd
from tkinter import messagebox, filedialog, ttk
import csv
from models import init_db

init_db()

current_table = "spectra"

def get_connection():
    return psycopg2.connect(
        dbname="spectra_db",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )

def toggle_table_view():
    global current_table
    current_table = "UNPD" if current_table == "spectra" else "spectra"
    update_treeview(current_table)
    messagebox.showinfo("Visualização Alterada", f"Visualizando dados da tabela {current_table}")

def search_records():
    query = entry_search.get().strip()
    if not query:
        messagebox.showwarning("Busca Vazia", "Por favor, insira um termo de busca.")
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {current_table} WHERE FILENAME ILIKE %s", (f"%{query}%",))
    records = cursor.fetchall()
    conn.close()
    update_treeview(current_table, records)

def refresh_treeview():
    update_treeview()

def create_record():
    data = {key: entry.get().strip() or None for key, entry in entries.items()}
    data["PEPMASS"] = float(data["PEPMASS"]) if data["PEPMASS"] else None
    data["EXACTMASS"] = float(data["EXACTMASS"]) if data["EXACTMASS"] else None
    data["SCANS"] = int(data["SCANS"]) if data["SCANS"] else None
    data["MZ"] = float(data["MZ"]) if data["MZ"] else None
    data["INTENSITY"] = float(data["INTENSITY"]) if data["INTENSITY"] else None

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_filename ON spectra (FILENAME)")
    cursor.execute(f'''
        INSERT INTO {current_table} (FILENAME, PEPMASS, CHARGE, UNPD_ID, MOLECULAR_FORMULA, IONMODE, EXACTMASS, NAME, 
        SMILES, INCHI, INCHIAUX, SCANS, MZ, INTENSITY) 
        VALUES (%(FILENAME)s, %(PEPMASS)s, %(CHARGE)s, %(UNPD_ID)s, %(MOLECULAR_FORMULA)s, %(IONMODE)s, %(EXACTMASS)s, 
        %(NAME)s, %(SMILES)s, %(INCHI)s, %(INCHIAUX)s, %(SCANS)s, %(MZ)s, %(INTENSITY)s)
    ''', data)
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Registro inserido com sucesso!")
    update_treeview(current_table)
    clear_entries()

def insert_csv_data():
    csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not csv_file_path:
        return

    conn = get_connection()
    cursor = conn.cursor()

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            cursor.execute(f'''
                INSERT INTO {current_table} (FILENAME, PEPMASS, CHARGE, UNPD_ID, MOLECULAR_FORMULA, IONMODE, EXACTMASS, 
                NAME, SMILES, INCHI, INCHIAUX, SCANS, MZ, INTENSITY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s)
            ''', row)
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Dados do CSV inseridos com sucesso!")
    update_treeview(current_table)

def insert_parquet_data():
    parquet_file_path = filedialog.askopenfilename(filetypes=[("Parquet files", "*.parquet")])
    if not parquet_file_path:
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        df = pd.read_parquet(parquet_file_path)
        for _, row in df.iterrows():
            cursor.execute(f'''
                INSERT INTO UNPD (
                    FILENAME, PEPMASS, CHARGE, UNPD_ID, MOLECULAR_FORMULA, IONMODE, EXACTMASS, NAME, 
                    SMILES, INCHI, INCHIAUX, SCANS, MZ, INTENSITY
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                row['FILENAME'], row['PEPMASS'], row['CHARGE'], row['UNPD_ID'], row['MOLECULAR_FORMULA'],
                row['IONMODE'], row['EXACTMASS'], row['NAME'], row['SMILES'], row['INCHI'],
                row['INCHIAUX'], row['SCANS'], row['MZ'], row['INTENSITY']
            ))
        conn.commit()
        messagebox.showinfo("Sucesso", "Dados do Parquet inseridos com sucesso!")
        update_treeview("UNPD")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        conn.close()

def delete_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um registro para deletar.")
        return

    record_id = tree.item(selected_item)['values'][0]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {current_table} WHERE id=%s", (record_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Registro deletado!")
    update_treeview(current_table)

def update_treeview(table="spectra", records=None):
    for row in tree.get_children():
        tree.delete(row)
    
    conn = get_connection()
    cursor = conn.cursor()
    if records is None:
        cursor.execute(f"SELECT * FROM {table}")
        records = cursor.fetchall()
    
    for record in records:
        tree.insert("", "end", values=record)
    
    conn.close()

# Interface Tkinter
root = tk.Tk()
root.title("NP3 SPECTRA DB")
root.geometry("1200x650")

labels = ["ID", "FILENAME", "PEPMASS", "CHARGE", "UNPD_ID", "MOLECULAR_FORMULA", "IONMODE", "EXACTMASS", "NAME", 
          "SMILES", "INCHI", "INCHIAUX", "SCANS", "MZ", "INTENSITY"]

entries = {}
for i, label in enumerate(labels[1:]):
    tk.Label(root, text=f"{label}:").grid(row=i, column=0, sticky="w", padx=5, pady=5)
    entry = tk.Entry(root, width=30)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries[label] = entry

tk.Label(root, text="Buscar FILENAME:").grid(row=0, column=3, sticky="w", padx=5, pady=5)
entry_search = tk.Entry(root, width=30)
entry_search.grid(row=0, column=4, padx=5, pady=5)
tk.Button(root, text="Buscar", command=search_records).grid(row=0, column=5, padx=5, pady=5)

button_frame = tk.Frame(root)
button_frame.grid(row=15, column=0, columnspan=6, pady=10, sticky="ew")

tk.Button(button_frame, text="Criar Registro", command=create_record).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Deletar Registro", command=delete_record).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Carregar CSV", command=insert_csv_data).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Carregar dados UNPD", command=insert_parquet_data).grid(row=0, column=3, padx=5, pady=5)
tk.Button(button_frame, text="Alternar Tabela", command=toggle_table_view).grid(row=0, column=4, padx=5, pady=5)
tk.Button(button_frame, text="Atualizar", command=refresh_treeview).grid(row=0, column=5, padx=5, pady=5)


frame = tk.Frame(root)
frame.grid(row=16, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

tree = ttk.Treeview(frame, columns=labels, show="headings")
for label in labels:
    tree.heading(label, text=label)
    tree.column(label, width=100, anchor="center")
tree.pack(fill=tk.BOTH, expand=True)

scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar_y.set)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
tree.configure(xscroll=scrollbar_x.set)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

update_treeview()

root.grid_rowconfigure(16, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
