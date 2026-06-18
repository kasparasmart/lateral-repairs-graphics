"""Render MULTIline technical data sheets as PDFs in the Lateral Repairs
brand style, matching the supplied FORCE TDS reference exactly:

  * per-product letterhead background (logo, TECHNICAL DATA SHEET block,
    grey title bar, magenta contact footer, watermark) — see make_backgrounds.py
  * Times New Roman body (Liberation Serif), black values
  * white serif page numbers on the magenta footer

Data is taken verbatim from the Word documents via parse_tds.py."""
import datetime
import html
import os

from weasyprint import HTML

from parse_tds import load_all

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
BG_DIR = os.path.join(ASSETS, "bg")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

# geometry of the letterhead (mm on A4): grey bar ends 61.3mm, footer 272.5mm
TOP_MM = 63
BOT_MM = 27
SIDE_MM = 15

VERSION = "V2026.1"
FIRST_ISSUE = "2021.01.21"
VIEWED = "2026.05.01"


def esc(s):
    return html.escape(s).replace("\n", "<br>")


def css(slug):
    bg = os.path.join(BG_DIR, f"{slug}.png").replace("\\", "/")
    return f"""
<style>
  @font-face {{ font-family: 'TNR'; src: url('file://{ASSETS}/fonts/LiberationSerif-Regular.ttf'); }}
  @page {{
    size: A4;
    margin: {TOP_MM}mm {SIDE_MM}mm {BOT_MM}mm {SIDE_MM}mm;
    @bottom-right {{
      content: "Page " counter(page) " of " counter(pages);
      color: #fff; font-family: 'Liberation Serif','Times New Roman',serif;
      font-size: 11pt; margin-right: 9mm; margin-bottom: 9mm;
    }}
  }}
  * {{ box-sizing: border-box; }}
  html {{ font-family: 'Liberation Serif','Times New Roman',serif;
    color: #000; font-size: 11pt; line-height: 1.22; }}
  body {{ margin: 0; }}
  .bgfull {{ position: fixed; top: -{TOP_MM}mm; left: -{SIDE_MM}mm;
    width: 210mm; height: 297mm; z-index: -1; }}

  table.blk {{ width: 100%; border-collapse: collapse; margin-bottom: 5mm;
    border: 1px solid #000; break-inside: avoid; }}
  table.blk td {{ border: 1px solid #000; padding: 3px 8px; vertical-align: top; }}
  td.sec {{ font-weight: bold; }}
  table.product td {{ background: #f2f2f2; }}
  table.product td.k {{ font-weight: bold; }}
  td.k {{ width: 30%; }}
  table.blk.wide td.k {{ width: 30%; }}
  td.cond {{ width: 30%; }}
  td.unit {{ width: 12%; }}
  td.val {{ width: 28%; }}

  .disc {{ border: 1px solid #000; padding: 5px 8px; margin-bottom: 4mm;
    text-align: justify; break-inside: avoid; }}
  .notes {{ font-size: 10pt; }}
  .notes div {{ margin-bottom: 1mm; }}
</style>
"""


def two_col(label, value, bold=False):
    return f'<tr><td class="k">{esc(label)}</td><td class="v">{esc(value)}</td></tr>'


def render_product(p):
    supply_rows = "".join(two_col(k, v) for k, v in p["supply"])
    general_rows = "".join(two_col(k, v) for k, v in p["general"])
    seam_label = "Used seam (stitched)<br>and seam sealing"
    for i, s in enumerate(p["seam"]):
        general_rows += (f'<tr><td class="k">{seam_label if i == 0 else "&nbsp;"}</td>'
                         f'<td class="v">{esc(s)}</td></tr>')

    phys_rows = ""
    for prop, cond, unit, val in p["physical"]:
        phys_rows += (f'<tr><td class="k">{esc(prop)}</td>'
                      f'<td class="cond">{esc(cond)}</td>'
                      f'<td class="unit">{esc(unit)}</td>'
                      f'<td class="val">{esc(val)}</td></tr>')

    hand_rows = ""
    for prop, cond, unit, val in p["handling"]:
        hand_rows += (f'<tr><td class="k">{esc(prop)}</td>'
                      f'<td class="v" colspan="3">{esc(cond)}</td></tr>')

    notes_html = ""
    if p["notes"]:
        notes_html = '<div class="notes">' + "".join(
            f"<div>{esc(n)}</div>" for n in p["notes"]) + "</div>"

    disclaimer = p["disclaimer"]

    bg = os.path.join(BG_DIR, f"{p['slug']}.png").replace("\\", "/")
    return css(p["slug"]) + f"""
  <img class="bgfull" src="file://{bg}" alt="">
  <main>
    <table class="blk product">
      <tr><td class="k">Product name</td><td class="v">{esc(p['product_name'])}</td></tr>
      <tr><td class="k">Product code</td><td class="v">{esc(p['product_code'])}</td></tr>
    </table>

    <table class="blk">
      <tr><td class="sec" colspan="2">Material composition</td></tr>
      <tr><td>&nbsp;</td><td>{esc(p['material'])}</td></tr>
    </table>

    <table class="blk">
      <tr><td class="sec" colspan="2">Supply data</td></tr>
      {supply_rows}
    </table>

    <table class="blk">
      <tr><td class="sec" colspan="2">General data</td></tr>
      {general_rows}
    </table>

    <table class="blk wide">
      <tr><td class="sec" colspan="4">Physical properties</td></tr>
      {phys_rows}
    </table>

    <table class="blk wide">
      <tr><td class="sec" colspan="4">Handling parameter</td></tr>
      {hand_rows}
    </table>

    <div class="disc">{esc(disclaimer)}</div>
    {notes_html}
  </main>
"""


def main():
    for p in load_all():
        doc = render_product(p)
        name = f"LR_{p['display'].replace(' ', '_')}"
        if p["variant"]:
            name += "_" + p["variant"].replace(" ", "").replace(".", "")
        path = os.path.join(OUT, f"{name}.pdf")
        HTML(string=doc, base_url=HERE).write_pdf(path)
        print("wrote", os.path.basename(path))


if __name__ == "__main__":
    main()
