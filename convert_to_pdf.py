"""Helper functions for converting Jupyter notebooks to PDF."""

import subprocess
import sys
from pathlib import Path


def notebook_to_pdf(
    notebook_path: str, output_path: str | None = None, execute: bool = True
) -> str:
    """Convert a Jupyter notebook to PDF using nbconvert.

    Args:
        notebook_path: Path to the .ipynb file.
        output_path: Optional output PDF path. Defaults to same name with .pdf extension.
        execute: If True, run all cells before converting (default: True).

    Returns:
        Path to the generated PDF file.
    """
    nb = Path(notebook_path).resolve()
    if not nb.exists():
        raise FileNotFoundError(f"Notebook not found: {nb}")

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
        raise RuntimeError(
            f"nbconvert failed (exit {result.returncode}):\n{result.stderr}"
        )

    pdf_path = out_dir / f"{out_name}.pdf"
    print(f"PDF saved to: {pdf_path}")
    return str(pdf_path)


def notebook_to_html(
    notebook_path: str, output_path: str | None = None, execute: bool = True
) -> str:
    """Convert a Jupyter notebook to HTML (fallback if LaTeX is not installed).

    Args:
        notebook_path: Path to the .ipynb file.
        output_path: Optional output HTML path.
        execute: If True, run all cells before converting (default: True).

    Returns:
        Path to the generated HTML file.
    """
    nb = Path(notebook_path).resolve()
    if not nb.exists():
        raise FileNotFoundError(f"Notebook not found: {nb}")

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
        "html",
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
        raise RuntimeError(
            f"nbconvert failed (exit {result.returncode}):\n{result.stderr}"
        )

    html_path = out_dir / f"{out_name}.html"
    print(f"HTML saved to: {html_path}")
    return str(html_path)


def convert_all_notebooks(
    root_dir: str = ".", fmt: str = "pdf", execute: bool = True
) -> list[str]:
    """Find and convert all notebooks in subdirectories to the given format.

    Args:
        root_dir: Root directory to search for notebooks.
        fmt: Output format ('pdf' or 'html').
        execute: If True, run all cells before converting.

    Returns:
        List of paths to generated files.
    """
    root = Path(root_dir).resolve()
    converter = notebook_to_pdf if fmt == "pdf" else notebook_to_html
    outputs = []

    for nb in sorted(root.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in str(nb):
            continue
        try:
            out = converter(str(nb), execute=execute)
            outputs.append(out)
        except RuntimeError as e:
            print(f"Failed to convert {nb}: {e}")

    return outputs


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert notebooks to PDF/HTML")
    parser.add_argument(
        "notebooks",
        nargs="*",
        help="Notebook paths. If empty, converts all notebooks in current directory tree.",
    )
    parser.add_argument(
        "--format",
        choices=["pdf", "html"],
        default="pdf",
        help="Output format (default: pdf)",
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
        converter = notebook_to_pdf if args.format == "pdf" else notebook_to_html
        for nb in args.notebooks:
            converter(nb, args.output, execute=execute)
    else:
        convert_all_notebooks(".", args.format, execute=execute)
