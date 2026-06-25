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
  .illus {{ text-align:center; margin:18px 0 6px; }}
  .illus img {{ max-width:74%; max-height:8.2cm; }}
  .illus figcaption {{ margin-top:8px; font-size:8.5pt; color:#777; }}
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
  <div class="foot">
    <div>For further information visit <a href="https://www.lateralrepairs.com">www.lateralrepairs.com</a> · info@lateralrepairs.com</div>
    <div>Issue: V2026.1 · 2026.06</div>
  </div>"""


def feature_table2(title, rows):
    body = "".join(
        f'<tr><td class="k2">{(B.ic(ic_)+" " if ic_ else "")}{k}</td><td class="v">{v}</td></tr>'
        for ic_, k, v in rows)
    return f'<table class="f"><tr><td class="hd" colspan="2">{title}</td></tr>{body}</table>'


# ----------------------------------------------------------------- Glassfiber
def glassfiber():
    rows = [
        ("material", "Glass composition", "E-CR Glass"),
        ("weight", "Weight per unit area", "1075 g/m² ± 8 % <span style='color:#777'>(deviation from nominal)</span>"),
        ("textile", "1st layer — Chopped Strand Mat", "500 g/m²"),
        ("textile", "2nd layer — Woven Roving", "Warp 0°: 150 g/m² &nbsp;·&nbsp; Weft 90°: 410 g/m²"),
        ("coating", "Bonding", "Stitching"),
        ("material", "Sewing thread (polyester)", "≤ 15 g/m²"),
        ("resin", "Moisture content", "&lt; 0.15 %"),
        ("thickness", "Edges", "Trimmed"),
        ("length", "Width", "Variable ± 1.5 cm"),
        ("coating", "Type of size", "Suitable for UP-, VE- and EP- resins"),
        ("colour", "Coupling agent", "Silane"),
        ("diameter", "Tube diameter, internal", "70 mm"),
    ]
    body = B.css() + EXTRA_CSS
    body += head("Glassfiber ", "Complex 1080",
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


def main():
    jobs = [("LR_Glassfiber_Complex_1080.pdf", glassfiber()),
            ("LR_Connection_Liners.pdf", connection())]
    for name, html in jobs:
        HTML(string=html, base_url=HERE).write_pdf(os.path.join(OUT, name))
        print("wrote", name)


if __name__ == "__main__":
    main()
