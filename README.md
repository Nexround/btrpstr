
# btrpstr (minimalistic LaTeX+TikZ poster class)

The `btrpstr` class was created as a simple support for efficiently creating
the #betterposter-style posters in LaTeX. See https://osf.io/ef53g/ for Mike
Morrison's non-TeX templates.

This repository contains 2 very rough templates, `posterh` (the "original"
horizontal betterposter) and `posterv` (the "vertical" format of the same,
better compatible with the way of postering at the conferences).

Prebuilt PDFs can be seen in [build/](build/).

| Horizontal | Vertical |
|------------|----------|
| ![Horizontal version](build/posterh.png) | ![Vertical version](build/posterv.png) |

### How-To

Take the poster template, compile with double `lualatex` (or switch to the
traditional font system and compile with double `pdflatex`), modify for your
needs, enjoy.

### Reference

This tries to very minimalistically mimic the behavior of `baposter` template
that gives a straightforward way to organize poster contents in "boxes" that
all belong to "columns", which makes the poster look seriously organized.

This class defines the following:

- `poster` environment that converts the current page to a poster (optionally
  it modifies the font sizes, turns off page numbering, sets up geometry if
  asked, and starts a `tikzpicture` environment. You can draw normal TikZ boxes
  and paths inside. Notably, `baposter` uses fullpage scaling to achieve "large
  fonts", we just scale fonts. If you need fullpage scaling (e.g. transparently
  scale up tikz arrows etc), use `pgfpages` to resize a smaller poster.

- `posterbox` and `headerbox` environments to create simple boxes with text
  nicely aligned in _columns_

- `\newpostercol` and `\splitpostercol` to define new columns, and, optionally,
  split them into multiple sub-columns

- several other helpers, mainly some stuff for simplified background drawing.

For now, see the comments in `posterv.tex` for a more precise reference. Some
study of the Tikz manual is highly recommended (reading that particular manual
is highly recommended in any case, even if you're not after posters).

### Future

Everything is likely going to change a lot (see the comments with TODOs in the
class file).

### RACE Paper Poster

The customized poster uses the A0 portrait option of `btrpstr` (841 x 1189 mm).
`posterv.tex` is the entry point, and `race_poster.tex` contains the editable
poster content. The original vertical example is preserved in
`templates/posterv_example.tex`.

Build the PDF and PNG preview with the installed XeLaTeX and Poppler tools:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_poster.ps1
```

The deliverables are `output/pdf/RACE_poster_A0_portrait.pdf` and
`output/pdf/RACE_poster_A0_portrait.png`. All charts remain vector artwork in
the PDF. The code QR links to the repository named in the paper.

`assets/race/reported_data.json` records chart values and their source tables
in the supplied arXiv v2 PDF. Accuracy results, suppression budgets, and scoring
costs retain the paper's experimental settings. The comprehension correctness
scores apply to the subset of outputs still containing comprehensions. The
approximately 230-fold reduction compares extra scoring FLOPs; it is not a
wall-clock speedup for the full RACE pipeline.

To regenerate the chart assets, run `python scripts/prepare_assets.py` with
Python 3 and XeLaTeX available. This script uses only Python's standard library.
The original paper path in the data manifest is needed to re-extract Figure 1;
the included figure PDF is sufficient for normal poster builds.

### License

This repository and all work in it is relased to public domain.
