import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

def run_conversion():
    try:
        script_path = os.path.join("scripts", "converting_mgf_to_csv.py")
        
        subprocess.run([sys.executable, script_path], check=True)
        messagebox.showinfo("Sucesso", "Conversão concluída e arquivo CSV gerado com sucesso.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Falha na conversão: {e}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

def open_database():
    try:
        script_path = os.path.join("scripts", "main.py")
        
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Falha ao abrir o banco de dados: {e}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

root = tk.Tk()
root.title("Tela Inicial - Conversão e Banco de Dados")

root.geometry("400x250") 
root.resizable(False, False)

title_label = tk.Label(root, text="Bem-vindo ao Sistema", font=("Helvetica", 14, "bold"))
title_label.pack(pady=20)

convert_button = tk.Button(root, text="Iniciar Conversão MGF para CSV", font=("Helvetica", 12), command=run_conversion)
convert_button.pack(pady=10)

database_button = tk.Button(root, text="Banco de Dados", font=("Helvetica", 12), command=open_database)
database_button.pack(pady=10)

instruction_label = tk.Label(root, text="Escolha uma das opções acima para continuar.", font=("Helvetica", 10))
instruction_label.pack(pady=10)

root.mainloop()
