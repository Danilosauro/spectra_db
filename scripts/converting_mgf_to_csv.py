import csv
import os

def mgf_to_csv_folder(input_folder, output_csv):
    try:
        mgf_files = [f for f in os.listdir(input_folder) if f.endswith(".mgf")]
        
        if not mgf_files:
            raise FileNotFoundError("Nenhum arquivo .mgf encontrado na pasta especificada.")
        
        
        with open(output_csv, 'w', newline='') as csv_out:
            writer = csv.writer(csv_out)
            
           
            writer.writerow([
                "FILENAME", "PEPMASS", "CHARGE", "UNPD_ID", "MOLECULAR_FORMULA", "IONMODE",
                "EXACTMASS", "NAME", "SMILES", "INCHI", "INCHIAUX", "SCANS", "MZ", "INTENSITY"
            ])
            
            
            for filename in mgf_files:
                filepath = os.path.join(input_folder, filename)
                
                try:
                    with open(filepath, 'r') as mgf:
                        data = {"FILENAME": filename}
                        mz_values = []
                        intensity_values = []

                        for line in mgf:
                            line = line.strip()
                            if line == "BEGIN IONS":
                                data.clear()
                                data["FILENAME"] = filename
                                mz_values.clear()
                                intensity_values.clear()
                            elif line == "END IONS":
                                for mz, intensity in zip(mz_values, intensity_values):
                                    writer.writerow([
                                        data.get("FILENAME", ""),
                                        data.get("PEPMASS", ""),
                                        data.get("CHARGE", ""),
                                        data.get("UNPD_ID", ""),
                                        data.get("MOLECULAR_FORMULA", ""),
                                        data.get("IONMODE", ""),
                                        data.get("EXACTMASS", ""),
                                        data.get("NAME", ""),
                                        data.get("SMILES", ""),
                                        data.get("INCHI", ""),
                                        data.get("INCHIAUX", ""),
                                        data.get("SCANS", ""),
                                        mz,
                                        intensity
                                    ])
                            elif "=" in line:
                                key, value = line.split("=", 1)
                                data[key] = value
                            else:
                                try:
                                    mz, intensity = map(float, line.split())
                                    mz_values.append(mz)
                                    intensity_values.append(intensity)
                                except ValueError:
                                    print(f"Erro ao converter valores MZ e INTENSITY em '{filename}': {line}")
                except IOError as e:
                    print(f"Erro ao ler o arquivo '{filename}': {e}")

        print(f"Arquivo CSV '{output_csv}' gerado com sucesso.")
    
    except FileNotFoundError as e:
        print(e)
    except IOError as e:
        print(f"Erro ao criar o arquivo CSV de saída '{output_csv}': {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

mgf_to_csv_folder("./insert_your_new_mgf_data", "source/mgf_output.csv")
