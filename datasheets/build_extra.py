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
  /* SDS */
  .sds-sec {{ background:{B.CHAR}; color:#fff; font-weight:700; font-size:9pt;
    padding:5px 10px; margin:11px 0 0; break-after:avoid; }}
  .sds-sec b {{ color:{B.PINK}; margin-right:6px; }}
  .sds-body {{ padding:6px 2px 0; }}
  .sds-body p {{ margin:0 0 4px; font-size:8pt; color:#333; line-height:1.45; }}
  .sds-body p .lbl {{ font-weight:700; color:{B.CHAR}; }}
  table.kv {{ width:100%; border-collapse:collapse; margin-top:3px; break-inside:auto; }}
  table.kv td {{ border-bottom:1px solid #e6e4ea; padding:2.5px 8px; font-size:8pt;
    vertical-align:top; }}
  table.kv td.k {{ background:#f1eff3; font-weight:600; width:38%; color:{B.CHAR}; }}
  .hazbox {{ display:flex; gap:14px; align-items:center; background:#fdeef5;
    border:1px solid {B.PINK}; border-radius:8px; padding:10px 14px; margin-top:8px; }}
  .hazbox img {{ height:62px; width:auto; }}
  .hazbox .sig {{ font-weight:700; color:{B.PINK}; font-size:10pt; }}
  /* SDS cover page */
  .cover-haz {{ display:flex; gap:16px; align-items:center; background:{B.CHAR};
    border-radius:12px; padding:16px 20px; margin-top:16px; }}
  .cover-haz img {{ height:78px; width:auto; background:#fff; border-radius:8px; padding:4px; }}
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


def head(title_a, title_b, subtitle, kind="Technical data sheet"):
    return f"""
  <div class="sidebar"></div>
  <h1 class="tds">{kind}</h1>
  <div class="titlebar">
    <div class="t"><span class="a">{title_a}</span><span class="b">{title_b}</span></div>
    <img src="{B.DROP}" alt="">
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
                 kind="Safety data sheet")
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


def main():
    jobs = [("LR_Glassfiber_Complex_1050.pdf", glassfiber()),
            ("LR_Connection_Liners.pdf", connection()),
            ("LR_End_Cap_Glue.pdf", endcap()),
            ("LR_MFE7516_Vinyl_Ester_SDS.pdf", sds())]
    for name, html in jobs:
        HTML(string=html, base_url=HERE).write_pdf(os.path.join(OUT, name))
        print("wrote", name)


if __name__ == "__main__":
    main()
