import os
# terminal -> python generate_structure_md.py

def generate_structure(path='.', max_depth=3, ignore_dirs=None, output_file='README.md'):
    """Generuje strukturu složek a souborů ve formátu Markdown."""
    if ignore_dirs is None:
        ignore_dirs = ['__pycache__', 'venv', 'migrations', '.git', 'node_modules', 'build', 'dist']

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('# 📂 Projektová struktura\n\n')
        f.write('```\n')  # Markdown code block
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            if level > max_depth:
                continue

            # Odstranit ignorované složky
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            indent = ' ' * 4 * level
            f.write(f'{indent}- {os.path.basename(root)}/\n')

            subindent = ' ' * 4 * (level + 1)
            for file in files:
                f.write(f'{subindent}- {file}\n')

        f.write('```\n')


if __name__ == "__main__":
    generate_structure(path='.', max_depth=3, output_file='README.md')
    #generate_structure(path='.', max_depth=3, output_file='project_structure.md')