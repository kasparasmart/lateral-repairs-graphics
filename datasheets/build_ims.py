"""IMS-style Lateral Repairs technical data sheets (v2).

Reproduces the IMS Group datasheet layout (charcoal labels, pink section bars,
two-column features, combined Features/Length/Resin/Pressure table, QR codes,
notice block) with Lateral Repairs branding (pink #E6007E, LR drop, Raleway).

Per-diameter data (elongation / inversion / curing / burst) comes from the
Lateral Repairs app tables; resin (kg/m), layflat width and cm-per-bend are
manufacturer figures to be supplied — shown as "on request" until provided.
"""
import base64
import os

from weasyprint import HTML

from parse_tds import load_all

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "out_ims")
os.makedirs(OUT, exist_ok=True)

PINK = "#E6007E"
CHAR = "#2f2c33"
GREY1 = "#d7d5db"
GREY2 = "#c9c7cf"

APP_IOS = "https://apps.apple.com/us/app/lateral-repairs/id1559870871"
APP_AND = "https://play.google.com/store/apps/details?id=com.lateralrepairs.app"


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


DROP = "data:image/png;base64," + b64(os.path.join(ASSETS, "drop.png"))
QR_IOS = "data:image/png;base64," + b64(os.path.join(ASSETS, "qr", "resincalc-ios.png"))
QR_AND = "data:image/png;base64," + b64(os.path.join(ASSETS, "qr", "resincalc-android.png"))
RAL = os.path.join(ASSETS, "fonts_raleway")

SUBTITLE = {
    "MULTIline PRO": "Hose liner for the trenchless inner lining of defective, leaking and statically impaired pipes.",
    "MULTIline FLEX": "Flexible hose liner for the trenchless rehabilitation of drains and house connections.",
    "MULTIline CORE": "Multi-knitted hose liner for the trenchless inner lining of pipes.",
    "MULTIline FORCE": "High-strength reinforced hose liner for structural pipe rehabilitation.",
}

# per-diameter installation table (from the LR app). value = cm-per-bend add.
# Only PRO is wired here for the design proof.
import json
PRO_ROWS = json.load(open(os.path.join(ASSETS, "pro_table.json"), encoding="utf-8"))


