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
</style>"""


def head(title_a, title_b, subtitle):
    return f"""
  <div class="sidebar"></div>
  <h1 class="tds">Technical data sheet</h1>
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


def main():
    jobs = [("LR_Glassfiber_Complex_1050.pdf", glassfiber()),
            ("LR_Connection_Liners.pdf", connection()),
            ("LR_End_Cap_Glue.pdf", endcap())]
    for name, html in jobs:
        HTML(string=html, base_url=HERE).write_pdf(os.path.join(OUT, name))
        print("wrote", name)


if __name__ == "__main__":
    main()
