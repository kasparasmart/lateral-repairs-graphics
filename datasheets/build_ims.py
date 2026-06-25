"""IMS-style Lateral Repairs technical data sheets.

Reproduces the IMS Group datasheet layout as closely as possible — charcoal
label cells, pink section bars, two-column features with little icons, a
combined Features / Length / Resin / Pressure table, QR codes and a notice
block — but with Lateral Repairs colours (#E6007E), the LR drop logo, Raleway
type and Lateral Repairs product information.

Per-diameter data (elongation / inversion / curing) comes from the Lateral
Repairs app tables for PRO (ex-NanoTech) and FLEX (ex-DrainPlus). Resin (kg/m),
layflat width and cm-per-bend, and the FORCE / CORE tables, are shown as
"on request" until the manufacturer supplies them.
"""
import base64
import json
import os

from weasyprint import HTML

from icons import ICONS
from parse_tds import load_all

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "out_ims")
os.makedirs(OUT, exist_ok=True)

PINK = "#E6007E"
CHAR = "#2f2c33"
GREY1 = "#d9d7dd"
GREY2 = "#cbc9d1"
REQ = '<span class="req">on request</span>'


def b64(p):
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode()


DROP = "data:image/png;base64," + b64(os.path.join(ASSETS, "drop.png"))
QR_IOS = "data:image/png;base64," + b64(os.path.join(ASSETS, "qr", "resincalc-ios.png"))
QR_AND = "data:image/png;base64," + b64(os.path.join(ASSETS, "qr", "resincalc-android.png"))
RAL = os.path.join(ASSETS, "fonts_raleway")

PRO_ROWS = json.load(open(os.path.join(ASSETS, "pro_table.json"), encoding="utf-8"))
FLEX_ROWS = json.load(open(os.path.join(ASSETS, "flex_table.json"), encoding="utf-8"))
EXCEL = json.load(open(os.path.join(ASSETS, "excel_data.json"), encoding="utf-8"))


def dash(v):
    v = str(v).strip()
    return "–" if v in ("", "-", "None") else v


def pct(v):
    """L+** column: 0.04 -> '4 %', '-' -> en dash."""
    v = str(v).strip()
    if v in ("", "-", "None"):
        return "–"
    try:
        return f"{round(float(v) * 100)} %"
    except ValueError:
        return v

SUBTITLE = {
    "MULTIline PRO": "Hose liner for the trenchless inner lining of defective, leaking and statically impaired pipes.",
    "MULTIline FLEX": "Flexible hose liner for the trenchless rehabilitation of drains and house connections.",
    "MULTIline CORE": "Multi-knitted hose liner for the trenchless inner lining of pipes.",
    "MULTIline FORCE": "High-strength, reinforced hose liner for the structural rehabilitation of pipes.",
}


