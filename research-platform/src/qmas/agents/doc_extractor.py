"""Agente de extração de documentos financeiros.

Pipeline: PyMuPDF (texto nativo) -> regex (campos) -> OCR (fallback p/ scans).
"""

from __future__ import annotations

import re
from typing import Any

import fitz  # PyMuPDF

from qmas.agents.base import Agent
from qmas.core.contracts import TaskKind

# Padrões de campos comuns em documentos financeiros BR — expandir conforme corpus
PATTERNS = {
    "cnpj": re.compile(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"),
    "valor": re.compile(r"R\$\s?[\d.]+,\d{2}"),
    "data": re.compile(r"\d{2}/\d{2}/\d{4}"),
}


class DocExtractorAgent(Agent):
    name = "doc_extractor"
    handles = (TaskKind.EXTRACT,)

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        path = payload["path"]
        text = self._extract_text(path)
        fields = {k: pat.findall(text) for k, pat in PATTERNS.items()}
        return {"n_chars": len(text), "fields": fields}

    def _extract_text(self, path: str) -> str:
        doc = fitz.open(path)
        text = "\n".join(page.get_text() for page in doc)
        if len(text.strip()) < 50:  # provável scan -> OCR
            text = self._ocr(doc)
        return text

    def _ocr(self, doc: "fitz.Document") -> str:
        import pytesseract
        from PIL import Image
        import io

        chunks = []
        for page in doc:
            pix = page.get_pixmap(dpi=200)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            chunks.append(pytesseract.image_to_string(img, lang="por"))
        return "\n".join(chunks)
