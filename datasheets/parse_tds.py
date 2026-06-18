"""Parse the MULTIline TDS Word-doc tables (source_tables.json) into a clean
per-product data model. No values are altered — only structured."""
import json
import os
import re

SRC = os.path.join(os.path.dirname(__file__), "assets", "source_tables.json")

# filename -> (display name, variant subtitle, old name)
PRODUCTS = [
    ("LR MULTIline  PRO 4.0 mm TDS (Nanotech HD).docx", "MULTIline PRO", "4.0 mm", "Nanotech HD", "pro-40"),
    ("LR MULTIline  PRO 4.5 mm TDS (Nanotech 4.5).docx", "MULTIline PRO", "4.5 mm", "Nanotech 4.5", "pro-45"),
    ("LR MULTIline FLEX TDS (DrainPlus).docx",           "MULTIline FLEX", "",     "DrainPlus", "flex"),
    ("LR MULTIline FORCE TDS (Mega).docx",               "MULTIline FORCE", "",    "Mega", "force"),
    ("LR MULTIline FORCE RF TDS (Mega RF).docx",         "MULTIline FORCE", "RF",   "Mega RF", "force-rf"),
    ("LR MULTIline FORCE UV TDS (Mega UV).docx",         "MULTIline FORCE", "UV",   "Mega UV", "force-uv"),
    ("LR MULTIline  CORE TDS (Polynex).docx",            "MULTIline CORE", "",      "Polynex", "core"),
]


def _clean(s):
    return re.sub(r"[ \t]+", " ", (s or "").replace(" ", " ")).strip()


def _is_section(row):
    """A section header row repeats the same text across all cells (and is
    not a footnote line beginning with '*')."""
    vals = [_clean(c) for c in row]
    return bool(vals[0]) and len(set(vals)) == 1 and not vals[0].startswith("*")


def _is_note(row):
    vals = [_clean(c) for c in row]
    return bool(vals[0]) and len(set(vals)) == 1 and vals[0].startswith("*")


def _is_disclaimer(row):
    v0 = _clean(row[0])
    return v0.lower().startswith("the final quality")


def parse_product(entry):
    tabs = entry["tables"]
    paras = entry.get("paras", [])
    t1, t2 = tabs[0], tabs[1]

    info = {
        "product_name": "", "product_code": "",
        "material": "", "supply": [], "general": [], "seam": [],
        "physical": [], "handling": [], "notes": [], "disclaimer": "",
    }

    # ---- Table 1: product / material / supply / general ----
    section = None
    for row in t1:
        a, b = _clean(row[0]), _clean(row[1]) if len(row) > 1 else ""
        if not a and not b:
            continue
        if _is_section(row):
            section = a.lower()
            continue
        if a == "Product name":
            info["product_name"] = b
        elif a == "Product code":
            info["product_code"] = b
        elif section and section.startswith("material"):
            # material rows have empty label, text in col2
            txt = b or a
            if txt and txt.lower() != "material composition":
                info["material"] = (info["material"] + " " + txt).strip()
        elif not a and b:
            # stray material continuation
            if section and section.startswith("material"):
                info["material"] = (info["material"] + " " + b).strip()
        elif section and section.startswith("supply"):
            info["supply"].append((a, b))
        elif section and section.startswith("general"):
            if a.startswith("Used seam"):
                info["seam"].append(b)
            else:
                info["general"].append((a, b))

    # ---- Table 2: physical properties / handling / notes ----
    section = None
    for row in t2:
        cells = [_clean(c) for c in row]
        if not any(cells):
            continue
        if _is_disclaimer(row):
            info["disclaimer"] = cells[0]
            continue
        if _is_note(row):
            info["notes"].append(cells[0])
            continue
        if _is_section(row):
            section = cells[0].lower()
            continue
        prop, cond, unit, val = (cells + ["", "", "", ""])[:4]
        if section and section.startswith("physical"):
            info["physical"].append((prop, cond, unit, val))
        elif section and section.startswith("handling"):
            info["handling"].append((prop, cond, unit, val))

    # body paragraphs (Additional Information, steam-curing advice) become notes
    for p in paras:
        pc = _clean(p)
        if pc and pc not in info["notes"]:
            info["notes"].append(pc)

    return info


def load_all():
    data = json.load(open(SRC, encoding="utf-8"))
    out = []
    for fname, name, variant, old, slug in PRODUCTS:
        info = parse_product(data[fname])
        info.update({"display": name, "variant": variant, "old": old, "slug": slug})
        out.append(info)
    return out


if __name__ == "__main__":
    for p in load_all():
        print("\n===", p["display"], p["variant"], "| code", p["product_code"], "| was", p["old"])
        print("  product_name:", p["product_name"])
        print("  material:", p["material"])
        print("  supply:", p["supply"])
        print("  general:", p["general"])
        print("  seam:", p["seam"])
        print("  physical:", p["physical"])
        print("  handling:", p["handling"])
        print("  notes:", p["notes"])
