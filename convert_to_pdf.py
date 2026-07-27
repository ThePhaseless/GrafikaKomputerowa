"""Helper functions for converting Jupyter notebooks to PDF."""

import re
import shutil
import subprocess
import sys
from pathlib import Path


def _install_missing_latex_packages(stderr: str) -> bool:
    """Auto-install missing LaTeX packages via tlmgr (for TinyTeX).

    Parses stderr for 'File `X.sty' not found' errors and installs them.

    Returns:
        True if any packages were installed, False otherwise.
    """
    missing = re.findall(r"File `([^']+\.sty)' not found", stderr)
    if not missing:
        return False

    # Map sty files to CTAN package names (common ones)
    sty_to_pkg = {
        "titling.sty": "titling",
        "longtable.sty": "longtable",
        "booktabs.sty": "booktabs",
        "fancyhdr.sty": "fancyhdr",
    }

    packages = []
    for sty in missing:
        pkg = sty_to_pkg.get(sty, sty.replace(".sty", ""))
        packages.append(pkg)

    if not packages:
        return False

    print(f"Auto-installing missing LaTeX packages: {packages}")
    result = subprocess.run(
        ["tlmgr", "install"] + packages,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"tlmgr install failed: {result.stderr}")
    return True


def notebook_to_pdf(
    notebook_path: str, output_path: str | None = None, execute: bool = True
) -> str:
    """Convert a Jupyter notebook to PDF using nbconvert.

    If using TinyTeX, automatically installs missing LaTeX packages.

    Args:
        notebook_path: Path to the .ipynb file.
        output_path: Optional output PDF path. Defaults to same name with .pdf extension.
        execute: If True, run all cells before converting (default: True).

    Returns:
        Path to the generated PDF file.
    """
    nb = Path(notebook_path).resolve()
    if not nb.exists():
        raise FileNotNotFoundError(f"Notebook not found: {nb}")

    if output_path:
        out_dir = Path(output_path).resolve().parent
        out_name = Path(output_path).stem
    else:
        out_dir = nb.parent
        out_name = nb.stem

    cmd = [
        sys.executable,
        "-m",
        "nbconvert",
        "--to",
        "pdf",
        "--output-dir",
        str(out_dir),
        "--output",
        out_name,
        str(nb),
    ]
    if execute:
        cmd.append("--execute")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=nb.parent)

    if result.returncode != 0:
        # Try auto-installing missing LaTeX packages if tlmgr is available
        if shutil.which("tlmgr") and _install_missing_latex_packages(result.stderr):
            # Retry once after installing packages
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=nb.parent)
            if result.returncode == 0:
                pdf_path = out_dir / f"{out_name}.pdf"
                print(f"PDF saved to: {pdf_path}")
                return str(pdf_path)

        raise RuntimeError(
            f"nbconvert failed (exit {result.returncode}):\n{result.stderr}"
        )

    pdf_path = out_dir / f"{out_name}.pdf"
    print(f"PDF saved to: {pdf_path}")
    return str(pdf_path)


def convert_all_notebooks(root_dir: str = ".", execute: bool = True) -> list[str]:
    """Find and convert all notebooks in subdirectories to PDF.

    Args:
        root_dir: Root directory to search for notebooks.
        execute: If True, run all cells before converting.

    Returns:
        List of paths to generated PDF files.
    """
    root = Path(root_dir).resolve()
    outputs = []

    for nb in sorted(root.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in str(nb):
            continue
        try:
            out = notebook_to_pdf(str(nb), execute=execute)
            outputs.append(out)
        except RuntimeError as e:
            print(f"Failed to convert {nb}: {e}")

    return outputs


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert notebooks to PDF")
    parser.add_argument(
        "notebooks",
        nargs="*",
        help="Notebook paths. If empty, converts all notebooks in current directory tree.",
    )
    parser.add_argument("-o", "--output", help="Output path (only for single notebook)")
    parser.add_argument(
        "--no-execute",
        action="store_true",
        help="Skip executing cells before conversion",
    )

    args = parser.parse_args()
    execute = not args.no_execute

    if args.notebooks:
        for nb in args.notebooks:
            notebook_to_pdf(nb, args.output, execute=execute)
    else:
        convert_all_notebooks(".", execute=execute)
