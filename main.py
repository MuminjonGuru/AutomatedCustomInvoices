import requests
import os

# or Securely load API keys from environment variables
VATLAYER_API_KEY = ''
PDFLAYER_API_KEY = ''

def calculate_vat(amount, country_code):
    """
    Calculates the VAT amount using the VATLayer API's 'price' endpoint.

    Args:
    amount (float): The original amount before VAT.
    country_code (str): The country code for which the VAT is calculated.

    Returns:
    float: The VAT amount.
    """
    url = f"http://apilayer.net/api/price?access_key={VATLAYER_API_KEY}&amount={amount}&country_code={country_code}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()

        if data.get('success'):
            price_excl_vat = data.get('price_excl_vat', 0)
            price_incl_vat = data.get('price_incl_vat', 0)
            return price_incl_vat - price_excl_vat
        else:
            raise ValueError("Error calculating VAT. API response unsuccessful.")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        raise

def generate_html_invoice(items, customer_info, subtotal, total_vat):
    """
    Generates the HTML content for the invoice.
    """
    items_html = "".join(
        f"<tr><td>{item['description']}</td><td>{item['quantity']}</td><td>${item['unit_price']}</td></tr>"
        for item in items
    )
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Invoice</title>
        <!-- Styles here -->
    </head>
    <body>
        <h1>Invoice #{customer_info['invoice_number']}</h1>
        <p>Date: {customer_info['date']}</p>
        <!-- Customer details here -->
        <h2>Invoice Details</h2>
        <table>
            <tr>
                <th>Description</th>
                <th>Quantity</th>
                <th>Unit Price</th>
            </tr>
            {items_html}
        </table>
        <h3>Summary</h3>
        <p>Subtotal: ${subtotal}</p>
        <p>VAT: ${total_vat}</p>
        <p>Total: ${subtotal + total_vat}</p>
    </body>
    </html>
    """
    return html_content

def convert_html_to_pdf(html_content, output_filename='invoice.pdf'):
    """
    Converts the given HTML content to a PDF using the PDFLayer API.
    """
    url = "http://api.pdflayer.com/api/convert"
    params = {
        'access_key': PDFLAYER_API_KEY,
    }
    data = {
        'document_html': html_content,
        'page_size': 'A4'
    }
    try:
        response = requests.post(url, params=params, data=data)
        response.raise_for_status()

        if response.headers.get('Content-Type', '').lower() == 'application/pdf':
            with open(output_filename, 'wb') as f:
                f.write(response.content)
        else:
            print("Error: Received non-PDF response.")
            print(response.content.decode('utf-8'))  # For debugging
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        raise

def update_and_convert_html_to_pdf(items, customer_info, country_code, output_filename='invoice.pdf'):
    """
    Updates the invoice HTML with given details, calculates VAT, and converts it to a PDF.
    """
    subtotal = sum(item['quantity'] * item['unit_price'] for item in items)
    total_amount = calculate_vat(subtotal, country_code)
    total_vat = total_amount - subtotal

    html_content = generate_html_invoice(items, customer_info, subtotal, total_vat)
    convert_html_to_pdf(html_content, output_filename)

# Example usage
items = [
    {"description": "Product 1", "quantity": 2, "unit_price": 50},
    {"description": "Service 1", "quantity": 1, "unit_price": 80}
]

customer_info = {
    "invoice_number": "12345",
    "date": "2023-11-29",
    "name": "John Doe",
    "address": "1234 Street, City, Country"
}

update_and_convert_html_to_pdf(items, customer_info, 'GB')
