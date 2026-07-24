"""Extra Lateral Repairs technical data sheets (Glassfiber Complex, Connection
Liners) rendered in the same IMS-style LR format as the MULTIline range.
Reuses the styling, logo, QR codes and icons from build_ims.py."""
import os

from weasyprint import HTML

import build_ims as B

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "out_ims")
os.makedirs(OUT, exist_ok=True)

CONN_DIAGRAM = "data:image/png;base64," + B.b64(os.path.join(HERE, "assets", "conn_diagram.png"))

EXTRA_CSS = f"""
<style>
  table.f td.k2 {{ background:{B.CHAR}; color:#fff; font-weight:600; width:38%;
    padding:3px 8px; border-bottom:2px solid #fff; vertical-align:middle; }}
  table.f td.k2 .ic {{ height:13px; width:13px; vertical-align:-2px; margin-right:6px; }}
  table.f3 {{ width:100%; border-collapse:collapse; }}
  table.f3 td {{ border-bottom:2px solid #fff; padding:3px 8px; vertical-align:middle; }}
  table.f3 td.k {{ background:{B.CHAR}; color:#fff; font-weight:600; width:34%; }}
  table.f3 td.m {{ width:42%; font-weight:500; }}
  table.f3 td.t {{ width:24%; color:#3a3742; font-size:8pt; }}
  table.f3 tr:nth-child(odd) td.m {{ background:{B.GREY1}; }}
  table.f3 tr:nth-child(even) td.m {{ background:{B.GREY2}; }}
  table.f3 tr:nth-child(odd) td.t {{ background:#e7e5ea; }}
  table.f3 tr:nth-child(even) td.t {{ background:#dedce3; }}
  .hd3 {{ background:{B.PINK}; color:#fff; font-weight:700; font-size:10pt; padding:6px; }}
  .hd3 .sub {{ font-weight:500; font-size:8pt; opacity:.9; }}
  .card {{ border:1px solid #dcdae0; border-radius:8px; padding:9px 13px; margin-top:11px; }}
  .card h4 {{ margin:0 0 4px; font-size:9.5pt; color:{B.CHAR}; }}
  .card p {{ margin:0 0 4px; font-size:8pt; color:#444; line-height:1.45; }}
  .twocard {{ display:flex; gap:14px; }} .twocard .card {{ flex:1; }}
  .desc {{ font-size:9.5pt; color:#3a3742; line-height:1.6; margin:0 0 10px; }}
  .secttl {{ background:{B.PINK}; color:#fff; font-weight:700; font-size:11pt;
    text-align:center; padding:7px; margin:14px 0 0; }}
  .illus {{ text-align:center; margin:26px 0 6px; }}
  .illus img {{ max-width:90%; max-height:13cm; }}
  .illus figcaption {{ margin-top:12px; font-size:9pt; color:#777; }}
  .pagebreak {{ break-before:page; }}
  .bl {{ display:block; position:relative; padding-left:13px; font-size:8pt; color:#333;
    line-height:1.4; margin:1px 0; }}
  .bl:before {{ content:"•"; color:{B.PINK}; position:absolute; left:0; font-weight:700; }}
  /* SDS */
  .sds-sec {{ background:{B.CHAR}; color:#fff; font-weight:700; font-size:9pt;
    padding:5px 10px; margin:11px 0 0; break-after:avoid; }}
  .sds-sec b {{ color:{B.PINK}; margin-right:6px; }}
  .sds-body {{ padding:6px 2px 0; }}
  .sds-body p {{ margin:0 0 4px; font-size:8pt; color:#333; line-height:1.45; }}
  .sds-body p .lbl {{ font-weight:700; color:{B.CHAR}; }}
  .sds-body p.subh {{ font-weight:700; color:{B.PINK}; font-size:8.3pt; margin:7px 0 2px; }}
  table.clp, table.comp {{ width:100%; border-collapse:collapse; margin:4px 0 6px; }}
  table.clp th, table.comp th {{ background:{B.CHAR}; color:#fff; font-weight:600;
    font-size:7.3pt; text-align:left; padding:4px 7px; border:1px solid #fff; }}
  table.clp td, table.comp td {{ border:1px solid #d8d6dc; padding:3px 7px; font-size:8pt;
    vertical-align:top; }}
  table.clp tr:nth-child(even) td, table.comp tr:nth-child(even) td {{ background:#f4f2f6; }}
  table.clp td.c {{ font-weight:700; color:{B.PINK}; white-space:nowrap; }}
  table.comp td.n {{ font-weight:600; color:{B.CHAR}; }}
  table.kv {{ width:100%; border-collapse:collapse; margin-top:3px; break-inside:auto; }}
  table.kv td {{ border-bottom:1px solid #e6e4ea; padding:2.5px 8px; font-size:8pt;
    vertical-align:top; }}
  table.kv td.k {{ background:#f1eff3; font-weight:600; width:38%; color:{B.CHAR}; }}
  .hazbox {{ display:flex; gap:14px; align-items:center; background:#fdeef5;
    border:1px solid {B.PINK}; border-radius:8px; padding:10px 14px; margin-top:8px; }}
  .hazbox img {{ height:62px; width:62px; }}
  .sds-body p.lab {{ font-weight:700; color:#1a1820; font-size:8.2pt; margin:6px 0 1px; }}
  .sds-body p.val {{ margin:0 0 2.5px 0; font-size:8pt; color:#333; line-height:1.42; }}
  .sds-body p.val.vin {{ margin-left:0; }}
  .sds-body p.pv {{ margin:0 0 3px; font-size:8pt; color:#333; line-height:1.45; }}
  .sds-body b.code {{ color:{B.PINK}; font-weight:700; }}
  .ghsrow {{ margin:3px 0 5px 10px; }}
  .ghsrow img {{ height:1.35cm; width:1.35cm; margin-right:9px; vertical-align:middle; }}
  table.tox {{ width:100%; border-collapse:collapse; margin:4px 0 7px; }}
  table.tox td {{ border:1px solid #d8d6dc; padding:3px 7px; font-size:8pt; vertical-align:top; }}
  table.tox td.e {{ width:36%; font-weight:600; color:{B.CHAR}; background:#f4f2f6; }}
  .fnote {{ margin:1px 0 0; font-size:7.2pt; color:#777; }}
  .hazbox .sig {{ font-weight:700; color:{B.PINK}; font-size:10pt; }}
  /* SDS cover page */
  .cover-haz {{ display:flex; gap:16px; align-items:center; background:{B.CHAR};
    border-radius:12px; padding:16px 20px; margin-top:16px; }}
  .cover-haz img {{ height:78px; width:78px; background:#fff; border-radius:8px; padding:4px; }}
  .cover-haz .sig {{ color:{B.PINK}; font-weight:700; font-size:13pt; letter-spacing:.5px; }}
  .cover-haz .hs {{ color:#fff; font-size:9pt; line-height:1.5; margin-top:5px; }}
  .cover-haz .hs b {{ color:{B.PINK}; }}
  .cover-grid {{ display:flex; gap:16px; margin-top:16px; }}
  .cover-card {{ flex:1; border:1px solid #dcdae0; border-radius:12px; padding:16px 18px; }}
  .cover-card h4 {{ margin:0 0 10px; font-size:8pt; font-weight:700; letter-spacing:.16em;
    text-transform:uppercase; color:{B.PINK}; }}
  .cover-card .r {{ font-size:9pt; color:#333; line-height:1.5; margin:0 0 7px; }}
  .cover-card .r b {{ display:block; font-size:7.5pt; font-weight:700; letter-spacing:.06em;
    text-transform:uppercase; color:{B.CHAR}; margin-bottom:1px; }}
  .cover-card.em {{ border-color:{B.PINK}; background:#fdeef5; }}
  .docmeta {{ display:flex; justify-content:space-between; align-items:center;
    background:{B.CHAR}; color:#fff; border-radius:10px; padding:12px 20px; margin-top:16px; }}
  .docmeta .dm {{ text-align:center; }}
  .docmeta .dm .l {{ font-size:7pt; letter-spacing:.14em; text-transform:uppercase; color:#b9b3c0; }}
  .docmeta .dm .v {{ font-size:10.5pt; font-weight:700; margin-top:2px; }}
  .cover-eyebrow {{ display:inline-block; font-size:8pt; font-weight:700; letter-spacing:.2em;
    text-transform:uppercase; color:{B.PINK}; margin:2px 0 0; }}
  .qa-grid {{ display:flex; gap:12px; margin-top:10px; }}
  .qa {{ flex:1; border:1px solid #e3e1e7; border-left:3px solid {B.PINK}; border-radius:8px;
    padding:11px 13px; font-size:8.5pt; color:#444; line-height:1.45; }}
  .qa b {{ display:block; color:{B.CHAR}; font-size:7.5pt; font-weight:700;
    text-transform:uppercase; letter-spacing:.06em; margin-bottom:4px; }}
</style>"""


def head(title_a, title_b, subtitle, kind="Technical data sheet", show_drop=True):
    drop_img = f'<img src="{B.DROP}" alt="">' if show_drop else ""
    return f"""
  <div class="sidebar"></div>
  <h1 class="tds">{kind}</h1>
  <div class="titlebar">
    <div class="t"><span class="a">{title_a}</span><span class="b">{title_b}</span></div>
    {drop_img}
  </div>
  <p class="lede">{subtitle}</p>"""


