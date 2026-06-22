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
  @page {{ size:A4; margin:11mm 10mm 10mm 13mm;
    @bottom-right {{ content:"Page " counter(page) " of " counter(pages);
      font-family:'Ral'; font-size:7pt; color:#999; }} }}
  * {{ box-sizing:border-box; }}
  html {{ font-family:'Ral',sans-serif; color:#1a1820; font-size:8.5pt; }}
  body {{ margin:0; }}
  .sidebar {{ position:fixed; top:-11mm; left:-13mm; width:6mm; height:297mm; background:{CHAR}; }}

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


def build_rows(p):
    """Return list of dicts: dim, flat, bend, lbend, lelong, resin, inv, cure."""
    bend = hget(p, "bend", "Max. 45°" if "FORCE" in p["display"] else "Max. 90°")
    al = addlen(p) or REQ          # additional length % (Word) — applies over full Ø range
    rows = []
    if p["slug"] in ("pro-40", "pro-45"):
        for r in PRO_ROWS:
            ln = r["liner"].split("/")[0].strip()
            pi = r["pipe"].split("/")[0].strip()
            rows.append(dict(dim=f"DN {ln} → {pi}", flat=REQ, bend=bend, lbend=REQ,
                             lelong=f'{r["elong"]} cm/m', resin=REQ, inv=r["inv"], cure=r["cure"]))
    elif p["slug"] == "flex":
        for r in FLEX_ROWS:
            d = r["dim"].replace(' pipe', '').replace('into', '→')
            for q in ('(2")', '(2.8")', '(4")', '(5")', '(6")', '(8")', '(9")', '(10")'):
                d = d.replace(q, '')
            d = " ".join(d.split())
            rows.append(dict(dim=d, flat=REQ, bend=bend, lbend=REQ,
                             lelong=f'{r["elong"]} cm/m', resin=REQ, inv=r["contact"], cure=REQ))
    elif p["slug"] == "core":
        diam = next((v for k, v in p["supply"] if k == "Pipe diameter"), "")
        for dn in [x.strip().rstrip(".") for x in diam.split("\n")[0].split(",") if x.strip()]:
            rows.append(dict(dim=f"DN {dn}", flat=REQ, bend=bend, lbend=REQ,
                             lelong=al, resin=REQ, inv=REQ, cure=REQ))
    else:  # force, force-rf, force-uv : diameter range
        diam = next((v for k, v in p["supply"] if k == "Pipe diameter"), "").split("\n")[0]
        rows.append(dict(dim=diam, flat=REQ, bend=bend, lbend=REQ,
                         lelong=al, resin=REQ, inv=REQ, cure=REQ))
    return rows


def big_table(rows):
    body = ""
    for r in rows:
        body += (f'<tr><td class="dim">{r["dim"]}</td><td>{r["flat"]}</td><td>{r["bend"]}</td>'
                 f'<td>{r["lbend"]}</td><td>{r["lelong"]}</td><td>{r["resin"]}</td>'
                 f'<td>{r["inv"]}</td><td>{r["cure"]}</td></tr>')
    return f"""
  <table class="big">
    <tr>
      <th class="grp" colspan="3">Features</th>
      <th class="grp" colspan="2">Length</th>
      <th class="grp">Resin</th>
      <th class="grp" colspan="2">Pressure</th>
    </tr>
    <tr>
      <th class="sub">Dimension</th>
      <th class="sub">Flat (cm)</th>
      <th class="sub">{ic('bend')} Bend</th>
      <th class="sub">{ic('bend')} L + bend (cm)</th>
      <th class="sub">{ic('liner')} L + length</th>
      <th class="sub">{ic('resin')} kg / m</th>
      <th class="sub">Inversion (bar)</th>
      <th class="sub">Curing (bar)</th>
    </tr>
    {body}
  </table>"""


def render(p):
    diam = next((v for k, v in p["supply"] if k == "Pipe diameter"), "").split("\n")[0]
    length = next((v for k, v in p["supply"] if k == "Liner lengths"), "").split("\n")[0]
    undersize = next((v for k, v in p["supply"] if "undersized" in k.lower()), "")
    gd = dict(p["general"])

    al = addlen(p)
    prod_rows = [
        ("", "Product name", p["product_name"]),
        ("", "Product code", p["product_code"]),
        ("length", "Length", length),
        ("diameter", "Diameter", diam),
        ("thickness", "Wall thickness", fmt_thickness(p)),
        ("undersize", "Liner undersized", undersize),
        ("length", "Additional length", al or REQ),
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
  {big_table(build_rows(p))}
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
  <div class="foot">
    <div>For further information visit <a href="https://www.lateralrepairs.com">www.lateralrepairs.com</a> · info@lateralrepairs.com</div>
    <div>Issue: V2026.1 · 2026.06</div>
  </div>
"""


def main():
    for p in load_all():
        name = "LR_" + p["display"].replace(" ", "_")
        if p["variant"]:
            name += "_" + p["variant"].replace(" ", "").replace(".", "")
        HTML(string=render(p), base_url=HERE).write_pdf(os.path.join(OUT, name + ".pdf"))
        print("wrote", name + ".pdf")


if __name__ == "__main__":
    main()
