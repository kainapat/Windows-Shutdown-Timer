# -*- coding: utf-8 -*-
"""Export generated HTML diagrams to standalone SVG and crisp 2x PNG images."""

import os
import re
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage, QPainter, QColor
from PySide6.QtCore import Qt, QSize
from PySide6.QtSvg import QSvgRenderer

DIAGRAM_DIR = Path(__file__).resolve().parent

FONT_IMPORT = (
    "<style>@import url('https://fonts.googleapis.com/css2?"
    "family=Instrument+Serif:ital@0;1&amp;"
    "family=Geist:wght@400;500;600&amp;"
    "family=Geist+Mono:wght@400;500;600&amp;display=swap');</style>"
)


def export_svg(html_path: Path) -> Path:
    html_content = html_path.read_text(encoding="utf-8")
    svg_match = re.search(r"(<svg\b[^>]*>.*?</svg>)", html_content, re.DOTALL)
    if not svg_match:
        raise ValueError(f"No <svg> block found in {html_path}")

    svg_content = svg_match.group(1)

    # Ensure xmlns is present
    if 'xmlns="http://www.w3.org/2000/svg"' not in svg_content:
        svg_content = re.sub(r"<svg\b", '<svg xmlns="http://www.w3.org/2000/svg"', svg_content, count=1)

    # Inject font @import into <defs>
    if "<defs>" in svg_content:
        svg_content = svg_content.replace("<defs>", f"<defs>\n          {FONT_IMPORT}", 1)
    else:
        svg_content = re.sub(r"(<svg\b[^>]*>)", r"\1\n  <defs>\n    " + FONT_IMPORT + "\n  </defs>", svg_content, count=1)

    out_svg = html_path.with_suffix(".svg")
    xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg_content
    out_svg.write_text(xml_output, encoding="utf-8")
    print(f"  [SVG] Exported: {out_svg.name}")
    return out_svg


def export_png(svg_path: Path, scale: int = 2) -> Path:
    renderer = QSvgRenderer(str(svg_path))
    if not renderer.isValid():
        raise ValueError(f"Invalid SVG file for rendering: {svg_path}")

    default_size = renderer.defaultSize()
    w = default_size.width() * scale
    h = default_size.height() * scale

    image = QImage(w, h, QImage.Format_ARGB32_Premultiplied)
    image.fill(Qt.transparent)

    painter = QPainter(image)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.TextAntialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)
    renderer.render(painter)
    painter.end()

    out_png = svg_path.with_suffix(".png")
    image.save(str(out_png), "PNG")
    print(f"  [PNG] Exported: {out_png.name} ({w}x{h}px)")
    return out_png


def main():
    app = QApplication(sys.argv)
    html_files = sorted(DIAGRAM_DIR.glob("*.html"))
    print(f"Found {len(html_files)} HTML diagrams to export in {DIAGRAM_DIR}:")
    
    for html_file in html_files:
        print(f"\nProcessing {html_file.name}...")
        svg_file = export_svg(html_file)
        export_png(svg_file, scale=2)

    print("\n All diagrams exported successfully to SVG and PNG!")


if __name__ == "__main__":
    main()
