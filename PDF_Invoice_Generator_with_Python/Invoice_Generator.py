import json
from fpdf import FPDF
import argparse

class InvoiceGenerator(FPDF):

    #Add header
    def header(self):
        self.set_y(5)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'INVOICE', border = 0, ln = 1, align='C')
        self.ln(10)

    #Add Business with Business Name, and address
    def add_business(self, business_name, business_address):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 5, business_name, border = 0, ln = 1, align='L')
        self.ln(2)
        self.set_font('Arial', '', 12)
        self.cell(0, 5, business_address, border = 0, ln = 1, align='L')
        self.ln(10)
    
    #Add Customer info with Customer name and address
    def add_customer_info(self, customer_name, customer_address):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 5, customer_name, border = 0, ln = 1, align = 'L')
        self.ln(2)
        self.set_font('Arial', '', 12)
        self.cell(0, 5, customer_address, border = 0, ln = 1, align = 'L')
        self.ln(10)

    #Add footer
    def footer(self):
        # Add the footer with page numbers
        self.set_y(-10)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    #Add Customer info with Customer name and address
    def add_items_table(self, items, tax_rate):
        
        #add table header
        self.set_font('Arial', 'B', 10)
        self.cell(80, 10, 'Description', border = 1)
        self.cell(30, 10, 'Quantity', border = 1, align = 'C')
        self.cell(40, 10, 'Unit Price', border = 1, align = 'C')
        self.cell(40, 10, 'Total', border = 1, align = 'C')
        self.ln()

        #Add items into the table
        self.set_font('Arial', '', 10)
        subtotal = 0

        for item in items:
            total = round(item['quantity'] * item['unit_price'], 2)
            self.cell(80, 10, item['description'], border = 1)
            self.cell(30, 10, str(item['quantity']), border = 1, align = 'C')
            self.cell(40, 10, str(item['unit_price']), border=1, align = 'C')
            self.cell(40, 10, str(total), border = 1, align = 'C')
            self.ln()        
            subtotal += total
        
        #calculate Tax and total
        tax = subtotal * tax_rate
        grand_total = subtotal + tax

        #Add subtotal, tax and total
        self.ln(5)
        self.set_font('Arial', 'B', 10)
        

        self.cell(150, 10, 'Subtotal', border=1, align='R')
        self.cell(40, 10, f'${subtotal:.2f}', border=1, align='C')
        self.ln()
        self.cell(150, 10, 'Tax', border=1, align='R')
        self.cell(40, 10, f'${tax:.2f}', border=1, align='C')
        self.ln()
        self.cell(150, 10, 'Total', border=1, align='R')
        self.cell(40, 10, f'${grand_total:.2f}', border=1, align='C')

        

def generate_invoice(json_file, pdf_output_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    pdf = InvoiceGenerator()
    pdf.add_page()
    pdf.add_business(data['business_name'], data['business_address'])
    pdf.add_customer_info(data['customer_name'], data['customer_address'])
    pdf.add_items_table(data['items'], 0.05)
    pdf.output(pdf_output_file, 'F')
    print('PDF file generated successfully!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Generate a PDF invoice from JSON input.')
    parser.add_argument('json_file', help='Path to the JSON file containing invoice data.')
    parser.add_argument('-o', '--output', default = 'Invoice.pdf', help='Output pdf file name.')
    args = parser.parse_args()

    generate_invoice(args.json_file, args.output)