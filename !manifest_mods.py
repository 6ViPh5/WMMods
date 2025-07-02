import os
import json
import hashlib

def create_manifest(mods_directory, output_file):
    """
    Recorre una carpeta de mods, calcula los hashes SHA256 y crea un manifest.json.
    """
    file_list = []
    print(f"Buscando mods en la carpeta: '{mods_directory}'...")

    # Recorrer todos los archivos en la carpeta de mods
    for filename in os.listdir(mods_directory):
        if filename.endswith(".jar"):
            file_path_local = os.path.join(mods_directory, filename)
            
            # Calcular el hash SHA256 del archivo
            sha256_hash = hashlib.sha256()
            with open(file_path_local, "rb") as f:
                # Leer el archivo en bloques para no consumir mucha memoria
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            # La ruta que irá en el manifiesto debe ser relativa (ej: "mods/modmenu.jar")
            path_in_manifest = f"mods/{filename}"

            # Añadir la info a nuestra lista
            file_list.append({
                "path": path_in_manifest,
                "sha256": sha256_hash.hexdigest()
            })
            print(f" - Procesado: {filename}")

    # Crear el diccionario final y guardarlo como JSON con formato legible
    manifest_data = {"files": file_list}
    with open(output_file, "w") as f:
        json.dump(manifest_data, f, indent=4)
    
    print(f"\n¡Listo! Manifest creado/actualizado en '{output_file}' con {len(file_list)} mods.")

# --- EJECUTAR EL SCRIPT ---
if __name__ == "__main__":
    mods_folder_name = "mods"
    output_filename = "manifest.json"
    
    if os.path.isdir(mods_folder_name):
        create_manifest(mods_folder_name, output_filename)
    else:
        print(f"Error: No se encontró la carpeta '{mods_folder_name}'.")
        print("Asegúrate de que este script esté en la misma carpeta que tu subcarpeta 'mods'.")