def css():
    return f"""
<style>
  @font-face {{ font-family:'Ral'; src:url('file://{RAL}/Raleway-Regular.ttf'); font-weight:400; }}
  @font-face {{ font-family:'Ral'; src:url('file://{RAL}/Raleway-Medium.ttf'); font-weight:500; }}
  @font-face {{ font-family:'Ral'; src:url('file://{RAL}/Raleway-SemiBold.ttf'); font-weight:600; }}
  @font-face {{ font-family:'Ral'; src:url('file://{RAL}/Raleway-Bold.ttf'); font-weight:700; }}
  @font-face {{ font-family:'Ral'; src:url('file://{RAL}/Raleway-Black.ttf'); font-weight:900; }}
  @page {{ size:A4; margin:11mm 10mm 15mm 13mm;
    @bottom-right {{ content:"Page " counter(page) " of " counter(pages);
      font-family:'Ral'; font-size:6.5pt; color:#aaa; margin-bottom:11mm; }} }}
  * {{ box-sizing:border-box; }}
  html {{ font-family:'Ral',sans-serif; color:#1a1820; font-size:8.5pt; }}
  body {{ margin:0; }}
  .sidebar {{ position:fixed; top:-11mm; left:-13mm; width:6mm; height:297mm; background:{CHAR}; }}
  .contactbar {{ position:fixed; bottom:-15mm; left:-13mm; width:210mm; height:10mm;
    background:{PINK}; }}
  .contactbar .crow {{ display:table; width:100%; height:10mm; }}
  .contactbar .ci {{ display:table-cell; vertical-align:middle; text-align:center;
    color:#fff; font-size:7pt; font-weight:500; }}
  .contactbar .ci .cic {{ height:11px; width:11px; vertical-align:-2px; margin-right:4px; }}

  h1.tds {{ font-weight:500; font-size:18pt; color:#3a3742; margin:0 0 5px; }}
  .titlebar {{ background:#e7e5ea; padding:7px 15px; display:flex; align-items:center;
    justify-content:space-between; margin-bottom:7px; }}
  .titlebar .t {{ font-weight:900; font-size:27pt; letter-spacing:-.5px; }}
  .titlebar .t .a {{ color:{CHAR}; }} .titlebar .t .b {{ color:{PINK}; }}
  .titlebar img {{ height:1.35cm; }}
  .lede {{ font-size:9pt; color:#3a3742; margin:0 0 6px; }}

  .cols {{ display:flex; gap:12px; }} .col {{ flex:1; }}
  table.f {{ width:100%; border-collapse:collapse; }}
  .hd {{ background:{PINK}; color:#fff; font-weight:700; font-size:10pt; text-align:center; padding:6px; }}
  table.f td.k {{ background:{CHAR}; color:#fff; font-weight:600; width:46%; padding:3px 8px;
    border-bottom:2px solid #fff; vertical-align:middle; }}
  table.f td.k .ic {{ height:13px; width:13px; vertical-align:-2px; margin-right:6px; }}
  table.f td.v {{ color:#1a1820; padding:3px 8px; border-bottom:2px solid #fff; vertical-align:middle;
    font-weight:500; }}
  table.f tr:nth-child(odd) td.v {{ background:{GREY1}; }}
  table.f tr:nth-child(even) td.v {{ background:{GREY2}; }}

  table.big {{ width:100%; border-collapse:collapse; margin-top:11px; }}
  table.big th.grp {{ background:{PINK}; color:#fff; font-weight:700; font-size:9.5pt;
    padding:6px 3px; border:2px solid #fff; }}
  table.big th.sub {{ background:{CHAR}; color:#fff; font-weight:600; font-size:7.3pt;
    padding:5px 2px; border:2px solid #fff; line-height:1.15; }}
  table.big th.sub .ic {{ height:12px; width:12px; vertical-align:-2px; }}
  table.big td {{ text-align:center; padding:2.5px 2px; border:2px solid #fff; font-size:7.8pt; }}
  table.big tr:nth-child(odd) td {{ background:{GREY1}; }}
  table.big tr:nth-child(even) td {{ background:{GREY2}; }}
  table.big td.dim {{ font-weight:600; }}
  .req {{ color:#8a8690; font-style:italic; }}
  .bigfoot {{ margin:4px 0 0; font-size:7pt; color:#777; }}

  .lower {{ display:flex; gap:14px; margin-top:11px; }}
  .qr {{ width:42%; border:1px solid #dcdae0; border-radius:8px; padding:9px 12px; }}
  .qr h4 {{ margin:0 0 3px; font-size:9.5pt; color:{CHAR}; }}
  .qr p {{ margin:0 0 7px; font-size:7.4pt; color:#555; }}
  .qr .codes {{ display:flex; gap:14px; }}
  .qr .code {{ text-align:center; font-size:7.4pt; color:#3a3742; }}
  .qr .code img {{ width:2.4cm; height:2.4cm; display:block; margin:0 auto 3px; }}
  .notice {{ flex:1; }}
  .notice h4 {{ margin:0 0 4px; font-size:9.5pt; color:{CHAR}; }}
  .notice ul {{ margin:0; padding-left:13px; }}
  .notice li {{ font-size:7.2pt; color:#444; line-height:1.4; margin-bottom:2px; }}
  .foot {{ margin-top:8px; border-top:1px solid #ddd; padding-top:4px; display:flex;
    justify-content:space-between; font-size:7pt; color:#999; }}
  .foot a {{ color:{PINK}; text-decoration:none; }}
</style>"""


def ic(name):
    return ICONS.get(name, "")


_CW = ('<svg class="cic" viewBox="0 0 24 24" fill="none" stroke="#fff" '
       'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{}</svg>')
