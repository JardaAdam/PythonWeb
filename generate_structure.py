import os
# terminal -> python generate_structure.py

def generate_structure(path='.', max_depth=2, ignore_dirs=None, output_file='struktura_projektu.txt'):
    """Generuje strukturu složek a souborů s omezením hloubky."""
    if ignore_dirs is None:
        ignore_dirs = ['__pycache__', 'venv', 'migrations', '.git']  # Přidán .git

    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            if level > max_depth:
                continue

            # Odstranit ignorované složky
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            indent = ' ' * 4 * level
            f.write(f'{indent}├── {os.path.basename(root)}\n')

            subindent = ' ' * 4 * (level + 1)
            for file in files:
                f.write(f'{subindent}├── {file}\n')


if __name__ == "__main__":
    generate_structure(path='.', max_depth=3, output_file='struktura_projektu.txt')
