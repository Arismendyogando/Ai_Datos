import pytest
from backend.services.invoice_parser import InvoiceParser
from backend.modules.invoice_processing.parsers.pdf_parser import PDFParser
from backend.modules.invoice_processing.parsers.excel_parser import ExcelParser
from backend.modules.invoice_processing.parsers.image_parser import ImageParser

@pytest.fixture
def invoice_parser():
    return InvoiceParser()

def test_invoice_parser_initialization(invoice_parser):
    assert isinstance(invoice_parser.pdf_parser, PDFParser)
    assert isinstance(invoice_parser.excel_parser, ExcelParser)
    assert isinstance(invoice_parser.image_parser, ImageParser)

def test_parse_invoice_pdf(invoice_parser):
    result = invoice_parser.parse_invoice("sample_invoice.pdf")
    assert result is not None
    assert "invoice_number" in result
    assert "date" in result
    assert "total_amount" in result
    assert "company_name" in result
    assert "line_items" in result

def test_parse_invoice_excel(invoice_parser):
    result = invoice_parser.parse_invoice("sample_invoice.xlsx")
    assert result is not None
    assert "invoice_number" in result
    assert "date" in result
    assert "total_amount" in result
    assert "company_name" in result
    assert "line_items" in result

def test_parse_invoice_image(invoice_parser):
    result = invoice_parser.parse_invoice("sample_invoice.jpg")
    assert result is not None
    assert "invoice_number" in result
    assert "date" in result
    assert "total_amount" in result
    assert "company_name" in result
    assert "line_items" in result

def test_parse_invoice_unsupported_format(invoice_parser):
    result = invoice_parser.parse_invoice("sample_invoice.txt")
    assert result is None

def test_extract_invoice_number(invoice_parser):
    assert invoice_parser.extract_invoice_number("Invoice #12345") == "12345"
    assert invoice_parser.extract_invoice_number("Factura N° ABC-987") == "ABC-987"
    assert invoice_parser.extract_invoice_number("REF: XYZ123") == "XYZ123"
    assert invoice_parser.extract_invoice_number("No Invoice Number Found") is None

def test_extract_date(invoice_parser):
    assert invoice_parser.extract_date("Date: 12/31/2023") == "31/12/2023"
    assert invoice_parser.extract_date("Fecha: 2023-12-31") == "31/12/2023"
    assert invoice_parser.extract_date("Fecha de Emisión: 31-12-2023") == "31/12/2023"
    assert invoice_parser.extract_date("No Date Found") is None

def test_extract_total_amount(invoice_parser):
    assert invoice_parser.extract_total_amount("Total: $100.00") == "100.00"
    assert invoice_parser.extract_total_amount("Importe Total: 123,45 €") == "123,45"
    assert invoice_parser.extract_total_amount("TOTAL: 99.99") == "99.99"
    assert invoice_parser.extract_total_amount("Total Amount is not found") is None

def test_extract_company_name(invoice_parser):
    assert invoice_parser.extract_company_name("Invoice from ACME Corp") == "ACME Corp"
    assert invoice_parser.extract_company_name("Factura de Compañía XYZ") == "Compañía XYZ"
    assert invoice_parser.extract_company_name("  Supplier:  Example Inc. ") == "Example Inc."
    assert invoice_parser.extract_company_name("No Company Name Here") is None

def test_extract_line_items(invoice_parser):
    invoice_text = """
    Item 1    $10.00
    Item 2    $20.00
    """
    expected_items = ["Item 1    $10.00", "Item 2    $20.00"]
    assert invoice_parser.extract_line_items(invoice_text) == expected_items

    invoice_text_spanish = """
    Producto 1    10,00 €
    Producto 2    20,00 €
    """
    expected_items_spanish = ["Producto 1    10,00 €", "Producto 2    20,00 €"]
    assert invoice_parser.extract_line_items(invoice_text_spanish) == expected_items_spanish

    assert invoice_parser.extract_line_items("No items here") == []