def footer(extra_notes):
    notes = "".join(f"<li>{n}</li>" for n in extra_notes)
    return f"""
  <div class="lower">
    <div class="qr">
      <h4>Resin quantity</h4>
      <p>Calculate the exact resin amount with the free Lateral Repairs app.</p>
      <div class="codes">
        <div class="code"><img src="{B.QR_IOS}"><div>iPhone · App&nbsp;Store</div></div>
        <div class="code"><img src="{B.QR_AND}"><div>Android · Google&nbsp;Play</div></div>
      </div>
    </div>
    <div class="notice"><h4>Notice</h4><ul>{notes}</ul></div>
  </div>
  <div class="foot"><div>Issue: V2026.1 · 2026.06</div></div>
  {B.contactbar()}"""


def feature_table2(title, rows):
    body = "".join(
        f'<tr><td class="k2">{(B.ic(ic_)+" " if ic_ else "")}{k}</td><td class="v">{v}</td></tr>'
        for ic_, k, v in rows)
    return f'<table class="f"><tr><td class="hd" colspan="2">{title}</td></tr>{body}</table>'


# ----------------------------------------------------------------- Glassfiber
def glassfiber():
    rows = [
        ("material", "Glass composition", "E-CR Glass"),
        ("weight", "Weight per unit area", "1050 g/m² ± 8 % <span style='color:#777'>(deviation from nominal)</span>"),
        ("textile", "1st layer — Chopped Strand Mat", "500 g/m²"),
        ("textile", "2nd layer — Woven Roving", "Warp 0°: 150 g/m² &nbsp;·&nbsp; Weft 90°: 410 g/m²"),
        ("coating", "Bonding", "Stitching"),
        ("material", "Sewing thread (polyester)", "≤ 15 g/m²"),
        ("resin", "Moisture content", "&lt; 0.15 %"),
        ("thickness", "Edges", "Trimmed"),
        ("length", "Width", "125 cm / 250 cm"),
        ("colour", "Coupling agent", "Silane"),
        ("diameter", "Tube diameter, internal", "70 mm"),
    ]
    body = B.css() + EXTRA_CSS
    body += head("Glassfiber ", "Complex 1050",
                 "E-CR glass-fibre reinforcement complex for structural pipe rehabilitation and CIPP lining.")
    body += feature_table2("Technical data", rows)
    body += """
  <div class="twocard">
    <div class="card"><h4>Processing / Storage</h4>
      <p>The product should be conditioned for 24 hours at room temperature in the application area prior to use.</p>
      <p>Store in its original packaging and keep dry. Storage temperature should not exceed 35 °C.</p></div>
    <div class="card"><h4>Delivery form</h4>
      <p>Rolls are packed in stretch film and supplied on pallets.</p>
      <p>* Other roll widths, tube diameters and lengths available on request.</p></div>
  </div>"""
    body += footer([
        "The information in this data sheet corresponds to our knowledge and experience at the present time and does not constitute legally binding assurance of properties.",
        "Before using the product, check its suitability for the intended application. As processing is beyond our control, responsibility rests solely with the user.",
    ])
    return body


# --------------------------------------------------------------- Connection
def conn_table(title, seam):
    rows = [
        ("Weight", "Approx. 450 g/m²", "DIN EN 29073 T1"),
        ("Thickness with coating", "Approx. 3.0 mm", "DIN EN 29073 T2"),
        ("Pore volume", "Approx. 85 %", "—"),
        ("Fibers", "Polyester", "—"),
        ("Coating", "TPU; PUR", "—"),
        ("Coating thickness", "Approx. 150 μm", "—"),
        ("Seam type", seam, "—"),
        ("Curing", "Ambient, Hot Water, Steam Mix", "—"),
        ("Properties", "DN50 to DN300 · 45°, 90°, 180° connections<br><span style='color:#777'>* other angles on request</span>", "—"),
    ]
    head_row = (f'<tr><td class="hd3" colspan="3">{title}'
                f'<div class="sub">Delivery status · Material data · ISO test method</div></td></tr>')
    body = "".join(
        f'<tr><td class="k">{k}</td><td class="m">{m}</td><td class="t">{t}</td></tr>'
        for k, m, t in rows)
    return f'<table class="f3">{head_row}{body}</table>'


def connection():
    body = B.css() + EXTRA_CSS
    # ---- page 1: product description + illustration ----
    body += head("Connection ", "Liners",
                 "Flexible polyester knitted hose with thermoplastic coating for the rehabilitation of lateral connections.")
    body += B.pagelogo()
    body += """
  <div class="secttl">Product description</div>
  <div class="card" style="margin-top:0;border-top-left-radius:0;border-top-right-radius:0">
    <p class="desc">Lateral Repairs Connection Liner is a flexible and versatile solution for the rehabilitation of non-pressure pipelines, designed to restore lateral connections with precision and reliability. Manufactured from a durable polyester knitted hose with a thermoplastic coating, it is available in sizes ranging from DN50 to DN300, with 45°, 90° and 180° connection options.</p>
    <p class="desc">This proven system is engineered to adapt to a wide range of installation conditions, providing contractors with a dependable solution for junction rehabilitation. For projects requiring unique specifications, custom sizes can also be supplied in consultation with Lateral Repairs.</p>
    <p class="desc">Lateral Repairs Connection Liners combine strength, adaptability and ease of use, making them a trusted solution for extending the service life of pipeline infrastructure.</p>
  </div>
  <figure class="illus">
    <img src="%s" alt="Lateral Repairs connection liner">
    <figcaption>Lateral Repairs Connection Liner — restores lateral / branch connections (45°, 90°, 180°).</figcaption>
  </figure>
  <!-- ---- page 2: technical data ---- -->
  <div class="pagebreak"></div>
  <div class="secttl">Technical data</div>
  <div style="display:flex;gap:14px;margin-top:11px">
    <div style="flex:1">%s</div>
    <div style="flex:1">%s</div>
  </div>""" % (CONN_DIAGRAM,
              conn_table("Stitched &amp; Sealed Connection Liners", "Stitched and sealed"),
              conn_table("Stitched (Not Sealed) Connection Liners", "Stitched"))
    body += footer([
        "The final quality depends on the resin system used, the inversion pressure and the curing pressure. We advise against the use of other resin systems or higher pressures and accept no liability.",
        "All data are guideline values determined under laboratory conditions and can differ on industrial job sites.",
    ])
    return body


# --------------------------------------------------------------- End Cap Glue
def endcap():
    tech = [
        ("curing", "Application temperature", "+10 °C – +40 °C"),
        ("storage", "Using temperature", "min. +5 °C"),
        ("curing", "Temperature resistance", "−40 °C – +75 °C *"),
        ("resin", "Curing time", "5 – 15 min (depending on conditions)"),
        ("length", "Open time", "10 – 40 min"),
        ("weight", "Density", "0,83 g/ml"),
        ("coating", "Dosage", "approx. 4 m² / l"),
        ("colour", "Colour", "Yellowish"),
        ("storage", "Storage stability", "12 months · +5 – +25 °C, dry"),
    ]
    handling = [
        ("material", "Phase", "Slightly yellowish liquid synthetic rubber solution"),
        ("coating", "Tools", "Brush, roller or spray gun"),
        ("weight", "Packaging", "Steel cans · 1, 3, 10, 20, 200, 1000 L"),
        ("resin", "Cleaning", "Acetone (product and tools)"),
        ("undersize", "Environment", "Hazardous-waste disposal; cans recyclable"),
        ("curing", "Fire", "Highly flammable"),
        ("diameter", "Transport", "ADR UN 1133, class 3.1"),
        ("certificate", "Safety", "Harmful — read the SDS before use"),
    ]
    body = B.css() + EXTRA_CSS
    body += head("End Cap ", "Glue",
                 "A solvent-borne, toluene-free, nearly n-hexane-free special contact adhesive for industrial and professional use.")
    body += """
  <div class="card" style="margin-top:0">
    <h4>Suitability</h4>
    <p class="desc" style="margin:0">Flooring, shoe and leather industry, ship, boat and car-chassis building. Very well suited for joining rubber, leather, gasket, floor and wall coverings, sheets, mouldings, metals, woodpiles and different linings and insulations.</p>
  </div>
  <div class="cols" style="margin-top:11px">
    <div class="col">""" + feature_table2("Technical data", tech) + """</div>
    <div class="col">""" + feature_table2("Handling &amp; safety", handling) + """</div>
  </div>
  <div class="card">
    <h4>Operating directions</h4>
    <p>Surfaces must be clean, dry and free from grease and dust; they can be coarse-ground. Apply the adhesive in a thin, smooth layer to both surfaces with a brush or roller — for spray-gun systems it can be diluted with acetone 5–20 %. Let the glue dry 15–40 minutes depending on conditions, then press the surfaces tightly together, checking there are no air bubbles. Over-dried surfaces can be reactivated with heat; if heated, press together while still warm. The bond holds immediately, with full strength developing in about two days. The dried adhesive is freeze-resistant.</p>
    <p style="margin-top:4px">* Heat resistance of the dry seam approx. +75 °C without hardener; with LR1600 hardener (3–10 %), approx. 80–90 °C.</p>
  </div>"""
    body += f"""
  <div class="notice" style="margin-top:11px">
    <h4>Notice</h4>
    <ul>
      <li>Contains hydroactive solvents 15–50 %, ethyl acetate 15–50 %. Highly flammable — store in well-closed cans in a cool, well-ventilated place; the directions for storing and transporting flammable liquids apply.</li>
      <li>Harmful. The product health &amp; safety data sheet (SDS) must be read before use.</li>
      <li>The information in this data sheet corresponds to our knowledge and experience at present and is non-binding; check the product's suitability for your application before use.</li>
    </ul>
  </div>
  <div class="foot"><div>Issue: V2026.1 · 2026.06</div></div>
  {B.contactbar()}"""
    return body


