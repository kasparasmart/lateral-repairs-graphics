# Lateral Repairs — MULTIline Technical Data Sheets (2026)

A4 technical data sheets for the 2026 MULTIline liner range, built to match
the supplied reference (`assets/REFERENCE_FORCE_TDS.pdf`) exactly:

- **Letterhead** (logo, magenta "TECHNICAL DATA SHEET" block, grey title bar,
  magenta contact footer, watermark) is reused **pixel-for-pixel** from the
  reference PDF, so colours, logo and contact info are identical. Only the
  per-product title in the grey bar is re-rendered (Montserrat, matching the
  reference's font).
- **Body** is set in Times New Roman (Liberation Serif), black values, bold
  section headers — matching the reference.
- **Page numbers** are white serif on the magenta footer ("Page X of Y").

All values come **verbatim** from the source Word documents — only the layout
was changed. An automated check confirms every product name, code, undersize
and physical value from the Word files appears in each PDF.

## 2026 renaming

| 2026 name        | Previous name |
|------------------|---------------|
| MULTIline PRO    | NanoTech      |
| MULTIline FLEX   | DrainPlus     |
| MULTIline FORCE  | Mega          |
| MULTIline CORE   | Polynex       |

## Output (`out/`)

| File | Product | Was |
|------|---------|-----|
| `LR_MULTIline_PRO_40mm.pdf` | MULTIline PRO 4.0 mm | Nanotech HD |
| `LR_MULTIline_PRO_45mm.pdf` | MULTIline PRO 4.5 mm | Nanotech 4.5 |
| `LR_MULTIline_FLEX.pdf`     | MULTIline FLEX | DrainPlus |
| `LR_MULTIline_CORE.pdf`     | MULTIline CORE | Polynex |
| `LR_MULTIline_FORCE.pdf`    | MULTIline FORCE | Mega |
| `LR_MULTIline_FORCE_RF.pdf` | MULTIline FORCE RF | Mega RF |
| `LR_MULTIline_FORCE_UV.pdf` | MULTIline FORCE UV | Mega UV |
| `LR_MULTIline_ALL_datasheets.pdf` | All seven combined | |
| `_preview_all.png` | Contact-sheet preview | |

## Rebuilding

```bash
cd datasheets
pip install python-docx weasyprint pypdf pillow
python3 make_backgrounds.py   # builds per-product letterheads in assets/bg/
python3 build.py              # renders all PDFs in out/
```

- `parse_tds.py` — parses the Word-doc tables (`assets/source_tables.json`)
  into a clean per-product model. No values are altered.
- `make_backgrounds.py` — reuses `assets/letterhead.png` (extracted from the
  reference PDF) and re-renders each product title with Montserrat
  (`assets/fonts/`) into `assets/bg/<slug>.png`.
- `build.py` — renders each product to PDF with WeasyPrint, using the
  letterhead as a full-page background and a Times New Roman body.

## Notes

- The Word documents contain product / material / supply / general data plus
  physical properties and handling parameters (two pages). They do **not**
  contain the page-3 inversion/curing-pressure table from the old FORCE
  reference, so that page is not reproduced (no source data for the new range).
- Fonts: body uses Liberation Serif (metric-identical to Times New Roman);
  titles use Montserrat (the reference's header font).
