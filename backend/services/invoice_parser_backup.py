from google.cloud import vision
import re

def extract_invoice_data(image_path):
    """
    Extracts data from an invoice image using Google Cloud Vision API.

    Args:
        image_path: Path to the invoice image file.

    Returns:
        A dictionary containing the extracted data, or None on error.
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(
            '{}\\nFor more info on error messages, check: '.format(
                response.error.message) + 'https://cloud.google.com/apis/design/errors')

    data = {}
    full_text = response.full_text_annotation.text
    # Improved extraction using more robust methods (can be further refined)
    invoice_number_match = re.search(r"Invoice\\s*No\\.?\\s*(\\S+)", full_text, re.IGNORECASE)
    if invoice_number_match:
        data["invoice_number"] = invoice_number_match.group(1)

    date_match = re.search(r"Date\\s*(\\S+)", full_text, re.IGNORECASE)
    if date_match:
        data["date"] = date_match.group(1)

    total_match = re.search(r"Total\\s*\\$?(\\d+\\.?\\d*)", full_text, re.IGNORECASE)
    if total_match:
        data["total_amount"] = total_match.group(1)

    return data

if __name__ == '__main__':
    # Example usage (for testing)
    # Replace 'path/to/your/invoice.jpg' with the actual path to an invoice image
    invoice_path = 'baked_goods_1.jpg'
    extracted_data = extract_invoice_data(invoice_path)
    if extracted_data:
        print("Extracted Data:")
        print(extracted_data)
    else:
        print("Error during extraction.")
