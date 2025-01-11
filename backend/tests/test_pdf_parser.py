import pytest
from backend.modules.invoice_processing.parsers.pdf_parser import PDFParser
from unittest.mock import mock_open, patch

def test_process_file_valid_pdf():
    parser = PDFParser()
    # Mock extract_text to avoid actual PDF processing
    with patch('backend.modules.invoice_processing.parsers.pdf_parser.extract_text') as mock_extract:
        mock_extract.return_value = "Invoice Number\n2023-10-26\n$100.00\nAcme Corp"
        result = parser._process_file("fake_path.pdf")
        assert result == {
            "invoice_number": "Invoice Number",
            "date": "2023-10-26",
            "total_amount": 100.00,
            "vendor_name": "Acme Corp",
        }

def test_process_file_invalid_pdf():
    parser = PDFParser()
    # Mock extract_text to raise an exception
    with patch('backend.modules.invoice_processing.parsers.pdf_parser.extract_text') as mock_extract:
        mock_extract.side_effect = Exception("Invalid PDF")
        with pytest.raises(Exception, match="Invalid PDF"):
            parser._process_file("fake_path.pdf")

def test_extract_invoice_data_basic():
    parser = PDFParser()
    text = "Invoice Number\n2023-10-26\n$100.00\nAcme Corp"
    result = parser.extract_invoice_data(text)
    assert result == {
        "invoice_number": "Invoice Number",
        "date": "2023-10-26",
        "total_amount": 100.00,
        "vendor_name": "Acme Corp",
    }

def test_extract_invoice_data_delimiter():
    parser = PDFParser(delimiter=";")
    text = "Invoice Number;2023-10-26;$100.00;Acme Corp"
    result = parser.extract_invoice_data(text)
    assert result == {
        "invoice_number": "Invoice Number",
        "date": "2023-10-26",
        "total_amount": 100.00,
        "vendor_name": "Acme Corp",
    }

def test_extract_invoice_data_template():
    parser = PDFParser(extraction_option="template")
    text = "Some invoice text"
    result = parser.extract_invoice_data(text)
    assert result == {"message": "Template-based extraction not implemented yet"}
