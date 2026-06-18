# Lateral Repairs — MULTIline Technical Data Sheets (2026)

Redesigned A4 technical data sheets for the 2026 MULTIline liner range,
styled to match the supplied reference (`assets/REFERENCE_FORCE_TDS.pdf`)
using the Lateral Repairs 2026 logo and brand pink (`#E6007E`).

All values are taken **verbatim** from the source Word documents — only the
layout/design was changed. An automated check confirms every product name,
code, undersize and physical value from the Word files appears in each PDF.

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
python3 build.py      # regenerates all PDFs in out/
```

- `parse_tds.py` — parses the Word-doc tables (`assets/source_tables.json`)
  into a clean per-product model. No values are altered.
- `build.py` — renders each product to a branded A4 PDF with WeasyPrint
  (repeating header/footer, page numbers, brand colours).

## Notes

- The Word documents contain product / material / supply / general data plus
  physical properties and handling parameters. They do **not** contain the
  page-3 inversion/curing-pressure table seen in the old FORCE reference PDF,
  so that table is not reproduced (no source data for the new range).
- Fonts fall back to DejaVu where Space Grotesk / Inter are unavailable; the
  layout and colours are unaffected.