# --------------------------------------------------------------- SDS (vinyl ester)
GHS07 = "data:image/png;base64," + B.b64(os.path.join(HERE, "assets", "ghs_exclamation.png"))


def sec(num, title, content):
    return f'<div class="sds-sec"><b>{num}</b>{title}</div><div class="sds-body">{content}</div>'


def kv(rows):
    body = "".join(f'<tr><td class="k">{k}</td><td>{v}</td></tr>' for k, v in rows)
    return f'<table class="kv">{body}</table>'


def p(label, text):
    return f'<p><span class="lbl">{label}:</span> {text}</p>' if label else f'<p>{text}</p>'


def sds():
    body = B.css() + EXTRA_CSS
    body += head("MFE 7516 ", "Vinyl Ester",
                 "Styrene-free vinyl ester resin — Safety Data Sheet according to Regulation (EC) No. 1272/2008.",
                 kind="Safety data sheet", show_drop=False)
    body += B.pagelogo()

    # ============ COVER PAGE ============
    body += '<div class="cover-eyebrow">Hazard overview · GHS / CLP</div>'
    body += ('<div class="cover-haz"><img src="' + GHS07 + '">'
             '<div><span class="sig">Warning</span>'
             '<div class="hs"><b>H315</b> Causes skin irritation. &nbsp; <b>H317</b> May cause an allergic skin reaction. &nbsp; <b>H319</b> Causes serious eye irritation.<br>'
             '<b>P280</b> Wear protective gloves. &nbsp; <b>P305+P351+P338</b> IF IN EYES: rinse cautiously with water for several minutes; remove contact lenses if easy; continue rinsing.</div></div></div>')

    body += ('<div class="cover-grid">'
             '<div class="cover-card">'
             '<h4>Product identification</h4>'
             '<p class="r"><b>Product</b>MFE 7516 Vinyl Ester (styrene-free)</p>'
             '<p class="r"><b>Product type</b>Environmentally friendly, corrosion-resistant resin</p>'
             '<p class="r"><b>Intended use</b>SU3 Industrial · SU12 Manufacture of plastics · SU22 Professional uses</p>'
             '<p class="r"><b>Stabiliser</b>Mequinol (≥ 180 – ≤ 220 ppm)</p>'
             '</div>'
             '<div class="cover-card em">'
             '<h4>Manufacturer &amp; emergency</h4>'
             '<p class="r"><b>Manufacturer</b>Lateral Repairs UAB<br>Paberžių g. 5, Tauragė, LT-72328, Lithuania</p>'
             '<p class="r"><b>Contact</b>info@lateralrepairs.com · +370 612 12882 · Office +370 698 76581</p>'
             '<p class="r"><b>Emergency telephone</b>+370 612 12882, or your local emergency number</p>'
             '</div></div>')

    body += ('<div class="docmeta">'
             '<div class="dm"><div class="l">Document</div><div class="v">Safety Data Sheet</div></div>'
             '<div class="dm"><div class="l">Regulation</div><div class="v">(EC) No. 1272/2008</div></div>'
             '<div class="dm"><div class="l">Version</div><div class="v">V2026.1</div></div>'
             '<div class="dm"><div class="l">Date of issue</div><div class="v">2026.06</div></div>'
             '</div>')

    body += '<div class="cover-eyebrow" style="margin-top:18px">First aid · quick reference</div>'
    body += ('<div class="qa-grid">'
             '<div class="qa"><b>Eye contact</b>Rinse thoroughly with plenty of water for at least 15 minutes and consult a physician.</div>'
             '<div class="qa"><b>Skin contact</b>Wash off with soap and plenty of water. Consult a physician.</div>'
             '<div class="qa"><b>Inhalation</b>Move to fresh air and keep at rest. Get medical advice if you feel unwell.</div>'
             '<div class="qa"><b>If swallowed</b>Do NOT induce vomiting. Rinse mouth with water. Consult a physician.</div>'
             '</div>')

    body += '<div class="pagebreak"></div>'

    # ============ SECTIONS (page 2+) ============
    body += sec("1.", "Identification",
        p("Product description", "MFE 7516 Vinyl Ester (styrene-free)")
        + p("Intended use", "Environmentally friendly, corrosion-resistant resin. SU3 — Industrial uses; SU12 — Manufacture of plastics products (compounding and conversion); SU22 — Professional uses.")
        + p("Uses advised against", "No information available")
        + p("Manufacturer", "Lateral Repairs UAB · Paberžių g. 5, Tauragė, LT-72328, Lithuania · info@lateralrepairs.com · Phone +370 612 12882 · Office +370 698 76581")
        + p("Emergency telephone", "+370 612 12882, or contact your local emergency telephone number"))

    body += sec("2.", "Hazards identification",
        '<div class="hazbox"><img src="' + GHS07 + '">'
        '<div><div class="sig">Signal word: Warning</div>'
        '<p style="margin:4px 0 0"><b>H315</b> Causes skin irritation. &nbsp; <b>H317</b> May cause an allergic skin reaction. &nbsp; <b>H319</b> Causes serious eye irritation.</p>'
        '<p style="margin:3px 0 0"><b>P280</b> Wear protective gloves. &nbsp; <b>P305+P351+P338</b> IF IN EYES: rinse cautiously with water for several minutes; remove contact lenses if present and easy to do; continue rinsing.</p></div></div>'
        + p("Classification (EC 1272/2008)", "Skin irritation H315 — Category 2; Eye irritation H319 — Category 2; Skin sensitization H317 — Category 1.")
        + p("Classification (67/548/EEC · 1999/45/EC)", "Xi Irritant — R36/38; R43."))

    body += sec("3.", "Composition / information on ingredients",
        p("Type", "Vinyl ester resin, styrene-free")
        + p("Stabiliser", "Mequinol (≥ 180 – ≤ 220 ppm)"))

    body += sec("4.", "First-aid measures",
        p("General advice", "Consult a physician. Show this safety data sheet to the doctor in attendance.")
        + p("If inhaled", "Remove victim to fresh air and keep at rest in a position comfortable for breathing. If not breathing, give artificial respiration. Consult a physician.")
        + p("Skin contact", "Wash off with soap and plenty of water. Consult a physician.")
        + p("Eye contact", "Rinse thoroughly with plenty of water for at least 15 minutes and consult a physician.")
        + p("If swallowed", "Do NOT induce vomiting. Never give anything by mouth to an unconscious person. Rinse mouth with water. Consult a physician."))

    body += sec("5.", "Firefighting measures",
        p("Extinguishing media", "Water spray, alcohol-resistant foam, dry chemical or carbon dioxide.")
        + p("Special hazards", "Carbon oxides, nitrogen oxides (NOx).")
        + p("Advice for firefighters", "Wear self-contained breathing apparatus if necessary. Use water spray to cool unopened containers."))

    body += sec("6.", "Accidental release measures",
        p("Personal precautions", "Wear respiratory protection. Avoid breathing vapours, mist or gas. Ensure adequate ventilation and remove all sources of ignition. Beware of vapours accumulating to form explosive concentrations in low areas.")
        + p("Environmental precautions", "Prevent further leakage or spillage if safe to do so. Do not let product enter drains.")
        + p("Containment / cleaning up", "Contain spillage, then collect with an electrically protected vacuum cleaner or by wet-brushing and place in a container for disposal according to local regulations."))

    body += sec("7.", "Handling and storage",
        p("Safe handling", "Avoid contact with skin and eyes; avoid inhalation of vapour or mist. Keep away from sources of ignition — no smoking. Prevent build-up of electrostatic charge.")
        + p("Storage", "Store in a cool place. Keep container tightly closed in a dry, well-ventilated place; reseal opened containers and keep upright. Recommended storage temperature ≤ 25 °C. Moisture- and light-sensitive."))

    body += sec("8.", "Exposure controls / personal protection",
        p("Exposure limits", "Contains no substances with occupational exposure limit values.")
        + p("Engineering controls", "Avoid contact with skin, eyes and clothing. Wash hands before breaks and immediately after handling.")
        + p("Eye / face", "Face shield and safety glasses tested and approved to NIOSH (US) or EN 166 (EU).")
        + p("Skin", "Protective gloves to EU Directive 89/686/EEC and EN 374; inspect before use.")
        + p("Body", "Complete chemical-protective suit, selected per concentration and amount at the workplace.")
        + p("Respiratory", "Where required, full-face respirator with type ABEK (EN 14387) cartridges; if the sole means of protection, use a supplied-air respirator."))

    body += sec("9.", "Physical and chemical properties",
        kv([("Appearance", "Clear liquid"),
            ("Colour", "Yellow, transparent liquid"),
            ("Odour", "Ester-like"),
            ("pH", "No data available"),
            ("Melting / freezing point", "&lt; −60 °C"),
            ("Boiling point / range", "67 °C at 4,7 hPa (lit.)"),
            ("Flash point", "96 °C — closed cup"),
            ("Vapour pressure", "0,1 hPa at 20 °C"),
            ("Relative density", "1,1 – 1,20 g/mL at 25 °C"),
            ("Partition coeff. (octanol/water)", "log Pow −0,53 at 20 °C"),
            ("Other properties", "No data available")]))

    body += sec("10.", "Stability and reactivity",
        p("Stability", "Contains stabiliser Mequinol. May polymerise on exposure to light.")
        + p("Conditions to avoid", "Exposure to light.")
        + p("Incompatible materials", "Strong acids, strong bases, strong oxidising agents, strong reducing agents.")
        + p("Hazardous decomposition", "No data available."))

    body += sec("11.", "Toxicological information",
        p("Acute toxicity", "LD50 oral, rat: 5050 mg/kg. LD50 dermal, rabbit: &gt; 3 000 mg/kg.")
        + p("Skin / eye", "Skin (rabbit): irritating (24 h). Eyes (rabbit): moderate eye irritation (24 h, Draize).")
        + p("Sensitisation", "May cause sensitisation by skin contact (OECD 406).")
        + p("Carcinogenicity", "IARC: no component ≥ 0,1 % identified as a carcinogen.")
        + p("Reproductive toxicity", "Rat, female, oral — effects on fertility and on embryo/fetus reported."))

    body += sec("12.", "Ecological information",
        p("Toxicity to fish", "Pimephales promelas (fathead minnow): 227 mg/l — 96 h (flow-through).")
        + p("Persistence / degradability", "Readily biodegradable — 84 % (28 d, Closed Bottle test).")
        + p("PBT / vPvB", "Assessment not available (chemical safety assessment not required/conducted)."))

    body += sec("13.", "Disposal considerations",
        p("Waste treatment", "May be burned in a chemical incinerator equipped with an afterburner and scrubber. Offer surplus and non-recyclable material to a licensed disposal company.")
        + p("Contaminated packaging", "Dispose of as unused product."))

    body += sec("14.", "Transport information",
        p("Classification", "ADR/RID, IMDG and IATA: Not dangerous goods.")
        + p("UN number / class / packing group", "None.")
        + p("Environmental hazards", "IMDG marine pollutant: no."))

    body += sec("15.", "Regulatory information",
        p("Labelling", "According to Regulation (EC) No 1272/2008 — see Section 2.")
        + p("Chemical safety assessment", "A Chemical Safety Assessment has not been carried out.")
        + p("Inventory", "EINECS — substance included in the regulations (√)."))

    body += sec("16.", "Other information",
        p("H-statements", "H315 Causes skin irritation. H317 May cause an allergic skin reaction. H319 Causes serious eye irritation.")
        + p("R-phrases", "R36/38 Irritating to eyes and skin. R43 May cause sensitisation by skin contact.")
        + p("", "The above information is believed to be correct but does not purport to be all-inclusive and shall be used only as a guide. It is based on the present state of our knowledge and does not represent any guarantee of the properties of the product."))

    body += '<div class="foot"><div>Safety data sheet · Issue V2026.1 · 2026.06</div></div>'
    body += B.contactbar()
    return body