def css():
    return f"""
<style>
  @font-face {{ font-family:'Ral'; src:url('file://{RAL}/Raleway-Regular.ttf'); font-weight:400; }}
  @font-face {{ font-family:'Ral'; src:url('file://{RAL}/Raleway-Medium.ttf'); font-weight:500; }}
  @font-face {{ font-family:'Ral'; src:url('file://{RAL}/Raleway-SemiBold.ttf'); font-weight:600; }}
  @font-face {{ font-family:'Ral'; src:url('file://{RAL}/Raleway-Bold.ttf'); font-weight:700; }}
  @font-face {{ font-family:'Ral'; src:url('file://{RAL}/Raleway-Black.ttf'); font-weight:900; }}
  @page {{ size:A4; margin:13mm 11mm 12mm 14mm;
    @bottom-right {{ content:"Page " counter(page) " of " counter(pages);
      font-family:'Ral'; font-size:7.5pt; color:#888; }} }}
  * {{ box-sizing:border-box; }}
  html {{ font-family:'Ral',sans-serif; color:#1a1820; font-size:9pt; }}
  body {{ margin:0; }}
  .sidebar {{ position:fixed; top:-13mm; left:-14mm; width:7mm; height:297mm;
    background:{CHAR}; }}

  h1.tds {{ font-weight:500; font-size:21pt; color:#3a3742; margin:0 0 6px; }}
  .titlebar {{ background:#e6e4e9; padding:11px 16px; display:flex;
    align-items:center; justify-content:space-between; margin-bottom:9px; }}
  .titlebar .t {{ font-weight:900; font-size:30pt; letter-spacing:-.5px; }}
  .titlebar .t .a {{ color:{CHAR}; }}
  .titlebar .t .b {{ color:{PINK}; }}
  .titlebar img {{ height:1.5cm; }}
  .lede {{ font-size:10pt; color:#3a3742; margin:0 0 12px; }}

  .cols {{ display:flex; gap:14px; }}
  .col {{ flex:1; }}
  table.f {{ width:100%; border-collapse:collapse; }}
  table.f td {{ padding:0; }}
  .hd {{ background:{PINK}; color:#fff; font-weight:700; font-size:11pt;
    text-align:center; padding:8px; }}
  table.f td.k {{ background:{CHAR}; color:#fff; font-weight:700; width:42%;
    text-align:center; padding:7px 8px; border-bottom:2px solid #fff;
    vertical-align:middle; }}
  table.f td.v {{ color:#1a1820; text-align:center; padding:7px 8px;
    border-bottom:2px solid #fff; vertical-align:middle; }}
  table.f tr:nth-child(odd) td.v {{ background:{GREY1}; }}
  table.f tr:nth-child(even) td.v {{ background:{GREY2}; }}
  td.k .ic {{ height:15px; vertical-align:middle; }}

  /* combined table */
  table.big {{ width:100%; border-collapse:collapse; margin-top:13px; }}
  table.big th.grp {{ background:{PINK}; color:#fff; font-weight:700;
    font-size:10.5pt; padding:7px 4px; border:2px solid #fff; }}
  table.big th.sub {{ background:{CHAR}; color:#fff; font-weight:700;
    font-size:8pt; padding:6px 3px; border:2px solid #fff; }}
  table.big td {{ text-align:center; padding:5px 3px; border:2px solid #fff;
    font-size:8.5pt; }}
  table.big tr:nth-child(odd) td {{ background:{GREY1}; }}
  table.big tr:nth-child(even) td {{ background:{GREY2}; }}
  table.big td.dim {{ font-weight:600; }}
  .req {{ color:#8a8690; font-style:italic; }}

  /* qr + notice */
  .lower {{ display:flex; gap:16px; margin-top:14px; }}
  .qr {{ width:43%; border:1px solid #d8d6dc; border-radius:8px; padding:11px 13px; }}
  .qr h4 {{ margin:0 0 8px; font-size:10pt; color:{CHAR}; }}
  .qr .codes {{ display:flex; gap:16px; }}
  .qr .code {{ text-align:center; font-size:8pt; color:#3a3742; }}
  .qr .code img {{ width:2.6cm; height:2.6cm; display:block; margin:0 auto 4px; }}
  .notice {{ flex:1; }}
  .notice h4 {{ margin:0 0 5px; font-size:10pt; color:{CHAR}; }}
  .notice ul {{ margin:0; padding-left:14px; }}
  .notice li {{ font-size:7.6pt; color:#444; line-height:1.45; margin-bottom:2px; }}
  .foot {{ margin-top:10px; border-top:1px solid #ddd; padding-top:5px;
    display:flex; justify-content:space-between; font-size:7.5pt; color:#888; }}
  .foot a {{ color:{PINK}; text-decoration:none; }}
</style>"""


ICON_DIA = ('<svg class="ic" viewBox="0 0 48 24" fill="none" stroke="#fff" '
            'stroke-width="2.5"><circle cx="24" cy="12" r="9"/>'
            '<path d="M9 12h30M13 8l-4 4 4 4M35 8l4 4-4 4" stroke-linecap="round" '
            'stroke-linejoin="round"/></svg>')


def feature_table(title, rows):
    body = ""
    for k, v in rows:
        body += f'<tr><td class="k">{k}</td><td class="v">{v}</td></tr>'
    return (f'<table class="f"><tr><td class="hd" colspan="2">{title}</td></tr>'
            f'{body}</table>')


