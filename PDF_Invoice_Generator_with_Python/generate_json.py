import json
import random

# List of random product names for descriptions
product_names = [
    "Laptop", "Mouse", "Keyboard", "Monitor", "Printer", "Tablet", "Router", 
    "Webcam", "Headset", "Smartphone", "Speaker", "Hard Drive", "Memory Stick", 
    "Charger", "Graphics Card", "Processor", "Motherboard", "Cooling Fan", 
    "Power Supply", "Network Switch", "USB Hub", "External SSD", "Microphone", 
    "Projector", "Stylus Pen"
]

# JSON structure
data_with_random_names = {
    "business_name": "Tech Solutions Inc.",
    "business_address": "123 Innovation Drive, Tech City, TX 75001",
    "customer_name": "Jane Doe",
    "customer_address": "456 Elm Street, Springfield, IL 62704",
    "items": [],
    "tax_rate": 0.07
}

# Generate 100 random items with random names from the product list
for i in range(1, 101):
    item = {
        "description": random.choice(product_names),
        "quantity": random.randint(1, 10),  # Random quantity between 1 and 10
        "unit_price": round(random.uniform(5.0, 500.0), 2)  # Random price between $5 and $500
    }
    data_with_random_names["items"].append(item)

# Save the JSON data to a file
output_file = "invoice_data.json"
with open(output_file, "w") as file:
    json.dump(data_with_random_names, file, indent=2)

print(f"JSON file with random product names saved as {output_file}")
