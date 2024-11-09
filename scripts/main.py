import sqlite3
import tkinter as tk
import pandas as pd
from tkinter import messagebox, filedialog, ttk
import csv
from models import init_db

init_db()

def create_record():
    filename = entry_filename.get().strip() or None
    pepmass = float(entry_pepmass.get().strip()) if entry_pepmass.get().strip() else None
    charge = entry_charge.get().strip() or None
    unpd_id = entry_unpd_id.get().strip() or None
    molecular_formula = entry_molecular_formula.get().strip() or None
    ionmode = entry_ionmode.get().strip() or None
    exactmass = float(entry_exactmass.get().strip()) if entry_exactmass.get().strip() else None
    name = entry_name.get().strip() or None
    smiles = entry_smiles.get().strip() or None
    inchi = entry_inchi.get().strip() or None
    inchiaux = entry_inchiaux.get().strip() or None
    scans = int(entry_scans.get().strip()) if entry_scans.get().strip() else None
    mz = float(entry_mz.get().strip()) if entry_mz.get().strip() else None
    intensity = float(entry_intensity.get().strip()) if entry_intensity.get().strip() else None

    conn = sqlite3.connect('database/spectra_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_filename ON spectra (FILENAME)")
    cursor.execute('''
        INSERT INTO spectra (
            FILENAME, PEPMASS, CHARGE, UNPD_ID, MOLECULAR_FORMULA, IONMODE, EXACTMASS, NAME, SMILES, 
            INCHI, INCHIAUX, SCANS, MZ, INTENSITY
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (filename, pepmass, charge, unpd_id, molecular_formula, ionmode, exactmass, name, smiles, inchi, inchiaux, scans, mz, intensity))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Registro inserido com sucesso!")
    update_treeview()
    clear_entries()  

def clear_entries():
    for entry in entries.values():
        entry.delete(0, tk.END)  

def insert_csv_data():
    csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not csv_file_path:
        return

    conn = sqlite3.connect('database/spectra_db.sqlite')
    cursor = conn.cursor()

    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                cursor.execute('''
                    INSERT INTO spectra (
                        FILENAME, PEPMASS, CHARGE, UNPD_ID, MOLECULAR_FORMULA, IONMODE, EXACTMASS, NAME, 
                        SMILES, INCHI, INCHIAUX, SCANS, MZ, INTENSITY
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', row)
        conn.commit()
        messagebox.showinfo("Sucesso", "Dados do CSV inseridos com sucesso!")
        update_treeview()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        conn.close()

def insert_parquet_data():
    parquet_file_path = filedialog.askopenfilename(filetypes=[("Parquet files", "*.parquet")])
    if not parquet_file_path:
        return

    conn = sqlite3.connect('database/spectra_db.sqlite')
    cursor = conn.cursor()

    try:
        df = pd.read_parquet(parquet_file_path)
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO spectra (
                    FILENAME, PEPMASS, CHARGE, UNPD_ID, MOLECULAR_FORMULA, IONMODE, EXACTMASS, NAME, 
                    SMILES, INCHI, INCHIAUX, SCANS, MZ, INTENSITY
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['FILENAME'], row['PEPMASS'], row['CHARGE'], row['UNPD_ID'], row['MOLECULAR_FORMULA'],
                row['IONMODE'], row['EXACTMASS'], row['NAME'], row['SMILES'], row['INCHI'],
                row['INCHIAUX'], row['SCANS'], row['MZ'], row['INTENSITY']
            ))
        conn.commit()
        messagebox.showinfo("Sucesso", "Dados do Parquet inseridos com sucesso!")
        update_treeview()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        conn.close()

def update_treeview(records=None):
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect('database/spectra_db.sqlite')
    cursor = conn.cursor()
    if records is None:
        cursor.execute("SELECT * FROM spectra")
        records = cursor.fetchall()
    
    for record in records:
        tree.insert("", "end", values=record)
    
    conn.close()

def delete_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um registro para deletar.")
        return

    record_id = tree.item(selected_item)['values'][0]
    conn = sqlite3.connect('database/spectra_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM spectra WHERE id=?", (record_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Registro deletado!")
    update_treeview()

def search_record():
    filename = entry_search_filename.get().strip()
    if not filename:
        messagebox.showwarning("Atenção", "Por favor, insira um FILENAME para buscar.")
        return
    conn = sqlite3.connect('database/spectra_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spectra WHERE FILENAME=?", (filename,))
    records = cursor.fetchall()
    conn.close()
    if records:
        update_treeview(records)
    else:
        messagebox.showinfo("Resultado", "Nenhum registro encontrado.")

def refresh_treeview():
    update_treeview()

# tkinter interface
root = tk.Tk()
root.title("NP3 SPECTRA DB")
root.geometry("1200x600")

labels = ["ID", "FILENAME", "PEPMASS", "CHARGE", "UNPD_ID", "MOLECULAR_FORMULA", "IONMODE", "EXACTMASS", "NAME", 
          "SMILES", "INCHI", "INCHIAUX", "SCANS", "MZ", "INTENSITY"]

entries = {}
for i, label in enumerate(labels[1:]):
    tk.Label(root, text=f"{label}:").grid(row=i, column=0, sticky="w", padx=5, pady=5)
    entry = tk.Entry(root, width=30)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries[label] = entry

(entry_filename, entry_pepmass, entry_charge, entry_unpd_id, entry_molecular_formula, entry_ionmode, entry_exactmass,
 entry_name, entry_smiles, entry_inchi, entry_inchiaux, entry_scans, entry_mz, entry_intensity) = entries.values()

tk.Button(root, text="Criar Registro", command=create_record).grid(row=15, column=0, padx=5, pady=5)
tk.Button(root, text="Deletar Registro", command=delete_record).grid(row=15, column=1, padx=5, pady=5)
tk.Button(root, text="Carregar CSV", command=insert_csv_data).grid(row=15, column=2, padx=5, pady=5)
tk.Button(root, text="Carregar Parquet", command=insert_parquet_data).grid(row=15, column=3, padx=5, pady=5)
tk.Button(root, text="Buscar", command=search_record).grid(row=16, column=1, padx=5, pady=5)
tk.Button(root, text="Refresh", command=refresh_treeview).grid(row=16, column=3, padx=5, pady=5)

tk.Label(root, text="Buscar por FILENAME:").grid(row=16, column=0, sticky="w", padx=5, pady=5)
entry_search_filename = tk.Entry(root, width=30)
entry_search_filename.grid(row=16, column=1, padx=5, pady=5)
tk.Button(root, text="Buscar", command=search_record).grid(row=16, column=2, padx=5, pady=5)

frame = tk.Frame(root)
frame.grid(row=17, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

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

root.grid_rowconfigure(17, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

root.mainloop()
