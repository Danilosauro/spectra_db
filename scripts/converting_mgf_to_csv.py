import csv
import os

def mgf_to_csv_folder(input_folder, output_csv):
    with open(output_csv, 'w', newline='') as csv_out:
        writer = csv.writer(csv_out)
        
        writer.writerow([
            "FILENAME", "PEPMASS", "CHARGE", "UNPD_ID", "MOLECULAR_FORMULA", "IONMODE",
            "EXACTMASS", "NAME", "SMILES", "INCHI", "INCHIAUX", "SCANS", "MZ", "INTENSITY"
        ])
        
        for filename in os.listdir(input_folder):
            if filename.endswith(".mgf"):
                filepath = os.path.join(input_folder, filename)
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
                            
                            mz, intensity = map(float, line.split())
                            mz_values.append(mz)
                            intensity_values.append(intensity)


mgf_to_csv_folder("./mgf_data", "source/output.csv")
