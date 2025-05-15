"""
This module provides a class `ResumeTextExtractor` for extracting and cleaning 
resume text from PDF and DOCX files. It uses PyMuPDF for PDF parsing and 
python-docx for DOCX parsing. The extracted text is cleaned by collapsing 
extra whitespace, standardizing bullet symbols, and normalizing common 
resume section headers (e.g., Skills, Experience, Education).

Typical usage example:
    extractor = ResumeTextExtractor("path/to/resume.pdf", verbose=True)
    text = extractor.extract_text()
    print(text)

Classes:
    ResumeTextExtractor: A class for extracting and formatting resume content.

Dependencies:
    fitz (PyMuPDF), python-docx, os, re

Raises:
    FileNotFoundError: If the specified resume file does not exist.
    ValueError: If the file extension is not PDF or DOCX.
    RuntimeError: If text extraction fails or file is empty.
"""



import fitz  # PyMuPDF
from docx import Document
import os
import re

class ResumeTextExtractor:
    """
    Extracts and cleans text from resumes in PDF or DOCX format.

    This class supports layout-aware PDF text extraction using PyMuPDF and
    paragraph-based DOCX extraction using python-docx. It also normalizes
    formatting by collapsing excess whitespace, standardizing bullets, and
    normalizing common resume section headers for easier downstream parsing.

    Attributes:
        file_path (str): Path to the resume file (PDF or DOCX).
        verbose (bool): Whether to log verbose output during processing.
        text (str): Extracted and cleaned resume text.
    """

    def __init__(self, file_path, verbose=False):
        """
        Initializes the ResumeTextExtractor with a file path and verbosity.

        Args:
            file_path (str): The path to the resume file.
            verbose (bool, optional): Whether to print verbose output. Defaults to False.
        """
        self.file_path = file_path
        self.verbose = verbose
        self.text = ""

    def extract_text(self):
        """
        Extracts and returns cleaned text from the resume file.

        Returns:
            str: Cleaned resume text.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file extension is unsupported.
        """
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"The file does not exist: {self.file_path}")

        ext = os.path.splitext(self.file_path)[1].lower()

        if ext == ".pdf":
            self.text = self._extract_pdf()
        elif ext == ".docx":
            self.text = self._extract_docx()
        else:
            raise ValueError("Unsupported file type. Only PDF and DOCX files are allowed.")

        return self.text

    def _extract_pdf(self):
        """
        Extracts and cleans text from a PDF resume.

        Returns:
            str: Cleaned resume text from PDF.

        Raises:
            RuntimeError: If text extraction fails or PDF is empty.
        """
        try:
            if self.verbose:
                print(f"Reading PDF: {self.file_path}")

            with fitz.open(self.file_path) as doc:
                raw_text = "\n".join(
                    page.get_text("text").strip()
                    for page in doc
                    if page.get_text("text").strip()
                )

            if not raw_text:
                raise ValueError("PDF contains no extractable text (possibly scanned image).")

            return self._clean_text(raw_text)

        except Exception as e:
            raise RuntimeError(f"PDF extraction failed for '{self.file_path}': {e}")

    def _extract_docx(self):
        """
        Extracts and cleans text from a DOCX resume.

        Returns:
            str: Cleaned resume text from DOCX.

        Raises:
            RuntimeError: If text extraction fails or document is empty.
        """
        try:
            if self.verbose:
                print(f"Reading DOCX: {self.file_path}")

            doc = Document(self.file_path)
            text_parts = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            combined_text = "\n".join(text_parts)

            if not combined_text:
                raise ValueError("DOCX file contains no extractable paragraph text.")

            return self._clean_text(combined_text)

        except Exception as e:
            raise RuntimeError(f"DOCX extraction failed for '{self.file_path}': {e}")

    def _clean_text(self, raw_text):
        """
        Cleans the extracted raw text by normalizing layout and section headers.

        This includes collapsing extra newlines, standardizing bullet characters,
        and converting section headers (like 'Education', 'Skills') to a consistent format.

        Args:
            raw_text (str): The raw text extracted from the resume.

        Returns:
            str: Cleaned and formatted text.
        """
        # Normalize excessive newlines
        text = re.sub(r'\n{2,}', '\n\n', raw_text)
        lines = [line.strip() for line in text.splitlines()]
        text = "\n".join(lines)

        # Normalize bullets
        text = re.sub(r'^\s*[•·●‣▪]', '-', text, flags=re.MULTILINE)

        # Normalize section headers
        section_keywords = [
            "Summary", "Professional Summary", "Career Objective",
            "Skills", "Experience", "Education", "Certifications",
            "Projects", "Languages", "Interests", "Volunteer", "References"
        ]
        for keyword in section_keywords:
            text = re.sub(rf"\b{re.escape(keyword)}\b", f"{keyword}:", text, flags=re.IGNORECASE)

        return text