# --------------------------------------------------------------- Silicate Resin SDSs
import json as _json
import re as _re

GHS = {n: "data:image/png;base64," + B.b64(os.path.join(HERE, "assets", f"{n}_{s}.png"))
       for n, s in (("ghs05", "corrosion"), ("ghs07", "exclamation"), ("ghs08", "health"))}
SILICATE = _json.load(open(os.path.join(HERE, "assets", "silicate_sds.json"), encoding="utf-8"))

# ---- Section 3 composition tables (verbatim from the source SDSs) ----------
COMP_A = [
    ("Silicic acid, sodium salt (Molar ratio Na₂O : SiO₂ = 1 : &gt; 1.6 – &lt; 2.6)",
     "215-687-4", "1344-09-8", "01-2119448725-31", "25–50",
     "Skin Irrit. 2 (H315), Eye Dam. 1 (H318)"),
    ("Water", "231-791-2", "7732-18-5", "—", "50–75", "—"),
]
FOOT_A = ["¹ – See Section 16 for the full text of the abbreviations declared above."]

_BHAZ = ("Acute Tox. 4 (H332), Skin Irrit. 2 (H315), Eye Irrit. 2 (H319), "
         "Resp. Sens. 1 (H334), Skin Sens. 1B (H317), Carc. 2 (H351), "
         "STOT SE 3 (H335), STOT RE 2 (H373)")
_MDI_OLIGO = ("4,4'-Methylenediphenyl diisocyanate, oligomeric reaction products with "
              "2,4'-diisocyanatodiphenylmethane, 2,2'-methylenediphenyl diisocyanate "
              "and α-hydro-ω-hydroxypoly[oxy(methyl-1,2-ethanediyl)]³")
COMP_WINTER = [
    ("Isocyanic acid, polymethylene-polyphenylene ester (Polymeric MDI)²",
     "(polymer)", "9016-87-9", "(polymer)", "&gt; 60", _BHAZ),
    ("Tris(2-chloro-1-methylethyl) phosphate (TCPP)",
     "237-158-7", "13674-84-5", "01-2119486772-26", "&gt; 10", "Acute Tox. 4 (H302)"),
    (_MDI_OLIGO, "951-860-7", "158885-25-7", "(polymer)", "≤ 5", _BHAZ),
]
FOOT_WINTER = [
    "¹ – See Section 16 for the full text of the abbreviations declared above.",
    "² – Contains &lt; 35% 4,4'-MDI (4,4'-methylenediphenyl diisocyanate) (CAS: 101-68-8).",
    "³ – Contains &lt; 10% 4,4'-MDI (4,4'-methylenediphenyl diisocyanate) (CAS: 101-68-8).",
]
COMP_W01 = [
    ("Isocyanic acid, polymethylene-polyphenylene ester (Polymeric MDI)²",
     "(polymer)", "9016-87-9", "(polymer)", "&gt; 60", _BHAZ),
    ("Tris(2-chloro-1-methylethyl) phosphate (TCPP)",
     "237-158-7", "13674-84-5", "01-2119486772-26", "&gt; 10", "Acute Tox. 4 (H302)"),
    (_MDI_OLIGO, "951-860-7", "158885-25-7", "(polymer)", "≤ 10", _BHAZ),
    ("Triisobutyl phosphate", "204-798-3", "126-71-6", "01-2119957118-32", "≤ 10",
     "Skin Sens. 1B (H317)"),
]
FOOT_W01 = [
    "¹ – See Section 16 for the full text of the abbreviations declared above.",
    "² – Contains &lt; 35% 4,4'-MDI (4,4'-methylenediphenyl diisocyanate) (CAS: 101-68-8).",
    "³ – Contains ca. 10% 4,4'-MDI (4,4'-methylenediphenyl diisocyanate) (CAS: 101-68-8).",
]
COMP_BY_SLUG = {"summer": (COMP_A, FOOT_A), "waterglass": (COMP_A, FOOT_A),
                "winter": (COMP_WINTER, FOOT_WINTER), "w01": (COMP_W01, FOOT_W01)}

# supplier block (Section 1.3) — identical for all four, per customer feedback
SUPPLIER_FIELDS = [
    ("Producer/Supplier:", ["UAB Lateral Repairs"]),
    ("Street/POB:", ["Paberziu g. 5"]),
    ("Postcode/City/Country:", ["LT-72328, Taurage, Lithuania"]),
    ("E-mail address for a competent person responsible for the safety data sheet:",
     ["info@lateralrepairs.com"]),
    ("Phone:", ["+370 698 76581"]),
]


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _sq(s):
    """collapse internal whitespace runs and escape"""
    return _esc(_re.sub(r"\s{2,}", " ", s.strip()))


# value text that must NOT be treated as a bold label's start (it is data)
_DATA_START = _re.compile(
    r"^(LC50|LD50|EC50|EC10|IC50|NOEC|NOEL|NOAEC|NOAEL|DNEL|PNEC|BCF|OECD|DIN\b|"
    r"EN\s?\d|ISO\s?\d|CAS\b|[0-9<>=≤≥~±]|ca\.|approx)", _re.I)
_STMT = _re.compile(r"^([HP]\d{3}(?:\s*\+\s*[HP]\d{3})*)\b[.:]?\s+(\S.*)$")
_HEAD = _re.compile(r"^(\d{1,2}(?:\.\d+)+\.?)\s*(.*)$")
_COL_LABEL = _re.compile(r"^(.{1,62}?):\s{2,}(\S.*)$")
_GAP_SPLIT = _re.compile(r"^(.{1,42}?)\s{3,}(\S.*)$")
_BARE_LABEL = _re.compile(r"^(.{1,62}?):$")
_INLINE_LABEL = _re.compile(r"^([A-Z][^:]{1,54}?):\s(\S.*)$")


_SECTION_LABEL_KW = _re.compile(
    r"exposure|DNEL|PNEC|LC50|LD50|EC50|IC50|NOAE|NOEC|OECD|CAS\b|mg/|"
    r"rabbit|rats?\b|guinea|reaction products|isocyanate", _re.I)


def _is_section_label(label):
    """A short descriptive heading (bold) vs a long data descriptor (inline)."""
    return len(label) <= 40 and not _SECTION_LABEL_KW.search(label)


def _norm(s):
    """normalise a heading for matching: lower-case, single spaces, no trailing colon"""
    return _re.sub(r"\s+", " ", s.strip()).rstrip(":").strip().lower()


