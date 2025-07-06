import os
import hashlib
import json

# Carpetas relativas esperadas
DIRS = {
    "mods": "mods",
    "resourcepacks": "resourcepacks",
    "shaderpacks": "shaderpacks",
    "config": "config"
}

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def sha1sum(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def get_files_with_hash(base_dir, hash_func, hash_key, extension):
    result = []
    if not os.path.isdir(base_dir):
        return result
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(extension):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, os.getcwd()).replace("\\", "/")
                result.append({
                    "path": rel_path,
                    hash_key: hash_func(full_path)
                })
    return result

def get_config_paths(base_dir):
    result = []
    if not os.path.isdir(base_dir):
        return result
    for root, _, files in os.walk(base_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, os.getcwd()).replace("\\", "/")
            result.append({"path": rel_path})
    return result

def main():
    manifest = {
        "files": {
            "mods": get_files_with_hash(DIRS["mods"], sha256sum, "sha256", ".jar"),
            "resourcepacks": get_files_with_hash(DIRS["resourcepacks"], sha1sum, "sha1", ".zip"),
            "shaderpacks": get_files_with_hash(DIRS["shaderpacks"], sha1sum, "sha1", ".zip"),
            "config": get_config_paths(DIRS["config"])
        }
    }

    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)
    print("✅ manifest.json generado correctamente.")

if __name__ == "__main__":
    main()
