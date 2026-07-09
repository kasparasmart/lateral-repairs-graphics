"""Extract and clean the LR Silicate Resin Safety Data Sheets (PDF) into a
structured JSON (cover fields + 16 sections) for the LR-style SDS renderer."""
import json
import os
import re
import re as R
import subprocess

SRC = "/tmp/redts"
OUT = os.path.join(os.path.dirname(__file__), "assets", "silicate_sds.json")

FILES = [
    ("LR Silicate Resin Type Summer.pdf", "summer", "LR Silicate Resin", "Type Summer"),
    ("LR Silicate Resin Type W (WINTER) EN.pdf", "winter", "LR Silicate Resin", "Type W · Winter"),
    ("LR Silicate Resin Type Waterglass (HARDENER) 1 EN.pdf", "waterglass", "LR Silicate Resin", "Waterglass · Hardener"),
    ("LR Silicate Resin W01 (FAST) EN.pdf", "w01", "LR Silicate Resin", "Type W01 · Fast"),
]

DROP_PATTERNS = [
    r"^SAFETY DATA SHEET\s*$",
    r"^Trade name:",
    r"^According to Regulation",
    r"^No 1907/2006 and",
    r"^Regulation \(EU\) 2015/830",
    r"^\s*\d+\s*/\s*\d+\s*$",           # page numbers  N/M
]
DROP_RE = re.compile("|".join(DROP_PATTERNS))
META_RE = re.compile(r"(Date of print|Date of issue|Version)\s*:?\s*([0-9./A-Za-z ]+)")


def clean_lines(txt):
    txt = txt.replace('\uf0b0', '°').replace('\uf0a3', '≤').replace('\uf0b3', '≥')
    txt = txt.replace('\uf02d', '-').replace('\uf0ae', '→').replace('\ufb01', 'fi')
    txt = R.sub('[\uf000-\uf0ff]', '', txt)  # drop remaining Symbol/Wingdings glyphs
    out = []
    for raw in txt.split("\n"):
        line = raw.rstrip()
        if not line.strip():
            out.append("")
            continue
        if DROP_RE.search(line.strip()):
            continue
        # strip the right-hand "Date of print ... Version" columns that ride along
        line = re.sub(r"\s{3,}(Date of (print|issue)|Version)\s*:.*$", "", line)
        out.append(re.sub(r"[ \t]{2,}", "  ", line.rstrip()))
    # collapse 3+ blank lines
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def split_sections(text):
    # section headers: "SECTION N: Title"
    idxs = [(m.start(), int(m.group(1)), m.group(2).strip())
            for m in re.finditer(r"SECTION (\d+):\s*(.*)", text)]
    secs = []
    for i, (pos, num, title) in enumerate(idxs):
        end = idxs[i + 1][0] if i + 1 < len(idxs) else len(text)
        body = text[pos:end].split("\n", 1)[1] if "\n" in text[pos:end] else ""
        # title may wrap onto next line(s) before content; keep as-is
        lines = [l for l in body.split("\n")]
        # trim leading/trailing blanks
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        # merge a wrapped title continuation (all-lowercase short line) into the title
        while lines and re.match(r"^[a-z][a-z/ ]{1,28}$", lines[0].strip()):
            title = title.rstrip() + " " + lines.pop(0).strip()
            while lines and not lines[0].strip():
                lines.pop(0)
        secs.append({"num": num, "title": re.sub(r"\s{2,}", " ", title), "lines": lines})
    return secs


def grab(text, pat, flags=re.S):
    m = re.search(pat, text, flags)
    return m.group(1).strip() if m else ""