def render_pro(p):
    # product / material features
    diam = next((v for k, v in p["supply"] if k == "Pipe diameter"), "")
    diam = diam.split("\n")[0]
    undersize = next((v for k, v in p["supply"] if "undersized" in k.lower()), "")
    lengths = next((v for k, v in p["supply"] if k == "Liner lengths"), "").split("\n")[0]
    gd = dict(p["general"])
    heat = next((c for pr, c, u, v in p["handling"] if "Heat" in pr), "")
    bend = next((c for pr, c, u, v in p["handling"] if "bend" in pr.lower()), "")
    pinch = next((c for pr, c, u, v in p["handling"] if "Pinch" in pr), "")
    addl = next((c for pr, c, u, v in p["handling"] if "Additional" in pr or "lenght" in pr.lower()), "")

    prod_rows = [
        ("Product name", p["product_name"]),
        ("Length", lengths),
        (f'{ICON_DIA} Diameter', diam),
        ("Liner undersized", undersize),
        ("Curing techniques", "Ambient, Warm (Water / Steam)"),
        ("Negotiating bends", bend),
    ]
    mat_rows = [
        ("Textile", gd.get("Type of fibers", "")),
        ("Material", p["material"]),
        ("Coating", gd.get("Coating", "")),
        ("Colour", gd.get("Basic color", "")),
        ("Coating colour", gd.get("Color coating", "")),
        ("Storage", "Protected from light, dry, 5–30 °C"),
    ]

    # combined table rows
    big = ""
    for r in PRO_ROWS:
        dim = f'DN {r["liner"].split("/")[0].strip()} → {r["pipe"].split("/")[0].strip()}'
        big += (f'<tr><td class="dim">{dim}</td>'
                f'<td>{bend or "Max. 90°"}</td>'
                f'<td>{r["elong"]} cm/m</td>'
                f'<td class="req">on request</td>'
                f'<td>{r["inv"]}</td><td>{r["cure"]}</td><td>{r["burst"]}</td></tr>')

    notes = [
        "Given the diversity of installation conditions and process techniques, the information in this data sheet can only be regarded as non-binding guideline values.",
        f"Length addition: add {addl or '2–5%'} of the liner length; for bends add the cm value per 45° as listed (on request).",
        "Final quality depends on the resin system, inversion pressure and curing pressure. We advise against other resin systems or higher pressures and accept no liability.",
        "All data were determined at 20 °C / 68 °F; bench-scale values that may differ on site.",
    ]

    return css() + f"""
  <div class="sidebar"></div>
  <h1 class="tds">Technical data sheet</h1>
  <div class="titlebar">
    <div class="t"><span class="a">MULTI</span><span class="b">line {p['display'].replace('MULTIline ','')}{(' '+p['variant']) if p['variant'] else ''}</span></div>
    <img src="{DROP}" alt="">
  </div>
  <p class="lede">{SUBTITLE.get(p['display'],'')}</p>

  <div class="cols">
    <div class="col">{feature_table("Product features", prod_rows)}</div>
    <div class="col">{feature_table("Material features", mat_rows)}</div>
  </div>

  <table class="big">
    <tr>
      <th class="grp" colspan="2">Features</th>
      <th class="grp">Length</th>
      <th class="grp">Resin</th>
      <th class="grp" colspan="3">Pressure</th>
    </tr>
    <tr>
      <th class="sub">Dimension</th><th class="sub">Bend</th>
      <th class="sub">L + elongation</th>
      <th class="sub">kg / m</th>
      <th class="sub">Inversion (bar)</th><th class="sub">Curing (bar)</th><th class="sub">Burst (bar)</th>
    </tr>
    {big}
  </table>

  <div class="lower">
    <div class="qr">
      <h4>Resin quantity — Lateral Repairs app</h4>
      <div class="codes">
        <div class="code"><img src="{QR_IOS}"><div>iPhone<br>App&nbsp;Store</div></div>
        <div class="code"><img src="{QR_AND}"><div>Android<br>Google&nbsp;Play</div></div>
      </div>
    </div>
    <div class="notice">
      <h4>Notice</h4>
      <ul>{''.join(f'<li>{n}</li>' for n in notes)}</ul>
    </div>
  </div>

  <div class="foot">
    <div>For further information visit <a href="https://www.lateralrepairs.com">www.lateralrepairs.com</a> or scan the QR codes.</div>
    <div>Issue: V2026.1 · 2026.06</div>
  </div>
"""


def main():
    pro = next(p for p in load_all() if p["slug"] == "pro-45")
    HTML(string=render_pro(pro), base_url=HERE).write_pdf(os.path.join(OUT, "PROOF_MULTIline_PRO.pdf"))
    print("wrote PROOF_MULTIline_PRO.pdf")


if __name__ == "__main__":
    main()