# Section sub-headings that must always render as bold labels (black), whether
# or not the source gave them a colon and regardless of length.  The EU CLP SDS
# format has a fixed vocabulary of these; listing them keeps the layout uniform
# and avoids over-bolding data descriptors.
_HEADINGS = {_norm(x) for x in [
    "Hazard determining component(s) for labelling",
    "Further information on storage conditions",
    "Occupational exposure controls", "Environmental exposure controls",
    "Unsuitable materials",
    # §11 endpoints
    "Irritation and corrosivity", "Sensitizing effects",
    "Carcinogenic/mutagenic/toxic effects for reproduction",
    "STOT– single exposure", "STOT single exposure", "STOT – single exposure",
    "STOT – repeated exposure", "STOT repeated exposure",
    "Aspiration hazard",
    "Acute toxicity", "Acute toxicity – oral",
    "Acute toxicity – inhalation (aerosol)", "Acute toxicity – dermal",
    "Skin corrosion/Skin irritation", "Eye damage/Irritation",
    "Skin sensitisation", "Respiratory sensitisation", "Effects on fertility",
    # §12 ecotox
    "Short-term toxicity to fish", "Long-term toxicity to fish",
    "Short-term toxicity to aquatic invertebrates",
    "Long-term toxicity to aquatic invertebrates",
    "Toxicity to aquatic algae and cyanobacteria",
    "Toxicity to aquatic plants other than algae",
    "Toxicity to microorganisms", "Toxicity to other aquatic organisms",
    "Toxicity to soil macroorganisms except arthropods",
    "Toxicity to terrestrial arthropods", "Toxicity to terrestrial plants",
    "Toxicity to soil microorganisms", "Toxicity to other above-ground organisms",
    "Phototransformation in air", "Phototransformation in water and soil",
    "Hydrolysis", "Biodegradation in water",
    "Biodegradation in water and sediment", "Biodegradation in soil",
    "Bioaccumulation – aquatic/sediment", "Terrestrial bioaccumulation",
    "Adsorption/desorption", "Volatilisation",
    "Conclusion for the P criterion", "Conclusion for the B criterion",
    "Conclusion for the T criterion", "Secondary poisoning",
    "Hazardous to the aquatic environment (acute)",
    "Hazardous to the aquatic environment (chronic)",
    "Further information",
    # §15 (silicate)
    "EU regulatory information", "Additional information",
    "National regulatory information",
    # §16 glossary
    "H-Phrases", "P-Phrases", "Hazard classes",
]}


def _heading_split(s):
    """If ``s`` is (or begins with) a known heading, return (heading, value)."""
    if _norm(s) in _HEADINGS:
        return (s.strip().rstrip(":").strip(), "")
    m = _re.match(r"^(.{3,70}?):\s+(\S.*)$", s.strip())
    if m and _norm(m.group(1)) in _HEADINGS:
        return (m.group(1).strip(), m.group(2).strip())
    return None


def _add_val(b, s):
    """append a value line; join to the previous when it is a sentence wrap"""
    s = _re.sub(r"\s{2,}", " ", s.strip())
    vals = b["vals"]
    if vals:
        last = vals[-1]
        if (not last.endswith((".", ";", ":")) and
                (s[:1].islower() or last.endswith(("/", ",", "–", "-")))):
            vals[-1] = last + " " + s
            return
    vals.append(s)


def _blocks(lines):
    """Reconstruct the source's two-column layout into typed blocks."""
    blocks, cur = [], None
    for raw in lines:
        if not raw.strip():
            cur = None
            continue
        indent = len(raw) - len(raw.lstrip())
        s = raw.strip()

        # continuation lines in the value column
        if cur is not None and indent >= 20:
            _add_val(cur, s)
            continue

        # a known section heading always renders bold (on its own line),
        # even when the source ran it together with the following value
        if indent <= 10:
            hs = _heading_split(s)
            if hs:
                cur = {"t": "label", "label": hs[0] + ":", "vals": []}
                blocks.append(cur)
                if hs[1]:
                    _add_val(cur, hs[1])
                continue

        # a statement code alone on its line — its text follows on the next
        # (indented) lines, e.g. "P303+P361+P353" then "IF ON SKIN …"
        if _re.match(r"^[HP]\d{3}(?:\s*\+\s*[HP]\d{3})*$", s):
            cur = {"t": "stmt", "label": _re.sub(r"\s*\+\s*", "+", s), "vals": []}
            blocks.append(cur)
            continue

        # H###/P### statement lines
        m = _STMT.match(s)
        if m and len(m.group(1)) <= 20:
            cur = {"t": "stmt", "label": _re.sub(r"\s*\+\s*", "+", m.group(1)),
                   "vals": [_re.sub(r"\s{2,}", " ", m.group(2).strip())]}
            blocks.append(cur)
            continue

        # numbered sub-heading (may carry an inline label/value)
        m = _HEAD.match(s)
        if m and indent <= 6:
            num, rest = m.group(1), m.group(2).strip()
            cm = _COL_LABEL.match(rest)
            gm = _GAP_SPLIT.match(rest)
            im = _INLINE_LABEL.match(rest)
            if cm:
                cur = {"t": "head", "label": f"{num} {cm.group(1)}:", "vals": []}
                blocks.append(cur)
                _add_val(cur, cm.group(2))
            elif gm:
                cur = {"t": "head", "label": f"{num} {gm.group(1)}", "vals": []}
                blocks.append(cur)
                _add_val(cur, gm.group(2))
            elif im and len(im.group(1).split()) <= 8:
                cur = {"t": "head", "label": f"{num} {im.group(1)}:", "vals": []}
                blocks.append(cur)
                _add_val(cur, im.group(2))
            else:
                cur = {"t": "head", "label": f"{num} {rest}".strip(), "vals": []}
                blocks.append(cur)
            continue

        # orphan tail of a wrapped heading (e.g. "Marpol and the IBC Code   Not relevant")
        if (cur is not None and cur["t"] == "head" and not cur["vals"] and indent <= 6
                and ":" not in s
                and not cur["label"].rstrip().endswith((".", ":"))):
            gm = _GAP_SPLIT.match(s)
            if gm and len(gm.group(1)) <= 32:
                cur["label"] = cur["label"].rstrip() + " " + gm.group(1).strip()
                _add_val(cur, gm.group(2))
                continue
            if len(s) <= 30 and ":" not in s and not s.endswith("."):
                cur["label"] = cur["label"].rstrip() + " " + s
                continue

        # columnar "Label:   value"
        m = _COL_LABEL.match(s)
        if m and indent <= 14:
            label, val = m.group(1).strip(), m.group(2).strip()
            # a label that begins lower-case is a wrapped continuation of the
            # previous line's lead (e.g. "Waste disposal number of waste" +
            # "from residues/unused products:") — rejoin them into one label
            forced = False
            if (label[:1].islower() and blocks and blocks[-1]["t"] == "para"
                    and len(blocks[-1]["vals"]) == 1
                    and not blocks[-1]["vals"][-1].rstrip()
                            .endswith((".", ";", ":", "!", "?"))):
                label = blocks.pop()["vals"][0].rstrip() + " " + label
                forced = True
            if forced or (indent <= 2 and _is_section_label(label)):
                cur = {"t": "label", "label": label + ":", "vals": []}
                blocks.append(cur)
                _add_val(cur, val)
            else:
                cur = {"t": "sub", "label": label + ":", "vals": []}
                blocks.append(cur)
                _add_val(cur, val)
            continue

        # bare "Label:" line
        m = _BARE_LABEL.match(s)
        if m and indent <= 14 and len(s) <= 96:
            # merge a single wrapped lead paragraph that ended without
            # punctuation (only one accumulated line — never a real list)
            if (cur is not None and cur["t"] == "para" and len(cur["vals"]) == 1
                    and not cur["vals"][-1].rstrip().endswith((".", ";", ":", "!", "?"))):
                cur["t"] = "label"
                cur["label"] = cur["vals"].pop() + " " + s
                if "raw" in cur:
                    del cur["raw"]
                cur["vals"] = []
                continue
            is_lab = indent <= 2 and _is_section_label(s[:-1])
            cur = {"t": "label" if is_lab else "sub", "label": s, "vals": []}
            blocks.append(cur)
            continue

        # columnar two-part line without a colon (species/data rows)
        m = _GAP_SPLIT.match(s)
        if m and indent <= 16:
            cur = {"t": "sub", "label": m.group(1).strip(), "vals": []}
            blocks.append(cur)
            _add_val(cur, m.group(2))
            continue

        # single-space "Label: value" (only when the value is not data-like)
        m = _INLINE_LABEL.match(s)
        if (m and indent <= 8 and len(m.group(1).split()) <= 8
                and _is_section_label(m.group(1).strip())
                and not _DATA_START.match(m.group(2))):
            cur = {"t": "label", "label": m.group(1).strip() + ":", "vals": []}
            blocks.append(cur)
            _add_val(cur, m.group(2))
            continue

        # a flush-left line that continues the previous field's value (the
        # source wrapped it back to column 0) — rejoin rather than scatter it
        if (blocks and blocks[-1]["t"] in ("label", "head", "sub") and blocks[-1]["vals"]
                and s[:1].islower()
                and not blocks[-1]["vals"][-1].rstrip().endswith((".", ";", ":", "!", "?"))):
            _add_val(blocks[-1], s)
            cur = blocks[-1]
            continue

        # plain paragraph line
        if cur is not None and cur["t"] == "para":
            if cur["raw"] >= 85:
                cur["vals"][-1] += " " + _re.sub(r"\s{2,}", " ", s)
            else:
                cur["vals"].append(_re.sub(r"\s{2,}", " ", s))
            cur["raw"] = len(raw)
        else:
            cur = {"t": "para", "vals": [_re.sub(r"\s{2,}", " ", s)], "raw": len(raw)}
            blocks.append(cur)
    return blocks


def _render_blocks(blocks, after_label_hook=None):
    html = ""
    for b in blocks:
        t = b["t"]
        if t == "head":
            html += f'<p class="subh">{_esc(b["label"])}</p>'
            if b["vals"]:
                html += f'<p class="val">{_esc(" ".join(b["vals"]))}</p>'
        elif t == "label":
            html += f'<p class="lab">{_esc(b["label"])}</p>'
            if after_label_hook:
                html += after_label_hook(b["label"])
            # a field value is one flowing paragraph — join wrapped lines so the
            # text is not scattered across several indented fragments
            if b["vals"]:
                html += f'<p class="val">{_esc(" ".join(b["vals"]))}</p>'
        elif t == "sub":
            # a data descriptor line ("… (inhalation): DNEL = 0.1 mg/m³") renders
            # flush-left as a paragraph so lists such as the DNEL/PNEC block are
            # uniformly left-aligned rather than alternating indent
            joined = (b["label"] + " " + " ".join(b["vals"])) if b["vals"] else b["label"]
            html += f'<p class="pv">{_esc(joined)}</p>'
        elif t == "stmt":
            txt = " ".join(b["vals"])
            html += f'<p class="val"><b class="code">{b["label"]}</b> {_esc(txt)}</p>'
        else:
            for v in b["vals"]:
                html += f'<p class="pv">{_esc(v)}</p>'
    return html