def extract_cover(text, raw):
    meta = {k: "" for k in ("print", "issue", "version")}
    for m in META_RE.finditer(raw):
        key = m.group(1).lower()
        val = m.group(2).strip()
        if "print" in key and not meta["print"]:
            meta["print"] = val.split("Date")[0].strip()
        elif "issue" in key and not meta["issue"]:
            meta["issue"] = val.split("Version")[0].strip()
        elif "version" in key and not meta["version"]:
            meta["version"] = val.strip()
    use = grab(text, r"1\.2\.[^\n]*\n(.*?)\n1\.3\.")
    use = re.sub(r"\s+", " ", use)
    email = grab(text, r"([\w.]+@lateralrepairs\.com)")
    phone = re.sub(r"\s+", " ", grab(text, r"(\+370[\d ]{6,})")).strip()
    emergency = re.sub(r"\s+", " ", grab(text, r"1\.4\.[^\n]*\n(.*?)\nSECTION 2"))
    signal = grab(text, r"Signal word:\s*([A-Za-z]+)")
    # H-statements: capture from the "Hazard statements:" block and the
    # classification table; description may wrap to the next line.
    lines = text.split("\n")
    hseen = {}
    for i, ln in enumerate(lines):
        m = re.match(r"^\s*(H\d{3})\b[\s:]+(.*)$", ln)
        if m:
            code, desc = m.group(1), m.group(2).strip()
            j = i + 1
            while j < len(lines) and not re.match(r"^\s*(H\d{3}|P\d|SECTION|\d\.\d|[A-Z][a-z]+ )", lines[j]) and lines[j].strip() and len(desc) < 90:
                desc += " " + lines[j].strip(); j += 1
            d = re.sub(r"\s+", " ", desc).strip().rstrip(".")
            if d and code not in hseen:
                hseen[code] = d
    hstate = [(c, hseen[c]) for c in sorted(hseen)]
    # P-statements from the "Precautionary statements:" area
    pseen = {}
    for i, ln in enumerate(lines):
        m = re.match(r"^\s*(P\d{3}(?:\s*\+\s*P\d{3})*)\b[\s:]+(.+)$", ln)
        if m:
            code = re.sub(r"\s*\+\s*", "+", m.group(1))
            desc = m.group(2).strip()
            if code not in pseen and len(desc) > 3:
                pseen[code] = re.sub(r"\s+", " ", desc)
    pstate = [(c, pseen[c]) for c in pseen][:6]
    return dict(meta=meta, use=use, email=email or "info@lateralrepairs.com",
                phone=phone, emergency=emergency, signal=signal or "Danger",
                hstatements=hstate, pstatements=pstate[:6])


HDR_JUNK = re.compile(r"^(SAFETY DATA SHEET|Trade name:|According to Regulation|"
                      r"No 1907/2006|Regulation \(EU\)|Date of (print|issue)|Version)")


def parse_classification(raw):
    """Section 2.1 CLP classification table -> [(hazard class, H-code, statement)]."""
    m = re.search(r"2\.1\. Classification.*?Classification according to[^\n]*\n(.*?)\n\s*2\.2\.",
                  raw, re.S)
    if not m:
        return []
    rows, pending = [], None
    for ln in m.group(1).split("\n"):
        if HDR_JUNK.search(ln.strip()) or not ln.strip():
            continue
        mm = re.match(r"^\s*([A-Za-z][\w.'’]*(?:\s+[\w.'’()]+)*?\.?\s*\d[A-Z]?)\s{2,}(H\d{3})\s+(.*)$", ln)
        if mm:
            if pending:
                rows.append(pending)
            pending = [re.sub(r"\s+", " ", mm.group(1)).strip(), mm.group(2),
                       mm.group(3).strip()]
        elif pending and not re.match(r"^\s*\d\.\d", ln):      # wrapped statement
            pending[2] = (pending[2] + " " + ln.strip()).strip()
    if pending:
        rows.append(pending)
    return [[c[0], c[1], re.sub(r"\s+", " ", c[2]).rstrip(".")] for c in rows]


