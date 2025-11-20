"""PDF loader helpers.

This module provides a small helper to normalize PDF contents to raw bytes
that can be passed to an LLM backend which accepts PDF binary data.

The function intentionally keeps the behavior minimal and defensive. For
full-featured text extraction use libraries such as `pdfplumber` or
`PyPDF2` (listed in `requirements.txt`).

Compatibility note (convenience): callers sometimes open a file in text
mode (e.g. `open('file.pdf', 'r')`) and then pass the file object or its
`.read()` result into this helper. That case is supported: if text is
provided, we convert it to bytes using ISO-8859-1 (latin-1) which maps code
points 0..255 directly to byte values and preserves raw bytes when the
text was produced by reading binary data in text mode. Prefer opening files
in binary mode (`'rb'`) when possible.
"""

from typing import Any


def _is_pdf_bytes(data: bytes) -> bool:
    """Return True if `data` looks like a PDF by checking the magic header.

    This is a lightweight sanity check: PDF files begin with the bytes
    ``%PDF-``.
    """
    return isinstance(data, (bytes, bytearray)) and data[:5] == b"%PDF-"


def load_pdf_binary(pdf_contents: Any) -> bytes:
    """Normalize input to PDF bytes.

    Accepts any of:
      - bytes or bytearray: returned (after validation)
      - a file-like object with a ``read()`` method (binary or text mode)
      - a str (assumed to be text read from a file) — converted with latin-1

    Returns:
        bytes: validated PDF bytes (same content returned as ``bytes``)

    Raises:
        TypeError: if the provided value isn't bytes-like or file-like.
        ValueError: if the resulting bytes do not start with the PDF header.

    Example (recommended):
        with open('resumes/example.pdf', 'rb') as f:
            pdf_bytes = load_pdf_binary(f)

    Example (text-mode file object — supported but not recommended):
        f = open('resumes/example.pdf', 'r')
        pdf_bytes = load_pdf_binary(f)  # will encode using latin-1
    """
    # bytes-like: accept directly
    if isinstance(pdf_contents, (bytes, bytearray)):
        data = bytes(pdf_contents)

    # file-like object: read its content (may return bytes or str)
    elif hasattr(pdf_contents, 'read'):
        raw = pdf_contents.read()
        if isinstance(raw, (bytes, bytearray)):
            data = bytes(raw)
        elif isinstance(raw, str):
            # Convert text to bytes preserving byte values 0..255
            data = raw.encode('latin-1')
        else:
            raise TypeError('file.read() returned unsupported type')

    # text string: convert to bytes (assume it came from a text-mode read)
    elif isinstance(pdf_contents, str):
        data = pdf_contents.encode('latin-1')

    else:
        raise TypeError('Unsupported input type for load_pdf_binary; expected bytes, file-like, or str')

    if not _is_pdf_bytes(data):
        raise ValueError('Provided data does not appear to be a PDF (missing %PDF- header)')

    return data