def _tox_table(blocks):
    """Section 11: two-column data table like the original document."""
    html, rows = "", []

    def flush():
        nonlocal html, rows
        if rows:
            html += '<table class="tox">' + "".join(rows) + "</table>"
            rows = []

    for b in blocks:
        t = b["t"]
        if t in ("label", "sub"):
            ind = ' style="padding-left:16px;font-weight:400"' if t == "sub" else ""
            cell = "<br>".join(_esc(v) for v in b["vals"]) or "—"
            rows.append(f'<tr><td class="e"{ind}>{_esc(b["label"])}</td><td>{cell}</td></tr>')
        elif t == "head":
            flush()
            html += f'<p class="subh">{_esc(b["label"])}</p>'
            if b["vals"]:
                html += f'<p class="val">{_esc(" ".join(b["vals"]))}</p>'
        else:
            # a species/endpoint data line whose source used a single-space
            # colon escaped the two-column layout (e.g. W01 §11.6 "Rats
            # (inhalation): NOAEL = …") — fold it back in as a table row so it
            # matches the aligned tables (§11.5, §11.8)
            first = b["vals"][0] if b.get("vals") else ""
            m = _re.match(r"^([A-Z][^:]{1,40}?):\s+(\S.*)$", first)
            if m and _DATA_START.match(m.group(2)):
                cell = "<br>".join([_esc(m.group(2))] + [_esc(v) for v in b["vals"][1:]])
                rows.append('<tr><td class="e" style="padding-left:16px;'
                            f'font-weight:400">{_esc(m.group(1))}:</td><td>{cell}</td></tr>')
            else:
                flush()
                html += _render_blocks([b])
    flush()
    return html


def _sec_shell(num, title, inner):
    return (f'<div class="sds-sec"><b>{num}.</b>{_esc(title)}</div>'
            f'<div class="sds-body">{inner}</div>')


def _sec1(d, c, sec):
    # product identifier from the source (line after the 1.1 heading)
    prod = ""
    lines = sec["lines"]
    for i, ln in enumerate(lines):
        if _re.match(r"^\s*1\.1\.", ln):
            for nx in lines[i + 1:]:
                if nx.strip():
                    prod = _sq(nx)
                    break
            break
    prod = prod or _esc(f'{d["title_a"]} {d["title_b"].replace(" · ", " ")}')
    inner = '<p class="subh">1.1. Product identifier</p>'
    inner += f'<p class="val">{prod}</p>'
    inner += ('<p class="subh">1.2. Relevant identified uses of the substance or '
              'mixture and uses advised against</p>')
    inner += f'<p class="val">{_esc(c["use"])}</p>'
    inner += '<p class="subh">1.3. Details of the supplier of the safety data sheet</p>'
    for lab, vals in SUPPLIER_FIELDS:
        inner += f'<p class="lab">{_esc(lab)}</p>'
        for v in vals:
            inner += f'<p class="val">{_esc(v)}</p>'
    inner += '<p class="subh">1.4. Emergency telephone number</p>'
    emer = c["emergency"]
    if "Tel.:" in emer:
        place, tel = emer.split("Tel.:", 1)
        inner += f'<p class="val">{_esc(place.strip())}</p>'
        inner += f'<p class="val">Tel.: {_esc(tel.strip())}</p>'
    else:
        inner += f'<p class="val">{_esc(emer)}</p>'
    return _sec_shell(sec["num"], sec["title"], inner)


def _sec2(d, c, sec):
    inner = '<p class="subh">2.1. Classification of the substance or mixture</p>'
    inner += '<p class="pv">Classification according to Regulation (EC) No 1272/2008 (CLP):</p>'
    if sec.get("class_table"):
        body = "".join(
            f'<tr><td>{_esc(cl)}</td><td class="c">{code}</td><td>{_esc(st)}.</td></tr>'
            for cl, code, st in sec["class_table"])
        inner += ('<table class="clp"><tr><th>Hazard class / category</th><th>Code</th>'
                  f'<th>Hazard statement</th></tr>{body}</table>')
    # rest of the section from the 2.2 marker onward
    rest = []
    for i, ln in enumerate(sec["lines"]):
        if _re.match(r"^\s*2\.2\.", ln):
            rest = sec["lines"][i:]
            break
    # keep "Hazard pictograms:" as its own label (a blank line resets the
    # block parser so the preceding "Labelling ..." lead is not merged in)
    split_rest = []
    for ln in rest:
        if ln.strip().lower() == "hazard pictograms:":
            split_rest.append("")
        split_rest.append(ln)
    rest = split_rest
    pics = "".join(f'<img src="{GHS[p]}">' for p in c["pictos"])

    def hook(label):
        if label.lower().startswith("hazard pictograms"):
            return f'<div class="ghsrow">{pics}</div>'
        return ""

    inner += _render_blocks(_blocks(rest), after_label_hook=hook)
    return _sec_shell(sec["num"], sec["title"], inner)


def _sec3(d, sec, slug):
    comp, foots = COMP_BY_SLUG[slug]
    # per customer feedback the sub-heading is numbered 3.1.
    inner = '<p class="subh">3.1. Mixtures</p>'
    inner += '<p class="lab">Chemical characterization</p>'
    body = "".join(
        f'<tr><td class="n">{name}</td><td>{ec}</td><td>{cas}</td>'
        f'<td>{reach}</td><td>{content}</td><td>{cls}</td></tr>'
        for name, ec, cas, reach, content, cls in comp)
    inner += ('<table class="comp"><tr><th>Substance</th><th>EC No.</th><th>CAS No.</th>'
              '<th>REACH Reg. No.</th><th>Content (%)</th><th>Classification (CLP)¹</th></tr>'
              f'{body}</table>')
    for f in foots:
        inner += f'<p class="fnote">{f}</p>'
    return _sec_shell(sec["num"], sec["title"], inner)


def _sec9(sec):
    lines = sec["lines"]
    kv, head_lines, tail_lines = [], [], []
    seen_kv = False
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        indent = len(raw) - len(raw.lstrip())
        m = _re.match(r"^\s*[a-z]\)\s+(.+?):\s*(.*)$", raw)
        if m:
            kv.append([_sq(m.group(1)), _re.sub(r"\s{2,}", " ", m.group(2).strip())])
            seen_kv = True
        elif seen_kv and indent >= 20 and kv and not tail_lines:
            kv[-1][1] = (kv[-1][1] + " " + _re.sub(r"\s{2,}", " ", s)).strip()
        elif not seen_kv:
            head_lines.append(raw)
        else:
            tail_lines.append(raw)
    inner = _render_blocks(_blocks(head_lines))
    if kv:
        body = "".join(f'<tr><td class="k">{k}</td><td>{_esc(v) if v else "—"}</td></tr>'
                       for k, v in kv)
        inner += f'<table class="kv">{body}</table>'
    inner += _render_blocks(_blocks(tail_lines))
    return _sec_shell(sec["num"], sec["title"], inner)


_SILICATE_SUBST = ("Silicic acid, sodium salt "
                   "(Molar ratio Na₂O : SiO₂ = 1 : &gt; 1.6 – &lt; 2.6) · CAS 1344-09-8")

# W01 embedded ingredient tables (§11) — reconstructed verbatim from the source
_ING_IRRIT = (
    '<table class="clp"><tr><th>Ingredient name</th><th>Result</th><th>Species</th>'
    '<th>Score</th><th>Exposure</th><th>Test</th></tr>'
    '<tr><td>Triisobutyl phosphate (CAS: 126-71-6)</td><td>Skin erythema/eschar</td>'
    '<td>Rabbit</td><td>0.67</td><td>–</td>'
    '<td>OECD 404 Acute Dermal Irritation/Corrosion</td></tr></table>')
_ING_SENS = (
    '<table class="clp"><tr><th>Ingredient name</th><th>Route of exposure</th>'
    '<th>Species</th><th>Result</th><th>Test description</th></tr>'
    '<tr><td>Triisobutyl phosphate (CAS: 126-71-6)</td><td>Skin</td>'
    '<td>Guinea pig</td><td>Sensitizing</td><td>OECD 406 Skin Sens.</td></tr></table>')


def _sec11_silicate(sec):
    inner = '<p class="subh">11.1. Information on toxicological effects</p>'
    inner += '<p class="lab">Acute toxicity</p>'
    inner += ('<p class="val">Based on available data, the classification criteria '
              'are not met.</p>')
    inner += f'<p class="val">{_SILICATE_SUBST}</p>'
    inner += ('<table class="clp"><tr><th>Exposure route</th><th>Dose</th>'
              '<th>Species</th><th>Source</th></tr>'
              '<tr><td>oral</td><td>LD50 &gt; 2000 mg/kg</td><td>Rat</td><td>IUCLID</td></tr>'
              '<tr><td>dermal</td><td>LD50 &gt; 5000 mg/kg</td><td>Rat</td><td>IUCLID</td></tr>'
              '</table>')
    ncm = "Based on available data, the classification criteria are not met."
    endpoints = [
        ("Irritation and corrosivity", "Causes skin irritation.<br>Causes serious eye damage."),
        ("Sensitizing effects", ncm),
        ("Carcinogenic/mutagenic/toxic effects for reproduction", ncm),
        ("STOT – single exposure", ncm),
        ("STOT – repeated exposure", ncm),
        ("Aspiration hazard", ncm),
    ]
    inner += '<table class="tox">' + "".join(
        f'<tr><td class="e">{_esc(k)}</td><td>{v}</td></tr>' for k, v in endpoints
    ) + "</table>"
    return _sec_shell(sec["num"], sec["title"], inner)