def parse_composition(raw):
    """Section 3 mixtures table -> [{name, ec, cas, reach, content, classification}]."""
    m = re.search(r"SECTION 3:.*?\n(.*?)\n\s*1\s*\n?\s*[–-]\s*See Section 16", raw, re.S)
    if not m:
        m = re.search(r"SECTION 3:(.*?)SECTION 4:", raw, re.S)
        if not m:
            return []
    block = m.group(1)
    # column x-positions (column within the line, not absolute offset)
    def xpos(kw):
        for ln in block.split("\n"):
            i = ln.find(kw)
            if i >= 0:
                return i
        return None
    ec = xpos("EC No.") or 30
    cas = xpos("CAS No.") or 44
    reach = (xpos("REACH") or 58) - 2
    content = (xpos("(%)") or xpos("Content") or 72) - 4
    cat = (xpos("Hazard") or xpos("categories") or 86) + 1
    hph = xpos("H-phrase") or 104
    bnds = [0, ec, cas, reach, content, cat, hph, 999]
    keys = ["name", "ec", "cas", "reach", "content", "cat", "hph"]

    data_lines = []
    started = False
    for ln in block.split("\n"):
        if re.search(r"\bName\b", ln) and "EC No." in ln:
            started = True
            continue
        if not started:
            continue
        if HDR_JUNK.search(ln.strip()):
            continue
        if ln.strip():
            data_lines.append(ln)

    def slice_cols(ln):
        return {keys[i]: ln[bnds[i]:bnds[i + 1]].strip() for i in range(7)}

    sliced = [slice_cols(ln) for ln in data_lines]
    anchors = [i for i, s in enumerate(sliced)
               if re.search(r"[<>≤≥]?\s*\d+\s*(–|-|to)?\s*\d*\s*%?$", s["content"]) and s["content"]]
    if not anchors:
        anchors = [i for i, s in enumerate(sliced) if s["cas"] or s["ec"]]
    ings = []
    for k, a in enumerate(anchors):
        lo = 0 if k == 0 else (anchors[k - 1] + a) // 2 + 1
        hi = len(sliced) if k == len(anchors) - 1 else (a + anchors[k + 1]) // 2
        chunk = sliced[lo:hi]
        name = " ".join(s["name"] for s in chunk if s["name"])
        cats = [s["cat"] for s in chunk if s["cat"]]
        hphs = [s["hph"] for s in chunk if s["hph"]]
        cls = ", ".join(f"{c} ({h})" for c, h in zip(cats, hphs)) if cats else (
            ", ".join(cats + hphs) if (cats or hphs) else "—")
        pick = lambda key: next((s[key] for s in chunk if s[key]), "—")
        ings.append(dict(name=re.sub(r"\s+", " ", name).strip() or "—",
                         ec=pick("ec"), cas=pick("cas"), reach=pick("reach"),
                         content=pick("content"), classification=cls or "—"))
    return ings


def pictos(hcodes):
    codes = set(hcodes)
    out = []
    if codes & {"H314", "H318"}:
        out.append("ghs05")
    if codes & {"H334", "H351", "H340", "H350", "H360", "H372", "H373", "H304"}:
        out.append("ghs08")
    if (codes & {"H302", "H312", "H315", "H317", "H319", "H332", "H335", "H336"}
            and "ghs05" not in out):
        out.append("ghs07")
    return out or ["ghs07"]


def main():
    data = {}
    for fname, slug, ta, tb in FILES:
        raw = subprocess.check_output(
            ["pdftotext", "-layout", os.path.join(SRC, fname), "-"]).decode("utf-8", "ignore")
        text = clean_lines(raw)
        cover = extract_cover(text, raw)
        cover["pictos"] = pictos([c for c, _ in cover["hstatements"]])
        secs = split_sections(text)
        class_tbl = parse_classification(raw)
        for s in secs:
            if s["num"] == 2 and class_tbl:
                s["class_table"] = class_tbl
        data[slug] = dict(title_a=ta, title_b=tb, cover=cover, sections=secs)
        print(f"{slug:11s} sections={len(secs)} H={len(cover['hstatements'])} "
              f"pictos={cover['pictos']} issue={cover['meta']['issue']}")
    json.dump(data, open(OUT, "w"), ensure_ascii=False, indent=1)
    print("saved", OUT)


if __name__ == "__main__":
    main()
