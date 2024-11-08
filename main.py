import sqlite3
import tkinter as tk
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

    conn = sqlite3.connect('spectra_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO spectra (
            FILENAME, PEPMASS, CHARGE, UNPD_ID, MOLECULAR_FORMULA, IONMODE, EXACTMASS, NAME, SMILES, 
            INCHI, INCHIAUX, SCANS, MZ, INTENSITY
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (filename, pepmass, charge, unpd_id, molecular_formula, ionmode, exactmass, name, smiles, inchi, inchiaux, scans, mz, intensity))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Registro inserido com sucesso!")
    update_listbox()

def insert_csv_data():
    csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not csv_file_path:
        return

    conn = sqlite3.connect('spectra_db.sqlite')
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
        update_listbox()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        conn.close()

def update_listbox(records=None):
    listbox.delete(0, tk.END)
    conn = sqlite3.connect('spectra_db.sqlite')
    cursor = conn.cursor()
    if records is None:
        cursor.execute("SELECT * FROM spectra")
        records = cursor.fetchall()
    for record in records:
        listbox.insert(tk.END, " - ".join([str(item) for item in record]))
    conn.close()

def delete_record():
    selected = listbox.get(tk.ACTIVE)
    if not selected:
        messagebox.showerror("Erro", "Selecione um registro para deletar.")
        return
    record_id = int(selected.split(" ")[0])
    conn = sqlite3.connect('spectra_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM spectra WHERE id=?", (record_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Registro deletado!")
    update_listbox()

def search_record():
    filename = entry_search_filename.get().strip()
    if not filename:
        messagebox.showwarning("Atenção", "Por favor, insira um FILENAME para buscar.")
        return
    conn = sqlite3.connect('spectra_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spectra WHERE FILENAME=?", (filename,))
    records = cursor.fetchall()
    conn.close()
    if records:
        update_listbox(records)
    else:
        messagebox.showinfo("Resultado", "Nenhum registro encontrado.")

def refresh_listbox():
    update_listbox()

# Interface tkinter
root = tk.Tk()
root.title("CRUD CHEM STRUCTURE")

labels = ["FILENAME", "PEPMASS", "CHARGE", "UNPD_ID", "MOLECULAR_FORMULA", "IONMODE", "EXACTMASS", "NAME", 
          "SMILES", "INCHI", "INCHIAUX", "SCANS", "MZ", "INTENSITY"]

entries = {}
for i, label in enumerate(labels):
    tk.Label(root, text=f"{label}:").grid(row=i, column=0, sticky="w", padx=5, pady=5)
    entry = tk.Entry(root, width=30)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries[label] = entry

(entry_filename, entry_pepmass, entry_charge, entry_unpd_id, entry_molecular_formula, entry_ionmode, entry_exactmass,
 entry_name, entry_smiles, entry_inchi, entry_inchiaux, entry_scans, entry_mz, entry_intensity) = entries.values()

tk.Button(root, text="Criar Registro", command=create_record).grid(row=15, column=0, padx=5, pady=5)
tk.Button(root, text="Deletar Registro", command=delete_record).grid(row=15, column=1, padx=5, pady=5)
tk.Button(root, text="Carregar CSV", command=insert_csv_data).grid(row=15, column=2, padx=5, pady=5)
tk.Button(root, text="Refresh", command=refresh_listbox).grid(row=15, column=3, padx=5, pady=5)

tk.Label(root, text="Buscar por FILENAME:").grid(row=16, column=0, sticky="w", padx=5, pady=5)
entry_search_filename = tk.Entry(root, width=30)
entry_search_filename.grid(row=16, column=1, padx=5, pady=5)
tk.Button(root, text="Buscar", command=search_record).grid(row=16, column=2, padx=5, pady=5)

frame = tk.Frame(root)
frame.grid(row=17, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

canvas = tk.Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

vertical_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=vertical_scrollbar.set)

horizontal_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
canvas.configure(xscrollcommand=horizontal_scrollbar.set)

listbox = tk.Listbox(scrollable_frame, width=100, height=20)
listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_frame_configure)

update_listbox()

root.grid_rowconfigure(17, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

root.mainloop()