def _sec11_mdi(sec, slug):
    lines = sec["lines"]
    # replace the embedded "Ingredient name" mini-tables with proper HTML tables
    segs, cur, tables = [], [], iter([_ING_IRRIT, _ING_SENS])
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("Ingredient name"):
            segs.append(("text", cur)); cur = []
            j = i + 1
            while j < len(lines):
                sj = lines[j].strip()
                if not sj:
                    j += 1; continue
                if _heading_split(sj) or (_HEAD.match(sj) and _re.match(r"^\d", sj)):
                    break
                j += 1
            try:
                segs.append(("html", next(tables)))
            except StopIteration:
                pass
            i = j
            continue
        cur.append(lines[i]); i += 1
    segs.append(("text", cur))
    html = ""
    for kind, payload in segs:
        if kind == "html":
            html += payload
        elif any(x.strip() for x in payload):
            html += _tox_table(_blocks(payload))
    return _sec_shell(sec["num"], sec["title"], html)


def _sec11(sec, slug):
    if slug in ("summer", "waterglass"):
        return _sec11_silicate(sec)
    return _sec11_mdi(sec, slug)


_ECO_RECORD = _re.compile(
    r"(mg/l|mg/kg|mg/m|g/m|µg/l|µmol|ppm|\(\s*\d|OECD\s+Guideline|OECD\s+\d|"
    r"DIN\s|EN\s?\d|ISO\s?\d|Method:|Half-life|Target organs|CAS[:\s]?\s*\d|"
    r"Guideline\s+\d|BCF\b|DT50)", _re.I)


def _render_eco(lines):
    """Ecotoxicology (§12) for the MDI resins: bold headings, one flowing
    paragraph per prose value, and measurement records kept line-per-line."""
    html, buf = "", []

    def flush():
        nonlocal html, buf
        if buf:
            html += f'<p class="pv">{_esc(" ".join(buf))}</p>'
            buf = []

    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        indent = len(raw) - len(raw.lstrip())
        if _HEAD.match(s) and indent <= 6 and _re.match(r"^\d", s):
            flush()
            m = _HEAD.match(s)
            html += f'<p class="subh">{_esc((m.group(1) + " " + m.group(2)).strip())}</p>'
            continue
        hs = _heading_split(s) if indent <= 10 else None
        if hs:
            flush()
            html += f'<p class="lab">{_esc(hs[0])}</p>'
            if hs[1]:
                buf = [hs[1]]
            continue
        s = _re.sub(r"\s{2,}", " ", s)
        # a measurement record is a short stand-alone data line; a long
        # sentence that merely mentions a unit (e.g. "…10000 mg/l, …") is prose
        if _ECO_RECORD.search(s) and len(s) <= 90:
            flush()
            html += f'<p class="val">{_esc(s)}</p>'
            continue
        buf.append(s)
    flush()
    return html


def _sec12_silicate(sec):
    lines = sec["lines"]
    inner = ('<p class="pv">The data refer to the product with the given composition '
             'and were used cross-referenced.</p>')
    inner += '<p class="subh">12.1. Toxicity</p>'
    inner += '<p class="val">The product has not been tested.</p>'
    inner += f'<p class="val">{_SILICATE_SUBST}</p>'
    inner += ('<table class="clp"><tr><th>Aquatic toxicity</th><th>Dose</th>'
              '<th>Time</th><th>Species</th><th>Source</th></tr>'
              '<tr><td>Acute fish toxicity</td><td>LC50 1108 mg/l</td><td>96 h</td>'
              '<td>Brachydanio rerio (zebrafish)</td><td>IUCLID</td></tr>'
              '<tr><td>Acute algae toxicity</td><td>ErC50 207 mg/l</td><td>72 h</td>'
              '<td>Scenedesmus subspicatus</td><td>IUCLID</td></tr>'
              '<tr><td>Acute crustacea toxicity</td><td>EC50 1700 mg/l</td><td>48 h</td>'
              '<td>Daphnia magna (big water flea)</td><td>IUCLID</td></tr></table>')
    # 12.2 onward (skip the blank separator line after the table)
    rest = []
    started = False
    for ln in lines:
        if _re.match(r"^\s*12\.2\.", ln):
            started = True
        if started:
            rest.append(ln)
    inner += _render_blocks(_blocks(rest))
    return _sec_shell(sec["num"], sec["title"], inner)


def _sec12(sec, slug):
    if slug in ("summer", "waterglass"):
        return _sec12_silicate(sec)
    return _sec_shell(sec["num"], sec["title"], _render_eco(sec["lines"]))


_ABBR_RE = _re.compile(r"^([^:]{1,16}):\s+(\S.*)$")
_CODE_RE = _re.compile(r"^([HP]\d{3}(?:\s*\+\s*[HP]\d{3})*)\s+(\S.*)$")


def _sec16(sec):
    """Section 16: clean two-column glossary tables for the abbreviations and
    the full text of H/P phrases and hazard classes."""
    lines = sec["lines"]
    html = ""
    state = None            # None | "abbr" | "code"
    abbr_rows, code_rows = [], []

    def flush_abbr():
        nonlocal html, abbr_rows
        if abbr_rows:
            html += '<table class="kv">' + "".join(
                f'<tr><td class="k">{_esc(a)}</td><td>{_esc(t)}</td></tr>'
                for a, t in abbr_rows) + "</table>"
            abbr_rows = []

    def flush_code():
        nonlocal html, code_rows
        if code_rows:
            html += '<table class="kv">' + "".join(
                f'<tr><td class="k">{_esc(a)}</td><td>{_esc(t)}</td></tr>'
                for a, t in code_rows) + "</table>"
            code_rows = []

    buf = []

    def flush_buf():
        nonlocal html, buf
        if buf:
            html += f'<p class="pv">{_esc(" ".join(buf))}</p>'
            buf = []

    for raw in lines:
        s = raw.strip()
        indent = len(raw) - len(raw.lstrip())
        if not s:
            continue
        # numbered sub-heading
        m = _HEAD.match(s)
        if m and _re.match(r"^\d", s) and indent <= 6:
            flush_buf(); flush_abbr(); flush_code()
            title = (m.group(1) + " " + m.group(2)).strip()
            html += f'<p class="subh">{_esc(title)}</p>'
            state = "abbr" if s.startswith("16.2") else None
            continue
        # H/P-phrase and hazard-class group headers
        if _norm(s) in {"h-phrases", "p-phrases", "hazard classes"}:
            flush_buf(); flush_abbr(); flush_code()
            html += f'<p class="lab">{_esc(s)}</p>'
            state = "code"
            continue
        if state == "abbr":
            am = _ABBR_RE.match(s)
            if am:
                abbr_rows.append((am.group(1).strip(), am.group(2).strip()))
                continue
        if state == "code":
            cm = _CODE_RE.match(s)
            if cm:
                code_rows.append((cm.group(1).replace(" ", ""), cm.group(2).strip()))
                continue
            gm = _GAP_SPLIT.match(s)
            if gm and indent <= 2:
                code_rows.append((gm.group(1).strip(), gm.group(2).strip()))
                continue
            if code_rows and indent >= 8:      # wrapped continuation of last text
                a, t = code_rows[-1]
                code_rows[-1] = (a, (t + " " + s).strip())
                continue
        # plain prose (intro, "16.1" value, etc.)
        buf.append(_re.sub(r"\s{2,}", " ", s))
    flush_buf(); flush_abbr(); flush_code()
    return _sec_shell(sec["num"], sec["title"], html)


def render_silicate(slug):
    d = SILICATE[slug]
    c = d["cover"]
    body = B.css() + EXTRA_CSS
    use_short = c["use"].replace("“", '"').replace("”", '"')
    body += head(d["title_a"] + " ", d["title_b"], use_short[:150],
                 kind="Safety data sheet", show_drop=False)
    body += B.pagelogo()

    # ---- cover ----
    pics = "".join(f'<img src="{GHS[p]}">' for p in c["pictos"])
    hlist = " &nbsp; ".join(f'<b>{code}</b> {_esc(desc)}.' for code, desc in c["hstatements"])
    plist = " &nbsp; ".join(f'<b>{code}</b> {_esc(desc)}' for code, desc in c["pstatements"][:4])
    body += '<div class="cover-eyebrow">Hazard overview · GHS / CLP</div>'
    body += (f'<div class="cover-haz">{pics}'
             f'<div><span class="sig">{_esc(c["signal"])}</span>'
             f'<div class="hs">{hlist}<br>{plist}</div></div></div>')

    body += ('<div class="cover-grid">'
             '<div class="cover-card"><h4>Product identification</h4>'
             f'<p class="r"><b>Product</b>{_esc(d["title_a"])} {_esc(d["title_b"].replace(" · ", " "))}</p>'
             f'<p class="r"><b>Identified use</b>{_esc(use_short)}</p></div>'
             '<div class="cover-card em"><h4>Manufacturer &amp; emergency</h4>'
             '<p class="r"><b>Manufacturer</b>UAB Lateral Repairs<br>Paberžių g. 5, Tauragė, LT-72328, Lithuania</p>'
             f'<p class="r"><b>Contact</b>info@lateralrepairs.com · {_esc(c["phone"])}</p>'
             f'<p class="r"><b>Emergency</b>{_esc(c["emergency"])}</p></div></div>')

    m = c["meta"]
    body += ('<div class="docmeta">'
             '<div class="dm"><div class="l">Document</div><div class="v">Safety Data Sheet</div></div>'
             '<div class="dm"><div class="l">Regulation</div><div class="v">1907/2006 · 2015/830</div></div>'
             f'<div class="dm"><div class="l">Version</div><div class="v">{_esc(m["version"] or "1.0 / EN")}</div></div>'
             f'<div class="dm"><div class="l">Date of issue</div><div class="v">{_esc(m["issue"] or "01/06/2020")}</div></div>'
             '</div>')
    body += '<div class="pagebreak"></div>'

    # ---- 16 sections ----
    for sec in d["sections"]:
        n = sec["num"]
        if n == 1:
            body += _sec1(d, c, sec)
        elif n == 2:
            body += _sec2(d, c, sec)
        elif n == 3:
            body += _sec3(d, sec, slug)
        elif n == 9:
            body += _sec9(sec)
        elif n == 11:
            body += _sec11(sec, slug)
        elif n == 12:
            body += _sec12(sec, slug)
        elif n == 16:
            body += _sec16(sec)
        else:
            body += _sec_shell(n, sec["title"], _render_blocks(_blocks(sec["lines"])))

    body += (f'<div class="foot"><div>Safety data sheet · Version '
             f'{_esc(m["version"] or "1.0 / EN")} · Issued {_esc(m["issue"] or "01/06/2020")}</div></div>')
    body += B.contactbar()
    return body


