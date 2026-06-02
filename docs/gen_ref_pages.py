"""Auto-generates an API reference page for every module found under python/."""
from pathlib import Path
import mkdocs_gen_files

SKIP_DIRS = ('vendor', 'vendors', 'extern', 'externals', 'third_party', 'venv', '.venv', 'site-packages', 'bin', 'scripts', 'startup', 'hooks', 'resources', 'tests', 'test')
SKIP_PREFIXES = ('tank_vendor', 'vendor_')

src = Path("python")
nav = mkdocs_gen_files.Nav()

for path in sorted(src.rglob("*.py")):
    # Skip vendored libraries and non-importable script directories
    if any(p in SKIP_DIRS or any(p.startswith(px) for px in SKIP_PREFIXES)
           for p in path.parts):
        continue

    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1].startswith("_"):
        continue

    if not parts:
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}\n")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
