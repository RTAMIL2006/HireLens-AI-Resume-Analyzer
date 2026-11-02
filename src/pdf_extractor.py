"""
pdf_extractor.py
----------------
Responsible for one job only: turning a PDF resume file into plain text.

We use PyMuPDF (imported as `fitz`) because it's fast, free, and doesn't
need any external system dependencies (unlike some other PDF libraries).

Privacy note: everything here happens in memory / on the local filesystem
during the session. We do not upload the resume anywhere or store it
permanently - it exists only for the duration of the analysis.
"""

import fitz  # PyMuPDF


class PDFExtractionError(Exception):
    """Raised when we cannot extract text from a given PDF file."""
    pass


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract all readable text from a PDF file.

    Parameters
    ----------
    file_bytes : bytes
        The raw bytes of the uploaded PDF file (e.g. from Streamlit's
        `st.file_uploader`, using `.read()` or `.getvalue()`).

    Returns
    -------
    str
        The extracted plain text, with pages joined by newlines.

    Raises
    ------
    PDFExtractionError
        If the file is not a valid PDF, is empty, or contains no
        extractable text (e.g. a scanned image with no text layer).
    """
    if not file_bytes:
        raise PDFExtractionError("The uploaded file is empty.")

    try:
        # "stream" mode lets us open a PDF directly from bytes,
        # without needing to save it to disk first.
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as exc:
        raise PDFExtractionError(
            f"Could not open the file as a PDF. Is it a valid, non-corrupted "
            f"PDF? (Details: {exc})"
        ) from exc

    if doc.page_count == 0:
        doc.close()
        raise PDFExtractionError("The PDF has no pages.")

    pages_text = []
    for page in doc:
        pages_text.append(page.get_text())
    doc.close()

    full_text = "\n".join(pages_text).strip()

    if not full_text:
        raise PDFExtractionError(
            "No readable text was found in this PDF. It may be a scanned "
            "image without a text layer. Try uploading a text-based PDF "
            "(e.g. exported directly from Word/Google Docs)."
        )

    return full_text