# --------------------------------------------------------------- Calibration hose
CAL_SUBTITLE = ("PVC-coated polyester fabric with an ultra-flexible high-frequency overlap "
                "welded seam — suitable for use with most resin types "
                "(Polyester, Vinyl Ester, Epoxy).")

# storage / handling text is identical across the three variants (verbatim from source)
CAL_STORAGE = [
    ("curing", "Avoid extremes of temperature", [
        "Freezing may cause the coating structure to degrade locally, especially areas where the "
        "coating is in tension or compression – at bends and edges, and immediately adjacent to seam welds.",
        "Recommended storage temperature 5 °C – 35 °C.",
        "Shelf life at this temperature: in excess of 1 year."]),
    ("resin", "Recommended humidity", [
        "Very high relative humidity (especially at high temperature such as tropical countries) "
        "could affect the pigmentation of the hose.",
        "Recommended storage humidity 25 % – 65 % rh.",
        "Shelf life at 65 %, 35 °C: 1 year."]),
    ("storage", "Avoid prolonged wet storage", [
        "As with high humidity, the coating is more susceptible to degradation at higher "
        "temperatures, and even further susceptible if the pH of liquid in contact is "
        "significantly above or below 7.",
        "Wet storage is not recommended."]),
    ("colour", "Avoid sunlight / UV", [
        "Prolonged exposure to ultraviolet light can affect the pigmentation of the hose."]),
]
CAL_FURTHER = [
    "All hose supplied is recommended as single use only. Multiple use of the material is at customer risk.",
    "When in use, the hose is to be supported outside the pipe.",
    "Due to sizing requirements at manufacture, the customer must specify the intended use as "
    "calibration hose or pre-liner.",
]
CAL_HANDLING = ("Ensure that the hose is not placed directly onto grit or gravel floor – sweep and "
                "cover the floor first. Handle the hose with care. Ensure personnel are instructed "
                "not to walk on the hose.")

CAL_HOSE = {
    "stitched_welded": {
        "file": "LR_Calibration_Hose_Stitched_Welded.pdf",
        "title_b": "Stitched &amp; Welded",
        "material": "Stitched &amp; Welded HD — Transparent",
        "seam": "High-frequency overlap welded and stitched seam (heavy duty).",
        "lengths": "Standard roll lengths 50 m, 100 m",
        "temp": "80 °C",
        "pressures": [("100", "2.00"), ("125", "2.00"), ("150", "2.00"), ("200", "2.00"),
                      ("225", "1.60"), ("250", "1.20"), ("300", "1.20")],
        "version": "1", "date": "11.02.24",
    },
    "heat_welded": {
        "file": "LR_Calibration_Hose_Heat_Welded_MD.pdf",
        "title_b": "Welded",
        "material": "Welded MD — Transparent",
        "seam": "Heat-welded, overlapped and taped seam (medium duty).",
        "lengths": "Standard roll lengths 50 m, 100 m",
        "temp": "50 °C",
        "pressures": [("50", "2.00"), ("70", "1.80"), ("100", "1.50"), ("125", "1.25"),
                      ("150", "1.00"), ("200", "0.75"), ("225", "0.68"), ("250", "0.60"),
                      ("300", "0.50")],
        "version": "001", "date": "11.02.24",
    },
    "welded_violet": {
        "file": "LR_Calibration_Hose_Welded_Violet.pdf",
        "title_b": "Welded · Violet",
        "material": "Welded HF LD — Violet",
        "seam": "High-frequency overlap welded seam (light duty).",
        "lengths": "Standard roll lengths 50 m, 100 m",
        "temp": "50 °C",
        "pressures": [("50", "0.80"), ("70", "0.68"), ("100", "0.55"), ("125", "0.51"),
                      ("150", "0.47"), ("200", "0.45"), ("225", "0.44"), ("250", "0.42"),
                      ("300", "0.40")],
        "version": "001", "date": "11.02.24",
    },
}


def _cal_kv(rows):
    body = "".join(
        f'<tr><td class="k2">{(B.ic(i) + " " if i else "")}{k}</td><td class="v">{v}</td></tr>'
        for i, k, v in rows)
    return f'<table class="f">{body}</table>'


def _cal_pressure(rows):
    diam = "".join(f'<td style="text-align:center;font-weight:600">{d}</td>' for d, _ in rows)
    pres = "".join(f'<td style="text-align:center">{p}</td>' for _, p in rows)
    return ('<table class="comp" style="margin-top:9px">'
            f'<tr><th style="text-align:left;white-space:nowrap">Pipe diameter (mm)</th>{diam}</tr>'
            '<tr><th style="text-align:left;white-space:nowrap">'
            f'Maximum recommended pressure (Bar)</th>{pres}</tr></table>')


def calibration_hose(key):
    d = CAL_HOSE[key]
    body = B.css() + EXTRA_CSS
    body += head("Calibration Hose ", d["title_b"], CAL_SUBTITLE)

    mat_rows = [
        ("material", "Material", d["material"]),
        ("coating", "Base fabric", "PVC-coated polyester"),
        ("textile", "Seam", d["seam"]),
        ("certificate", "Compatible resins", "Polyester · Vinyl Ester · Epoxy"),
    ]
    if d["lengths"]:
        mat_rows.append(("length", "Standard lengths", d["lengths"]))
    mat_rows.append(("curing", "Maximum working temperature", d["temp"]))

    stor_rows = [(ic_, k, "".join(f'<div class="bl">{p}</div>' for p in ps))
                 for ic_, k, ps in CAL_STORAGE]

    body += '<div class="secttl">Material &amp; construction</div>'
    body += _cal_kv(mat_rows)
    body += '<div class="secttl">Maximum recommended pressure</div>'
    body += _cal_pressure(d["pressures"])
    body += '<div class="secttl">Recommended storage</div>'
    body += _cal_kv(stor_rows)

    further = "".join(f"<li>{n}</li>" for n in CAL_FURTHER)
    body += ('<div class="twocard" style="margin-top:11px">'
             '<div class="card"><h4>Recommended handling</h4>'
             f'<p><b>Mechanical damage to be avoided.</b> {CAL_HANDLING}</p></div>'
             '<div class="card"><h4>Further recommendations</h4>'
             f'<ul style="margin:0;padding-left:14px">{further}</ul></div></div>')

    body += ('<div class="notice" style="margin-top:11px"><h4>Notice</h4><ul>'
             '<li>The information in this data sheet corresponds to our knowledge and experience at '
             'present and is given without warranty; check the product’s suitability for the '
             'intended application before use.</li>'
             '<li>All values are guideline figures determined under laboratory conditions and can '
             'differ on industrial job sites.</li></ul></div>')
    body += (f'<div class="foot"><div>Version {d["version"]} · {d["date"]}</div>'
             '<div>Issue: V2026.1 · 2026.06</div></div>')
    body += B.contactbar()
    return body


def main():
    jobs = [("LR_Glassfiber_Complex_1050.pdf", glassfiber()),
            ("LR_Connection_Liners.pdf", connection()),
            ("LR_End_Cap_Glue.pdf", endcap()),
            ("LR_Calibration_Hose_Stitched_Welded.pdf", calibration_hose("stitched_welded")),
            ("LR_Calibration_Hose_Heat_Welded_MD.pdf", calibration_hose("heat_welded")),
            ("LR_Calibration_Hose_Welded_Violet.pdf", calibration_hose("welded_violet")),
            ("LR_MFE7516_Vinyl_Ester_SDS.pdf", sds()),
            ("LR_Silicate_Resin_Summer_SDS.pdf", render_silicate("summer")),
            ("LR_Silicate_Resin_Winter_SDS.pdf", render_silicate("winter")),
            ("LR_Silicate_Resin_Waterglass_Hardener_SDS.pdf", render_silicate("waterglass")),
            ("LR_Silicate_Resin_W01_Fast_SDS.pdf", render_silicate("w01"))]
    for name, html in jobs:
        HTML(string=html, base_url=HERE).write_pdf(os.path.join(OUT, name))
        print("wrote", name)


if __name__ == "__main__":
    main()
