"""Small white line-icons (SVG) for the IMS-style datasheet feature cells."""

_S = ('<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="#fff" '
      'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{}</svg>')

ICONS = {
    # diameter — circle with horizontal double arrow
    "diameter": _S.format('<circle cx="12" cy="12" r="7"/>'
                          '<path d="M5 12h14M8 9l-3 3 3 3M16 9l3 3-3 3"/>'),
    # wall thickness — two arrows pointing inward to a gap
    "thickness": _S.format('<path d="M3 6v12M21 6v12M7 12h3M14 12h3"/>'
                           '<path d="M10 9l-3 3 3 3M14 9l3 3-3 3"/>'),
    # length — ruler
    "length": _S.format('<rect x="2" y="8" width="20" height="8" rx="1"/>'
                        '<path d="M7 8v3M12 8v4M17 8v3"/>'),
    # undersize — compress arrows
    "undersize": _S.format('<path d="M4 12h6M14 12h6M7 9l3 3-3 3M17 9l-3 3 3 3"/>'),
    # bend / elbow pipe
    "bend": _S.format('<path d="M5 20v-6a8 8 0 0 1 8-8h6"/>'
                      '<path d="M16 3l3 3-3 3"/>'),
    # curing — heat / sun
    "curing": _S.format('<circle cx="12" cy="12" r="4"/>'
                        '<path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19"/>'),
    # textile — weave grid
    "textile": _S.format('<path d="M4 8h16M4 12h16M4 16h16M8 4v16M12 4v16M16 4v16"/>'),
    # coating — layers
    "coating": _S.format('<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>'),
    # weight — scale
    "weight": _S.format('<path d="M5 8h14l-2 11H7L5 8z"/><path d="M9 8a3 3 0 0 1 6 0"/>'),
    # colour — swatch / drop
    "colour": _S.format('<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>'),
    # storage — thermometer
    "storage": _S.format('<path d="M10 13V5a2 2 0 0 1 4 0v8a4 4 0 1 1-4 0z"/>'),
    # liner — tube end
    "liner": _S.format('<path d="M3 9h12v6H3z"/><path d="M15 8l5 2v4l-5 2z"/>'),
    # resin — drop
    "resin": _S.format('<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>'),
    # certificate — badge
    "certificate": _S.format('<circle cx="12" cy="9" r="6"/><path d="M9 14l-2 7 5-3 5 3-2-7"/>'),
    # material — knit loop
    "material": _S.format('<path d="M4 12c2-4 6-4 8 0s6 4 8 0"/><path d="M4 16c2-4 6-4 8 0s6 4 8 0"/>'),
}