CONTACT = {
    "globe": _CW.format('<circle cx="12" cy="12" r="9"/>'
                        '<path d="M3 12h18M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18z"/>'),
    "mail": _CW.format('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
    "phone": _CW.format('<path d="M5 4h4l2 5-3 2a12 12 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>'),
    "pin": _CW.format('<path d="M12 21s-7-5.3-7-11a7 7 0 0 1 14 0c0 5.7-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>'),
}


def contactbar():
    return f"""
  <div class="contactbar"><div class="crow">
    <span class="ci">{CONTACT['globe']} www.lateralrepairs.com</span>
    <span class="ci">{CONTACT['mail']} info@lateralrepairs.com</span>
    <span class="ci">{CONTACT['phone']} +370 698 76 581</span>
    <span class="ci">{CONTACT['pin']} Paberžių g. 5, Tauragė, Lithuania, LT-72328</span>
  </div></div>"""


def phys(p, key):
    for pr, cond, unit, val in p["physical"]:
        if key.lower() in pr.lower():
            return pr, cond, unit, val
    return None


def fmt_thickness(p):
    t = phys(p, "Thickness")
    if not t:
        return REQ
    units = t[2].split("\n")
    vals = t[3].split("\n")
    parts = [f"{v} {u}" for v, u in zip(vals, units)]
    return " / ".join(parts)


def fmt_weight(p, key):
    t = phys(p, key)
    return f"{t[3]} {t[2]}" if t else REQ


def feature_table(title, rows):
    body = ""
    for icon, k, v in rows:
        lbl = (ic(icon) + " " if icon else "") + k
        body += f'<tr><td class="k">{lbl}</td><td class="v">{v}</td></tr>'
    return f'<table class="f"><tr><td class="hd" colspan="2">{title}</td></tr>{body}</table>'


def hget(p, needle, default=""):
    for pr, cond, unit, val in p["handling"]:
        if needle.lower() in pr.lower():
            return cond
    return default


def addlen(p):
    """Additional length % from the Word handling table (e.g. '5 %')."""
    v = hget(p, "Additional", "")
    return v.replace(" ", "") if v else ""


def water(p):
    t = phys(p, "Water penetration")
    if not t:
        return REQ
    units = t[2].split("\n")
    vals = t[3].split("\n")
    if len(units) == len(vals) and len(vals) > 1:
        return " / ".join(f"{v} {u}" for v, u in zip(vals, units))
    return f"{t[3]} {t[2]}".strip()


def big_table(p):
    block = EXCEL.get(p["slug"], {"rows": [], "foot": ""})
    body = ""
    for r in block["rows"]:
        body += (f'<tr><td class="dim">{dash(r["dim"])}</td>'
                 f'<td>{dash(r["flat"])}</td><td>{dash(r["bend"])}</td>'
                 f'<td>{dash(r["lbend"])}</td><td>{pct(r["lpct"])}</td>'
                 f'<td>{dash(r["resin"])}</td><td>{dash(r["inv"])}</td>'
                 f'<td>{dash(r["d3"])}</td><td>{dash(r["roller"])}</td></tr>')
    foot = block.get("foot", "")
    foot_html = f'<p class="bigfoot">{foot}</p>' if foot else ""
    return f"""
  <table class="big">
    <tr>
      <th class="grp" colspan="3">Features</th>
      <th class="grp" colspan="2">Length</th>
      <th class="grp">Resin</th>
      <th class="grp" colspan="2">Pressure</th>
      <th class="grp">Roller</th>
    </tr>
    <tr>
      <th class="sub">Dimension</th>
      <th class="sub">Flat (mm)</th>
      <th class="sub">{ic('bend')} Bend</th>
      <th class="sub">{ic('bend')} L + * (cm)</th>
      <th class="sub">{ic('liner')} L + ** (%)</th>
      <th class="sub">{ic('resin')} kg / m</th>
      <th class="sub">Inversion (bar)</th>
      <th class="sub">3D (bar)</th>
      <th class="sub">Roller gap</th>
    </tr>
    {body}
  </table>{foot_html}"""


def render(p):
    p = dict(p)
    thickness = fmt_thickness(p)
    # the current PRO range is 4.0 mm and 5.5 mm; the 4.5 mm sheet is updated to
    # 5.5 mm to match the manufacturer's Liners_TDS data.
    if p["slug"] == "pro-45":
        p["variant"] = "5.5 mm"
        p["product_name"] = p["product_name"].replace("4.5 mm", "5.5 mm").replace("4,5", "5,5")
        thickness = "5,50 mm / 0,22 inch"

    diam = next((v for k, v in p["supply"] if k == "Pipe diameter"), "").split("\n")[0]
    length = next((v for k, v in p["supply"] if k == "Liner lengths"), "").split("\n")[0]
    undersize = next((v for k, v in p["supply"] if "undersized" in k.lower()), "")
    gd = dict(p["general"])

    prod_rows = [
        ("", "Product name", p["product_name"]),
        ("", "Product code", p["product_code"]),
        ("length", "Length", length),
        ("diameter", "Diameter", diam),
        ("thickness", "Wall thickness", thickness),
        ("undersize", "Liner undersized", undersize),
        ("curing", "Heat resistance", hget(p, "Heat", REQ)),
        ("bend", "Negotiating bends", hget(p, "bend", REQ)),
    ]
    mat_rows = [
        ("material", "Material", p["material"]),
        ("textile", "Textile", gd.get("Type of fibers", "")),
        ("weight", "Textile weight", fmt_weight(p, "Weight")),
        ("coating", "Coating", gd.get("Coating", "")),
        ("weight", "Coating weight", fmt_weight(p, "Weight of coating")),
        ("colour", "Colour / coating", f'{gd.get("Basic color","")} / {gd.get("Color coating","")}'),
        ("resin", "Water penetration", water(p)),
        ("storage", "Storage", "Protected from light, dry"),
    ]

    title_suffix = p["display"].replace("MULTIline ", "") + ((" " + p["variant"]) if p["variant"] else "")
    notes = [
        "Given the diversity of installation conditions, application areas and process techniques, the information in this data sheet can only be regarded as non-binding guideline values.",
        "Length addition: add the stated percentage of the liner length, plus the cm value per 45° bend; calculate the exact resin quantity with the Lateral Repairs app (scan the QR codes).",
        "The final quality depends on the resin system used, the inversion pressure and the curing pressure. We advise against the use of other resin systems or higher pressures and accept no liability.",
        "All data were determined at 20 °C / 68 °F and are bench-scale values that can differ on industrial job sites.",
    ]

    return css() + f"""
  <div class="sidebar"></div>
  <h1 class="tds">Technical data sheet</h1>
  <div class="titlebar">
    <div class="t"><span class="a">MULTI</span><span class="b">line {title_suffix}</span></div>
    <img src="{DROP}" alt="">
  </div>
  <p class="lede">{SUBTITLE.get(p['display'],'')}</p>
  <div class="cols">
    <div class="col">{feature_table("Product features", prod_rows)}</div>
    <div class="col">{feature_table("Material features", mat_rows)}</div>
  </div>
  {big_table(p)}
  <div class="lower">
    <div class="qr">
      <h4>Resin quantity</h4>
      <p>Calculate the exact resin amount with the free Lateral Repairs app.</p>
      <div class="codes">
        <div class="code"><img src="{QR_IOS}"><div>iPhone · App&nbsp;Store</div></div>
        <div class="code"><img src="{QR_AND}"><div>Android · Google&nbsp;Play</div></div>
      </div>
    </div>
    <div class="notice">
      <h4>Notice</h4>
      <ul>{''.join(f'<li>{n}</li>' for n in notes)}</ul>
    </div>
  </div>
  <div class="foot"><div>Issue: V2026.1 · 2026.06</div></div>
  {contactbar()}
"""


def main():
    from pypdf import PdfWriter
    files = []
    for p in load_all():
        variant = "5.5 mm" if p["slug"] == "pro-45" else p["variant"]
        name = "LR_" + p["display"].replace(" ", "_")
        if variant:
            name += "_" + variant.replace(" ", "").replace(".", "")
        path = os.path.join(OUT, name + ".pdf")
        HTML(string=render(p), base_url=HERE).write_pdf(path)
        files.append(path)
        print("wrote", name + ".pdf")

    order = ["PRO_40mm", "PRO_55mm", "FLEX", "CORE", "FORCE", "FORCE_RF", "FORCE_UV"]
    files.sort(key=lambda f: next((i for i, k in enumerate(order) if k in f), 99))
    w = PdfWriter()
    for f in files:
        w.append(f)
    combined = os.path.join(OUT, "LR_MULTIline_ALL_datasheets.pdf")
    with open(combined, "wb") as fh:
        w.write(fh)
    print("wrote", os.path.basename(combined), f"({len(files)} sheets)")


if __name__ == "__main__":
    main()
