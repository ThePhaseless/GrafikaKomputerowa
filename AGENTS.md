# Grafika Komputerowa — Project Instructions

## Project Overview
University lab reports for the **Grafika Komputerowa i komunikacja z komputerem** (Computer Graphics) course at SGGW, Warsaw.

- **Student**: Jakub Orchowski, s223281
- **Language**: Python (3.14+), Jupyter notebooks
- **Package manager**: `uv`

## Repository Structure
```
lab{N}/                    # Lab folder
  lab{N}.pdf               # Assignment PDF (tasks)
  lecture_*.pdf             # Lecture slides (optional, theory reference)
  *.bmp                    # Test images for the lab
  Labolatorium {N}.ipynb   # Notebook solution (note: "Labolatorium" spelling)
  Labolatorium {N}.pdf     # Exported PDF
convert_to_pdf.py          # Helper: converts notebooks to PDF (runs cells by default)
pyproject.toml             # Dependencies
```

## How to Create a Lab

When the user says **"do lab X"**, **"create lab X"**, **"zrób lab X"**:

1. Read `lab{X}/lab{X}.pdf` — extract the assignment tasks using `pymupdf` (`fitz`)
2. List files in `lab{X}/` — identify test images (`.bmp`, `.jpg`, `.png`) and lecture PDFs
3. Optionally read lecture PDFs for theoretical context
4. Create `lab{X}/Labolatorium {X}.ipynb` following the exact notebook format below
5. After creation, run and convert to PDF:
   ```bash
   python convert_to_pdf.py "lab{X}/Labolatorium {X}.ipynb"
   ```

## Notebook Format (MANDATORY)

Every notebook must follow this exact cell structure:

### Cell 1 — Markdown
```markdown
**Jakub Orchowski, s223281**
```

### Cell 2 — Markdown
```markdown
# CEL ĆWICZENIA
<Topic description in Polish>
```

### Cell 3 — Code: Imports
```python
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
%matplotlib inline
```

### Cell 4 — Markdown
```markdown
# Zadania
```

### Per Task — Repeating Pattern
For each task (Zadanie N):

1. **Markdown**: `## Zadanie N.` + task description in Polish
2. **Markdown** (optional): `### <subtitle>` for sub-tasks (a, b, c)
3. **Code cell(s)**:
   - Functions with docstrings
   - `fig, axes = plt.subplots(...)` for visualization
   - `ax.set_title(...)`, `ax.axis('off')` for images
   - `plt.tight_layout()` + `plt.show()`
   - f-strings for numerical output
4. **Markdown**: `### Wnioski` — 2-4 line conclusions in Polish

## Code Style Rules

- **All text in Polish** (markdown, conclusions, plot titles)
- **Implement from scratch** using numpy — no scikit-image, OpenCV, or scipy unless the task explicitly permits it
- **Grayscale images**: `cmap='gray'`, `ax.axis('off')`
- **Side-by-side plots**: `plt.subplots(1, N, figsize=(width, 5))`
- **Normalize helper** for float images: `(x - x.min()) / (x.max() - x.min())`
- **Load images**: `np.array(Image.open('file.bmp').convert('L'))` (gray) or `np.array(Image.open('file.bmp'))` (color)
- **Conclusions (Wnioski)**: concise, factual, explain what happened and why
- **No unnecessary comments** — code should be self-explanatory
- **Vectorized numpy** operations preferred for performance
- **filter2d helper** for 2D convolution tasks (MATLAB `filter2` equivalent)

## Dependencies
Only use packages from `pyproject.toml`:
- numpy, matplotlib, Pillow, imageio, pandas, nbconvert, pandoc, pymupdf

## PDF Conversion
```bash
# Execute cells and convert to PDF (default):
python convert_to_pdf.py "lab{X}/Labolatorium {X}.ipynb"

# Convert without executing:
python convert_to_pdf.py --no-execute "lab{X}/Labolatorium {X}.ipynb"

# Convert to HTML instead:
python convert_to_pdf.py --format html "lab{X}/Labolatorium {X}.ipynb"
```
