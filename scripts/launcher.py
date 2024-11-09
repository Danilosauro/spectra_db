import subprocess
import sys
import os

def main():
    shell_script = os.path.join(os.path.dirname(__file__), "run_program.sh")
    
    if not os.path.exists(shell_script):
        print("Erro: o script shell 'run_program.sh' não foi encontrado.")
        sys.exit(1)
    
    try:
        subprocess.run(["chmod", "+x", shell_script], check=True)
        
        subprocess.run(["/bin/bash", shell_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script shell: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
