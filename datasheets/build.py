"""Render MULTIline technical data sheets as PDFs in the Lateral Repairs
brand style (matching the supplied FORCE TDS reference). Data is taken
verbatim from the Word documents via parse_tds.py — no values are changed."""
import base64
import datetime
import html
import os

from weasyprint import HTML

from parse_tds import load_all

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

PINK = "#E6007E"
SLATE = "#33414c"
GREY_BAR = "#bcbcbc"
BORDER = "#3f3f3f"
SECTION_BG = "#fbe7f1"

VERSION = "V2026.1"
FIRST_ISSUE = "2021.01.21"
VIEWED = datetime.date.today().strftime("%Y.%m.%d")


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


DROP = "data:image/png;base64," + b64(os.path.join(ASSETS, "drop.png"))


def esc(s):
    return html.escape(s).replace("\n", "<br>")


def nl_cell(s):
    """value cell that may contain a primary line + 'available on request'."""
    return esc(s)


def two_col(label, value):
    return (f'<tr><td class="k">{esc(label)}</td>'
            f'<td class="v">{nl_cell(value)}</td></tr>')


def render_product(p):
    title_main = "MULTIline"
    suffix = p["display"].replace("MULTIline ", "")
    variant = f' <span class="variant">{esc(p["variant"])}</span>' if p["variant"] else ""

    # supply rows
    supply_rows = "".join(two_col(k, v) for k, v in p["supply"])
    # general rows
    general_rows = "".join(two_col(k, v) for k, v in p["general"])
    seam_label = "Used seam (stitched)<br>and seam sealing"
    for i, s in enumerate(p["seam"]):
        general_rows += (f'<tr><td class="k">{seam_label if i == 0 else ""}</td>'
                         f'<td class="v">{esc(s)}</td></tr>')

    # physical: property | condition | unit | value
    phys_rows = ""
    for prop, cond, unit, val in p["physical"]:
        phys_rows += (f'<tr><td class="k">{esc(prop)}</td>'
                      f'<td class="cond">{esc(cond)}</td>'
                      f'<td class="unit">{esc(unit)}</td>'
                      f'<td class="val">{esc(val)}</td></tr>')

    # handling: property | value (value spans cond/unit/val which repeat)
    hand_rows = ""
    for prop, cond, unit, val in p["handling"]:
        hand_rows += (f'<tr><td class="k">{esc(prop)}</td>'
                      f'<td class="v" colspan="3">{esc(cond)}</td></tr>')

    notes_html = ""
    if p["notes"]:
        notes_html = '<div class="notes">' + "".join(
            f"<div>{esc(n)}</div>" for n in p["notes"]) + "</div>"

    disclaimer = p["disclaimer"] or (
        "The final quality depends on the resin system used, the inversion "
        "pressure and the curing pressure. We advise against the use of other "
        "resin systems or higher inversion and/or curing pressures and accept "
        "no liability.")

    body = f"""
  <div class="pageheader">
    <div class="hrow1">
      <div class="hcell brand">
        <img class="drop" src="{DROP}" alt="">
        <div class="word"><span class="l">LATERAL</span><br><span class="r">REPAIRS</span></div>
      </div>
      <div class="hcell tds">TECHNICAL DATA SHEET</div>
    </div>
    <div class="hrow2">
      <div class="hcell meta">
        Document Version: {VERSION}<br>
        Date of first issue: {FIRST_ISSUE}<br>
        Date viewed: {VIEWED}
      </div>
      <div class="hcell bigtitle">{title_main} <b>{esc(suffix)}</b>{variant}</div>
    </div>
  </div>

  <div class="pagefooter">
    <span class="fitem"><img class="fdrop" src="{DROP}"><a href="https://www.lateralrepairs.com">www.lateralrepairs.com</a></span>
    <span class="fitem"><img class="fdrop" src="{DROP}"><a href="mailto:info@lateralrepairs.com">info@lateralrepairs.com</a></span>
    <span class="fitem"><img class="fdrop" src="{DROP}">+370 698 76 581</span>
    <span class="fitem"><img class="fdrop" src="{DROP}">Paberžių g. 5, Tauragė, Lithuania, LT-72328</span>
  </div>

  <main>
    <table class="blk">
      <tr><td class="k">Product name</td><td class="v">{esc(p['product_name'])}</td></tr>
      <tr><td class="k">Product code</td><td class="v">{esc(p['product_code'])}</td></tr>
    </table>

    <table class="blk">
      <tr><td class="sec" colspan="2">Material composition</td></tr>
      <tr><td class="full" colspan="2">{esc(p['material'])}</td></tr>
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
    return PAGE_CSS + body


PAGE_CSS = f"""
<style>
  @page {{
    size: A4;
    margin: 3.15cm 1.25cm 1.65cm 1.25cm;
    @bottom-right {{
      content: "Page " counter(page) " of " counter(pages);
      font-family: 'Inter', sans-serif; font-size: 8pt; color: #444;
      margin-bottom: 1mm;
    }}
  }}
  * {{ box-sizing: border-box; }}
  html {{ font-family: 'Inter','DejaVu Sans',sans-serif; color: #111; font-size: 9.3pt; }}
  body {{ margin: 0; }}

  /* ---------- header (repeats each page) — table layout (no flex) ---------- */
  .pageheader {{ position: fixed; top: -3.15cm; left: -1.25cm;
    width: 21cm; height: 2.95cm; }}
  .hrow1 {{ display: table; width: 100%; height: 1.85cm; table-layout: fixed; }}
  .hrow2 {{ display: table; width: 100%; height: 1.1cm; table-layout: fixed;
    background: {GREY_BAR}; }}
  .hcell {{ display: table-cell; vertical-align: middle; }}
  .brand {{ padding-left: 1.0cm; }}
  .brand .drop {{ height: 1.3cm; vertical-align: middle; }}
  .brand .word {{ display: inline-block; vertical-align: middle;
    margin-left: 13px; line-height: 0.92;
    font-family: 'Space Grotesk','DejaVu Sans',sans-serif; font-weight: 700;
    letter-spacing: 1px; }}
  .brand .word .l {{ color: {PINK}; font-size: 20pt; }}
  .brand .word .r {{ color: {SLATE}; font-size: 20pt; }}
  .tds {{ width: 9.0cm; background: {PINK}; color: #fff; text-align: left;
    font-family: 'Space Grotesk','DejaVu Sans',sans-serif; font-weight: 700;
    font-size: 16.5pt; letter-spacing: .5px; padding-left: .7cm; }}
  .meta {{ padding-left: 1.0cm; font-size: 7.6pt; color: #222;
    line-height: 1.28; }}
  .bigtitle {{ color: #fff; text-align: right; padding-right: .7cm;
    font-family: 'Space Grotesk','DejaVu Sans',sans-serif; font-weight: 500;
    font-size: 20pt; letter-spacing: .5px; }}
  .bigtitle b {{ font-weight: 700; }}
  .bigtitle .variant {{ font-weight: 700; font-size: 14pt; vertical-align: 2px; }}

  /* ---------- footer (repeats each page) — inline layout (no flex) ---------- */
  .pagefooter {{ position: fixed; bottom: -1.12cm; left: -1.25cm;
    width: 21cm; height: 0.9cm; padding: 5px 1.0cm 0;
    border-top: 2px solid {PINK}; white-space: nowrap; }}
  .fitem {{ display: inline-block; font-size: 7pt; color: #333;
    margin-right: 6mm; }}
  .fitem:last-child {{ margin-right: 0; }}
  .fitem a {{ color: #333; text-decoration: none; }}
  .fitem .fdrop {{ height: 9px; width: auto; vertical-align: -1px;
    margin-right: 3px; }}

  /* ---------- tables ---------- */
  main {{ padding-top: 2mm; }}
  table.blk {{ width: 100%; border-collapse: collapse; margin-bottom: 4mm;
    border: 1px solid {BORDER}; }}
  table.blk td {{ border: 1px solid {BORDER}; padding: 3.1px 7px;
    vertical-align: top; }}
  td.sec {{ background: {SECTION_BG}; font-weight: 700; color: #6d0b3d;
    border-bottom: 1px solid {PINK}; }}
  td.k {{ width: 36%; font-weight: 700; }}
  td.v, td.full {{ }}
  table.blk.wide td.k {{ width: 33%; }}
  td.cond {{ width: 30%; color: #333; }}
  td.unit {{ width: 12%; color: #333; }}
  td.val {{ width: 25%; font-weight: 700; color: {PINK}; }}

  .disc {{ border: 1px solid {BORDER}; padding: 5px 8px; font-size: 8.4pt;
    color: #222; margin-bottom: 3mm; line-height: 1.35; }}
  .notes {{ font-size: 8pt; color: #444; line-height: 1.5; }}
  .notes div {{ margin-bottom: .6mm; }}
</style>
"""


def main():
    products = load_all()
    for p in products:
        doc = render_product(p)
        slug = p["slug"]
        name = f"LR_{p['display'].replace(' ', '_')}"
        if p["variant"]:
            name += "_" + p["variant"].replace(" ", "").replace(".", "")
        path = os.path.join(OUT, f"{name}.pdf")
        HTML(string=doc, base_url=HERE).write_pdf(path)
        print("wrote", os.path.basename(path))


if __name__ == "__main__":
    main()
