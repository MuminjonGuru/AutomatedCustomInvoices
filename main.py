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
  pass

def convert_html_to_pdf(html_content, output_filename='invoice.pdf'):
  pass    

def update_and_convert_html_to_pdf(items, customer_info, country_code, output_filename='invoice.pdf'):
  pass


# update_and_convert_html_to_pdf is the final function
