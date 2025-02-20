import requests
import csv
import os
import glob

# Digi-Key API Credentials
CLIENT_ID = "YOUR_ID"
CLIENT_SECRET = "YOUR_SECRET"

# Digi-Key OAuth Token URL
TOKEN_URL = "https://api.digikey.com/v1/oauth2/token"

# Digi-Key Product Search API (base URL)
PRODUCT_SEARCH_URL = "https://api.digikey.com/products/v4/search/{}/productdetails"

# Function to find the latest BOM CSV file in the current directory
def find_bom_csv():
    csv_files = glob.glob("*BOM*.csv")  # Find all CSV files with "BOM" in the name
    if not csv_files:
        print("❌ No BOM CSV file found in the directory.")
        return None
    return max(csv_files, key=os.path.getctime)  # Get the most recently modified file

# Function to get a Bearer token
def get_bearer_token():
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    response = requests.post(TOKEN_URL, data=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"❌ Failed to get token: {response.json()}")
        return None

# Function to query Digi-Key API for a given part number
def get_part_details(part_number, token):
    url = PRODUCT_SEARCH_URL.format(part_number)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "X-DIGIKEY-Client-Id": CLIENT_ID
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n🔍 Details for {part_number}:")
        
        # Check each product variation for availability
        for variation in data["Product"].get("ProductVariations", []):
            package_name = variation["PackageType"]["Name"]
            quantity_available = variation["QuantityAvailableforPackageType"]

            print(f"  📦 Package: {package_name} | 🏷️ Digi-Key PN: {variation['DigiKeyProductNumber']}")
            print(f"  🏪 Available: {quantity_available}")

            if quantity_available == 0:
                print(f"  ❌ WARNING: {part_number} ({package_name}) is **out of stock**!")

    else:
        print(f"❌ Error fetching {part_number}: {response.json()}")

# Function to extract part numbers from a CSV file
def extract_part_numbers(csv_filename):
    with open(csv_filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row["MFG Part Number"].strip() for row in reader if row["MFG Part Number"].strip()]

# Find the latest BOM CSV file
csv_filename = find_bom_csv()
if not csv_filename:
    exit(1)

print(f"📂 Using BOM file: {csv_filename}")

# Extract part numbers from the CSV
mfg_part_numbers = extract_part_numbers(csv_filename)

# Get the Bearer token
bearer_token = get_bearer_token()

if bearer_token:
    # Query Digi-Key for each part number
    for part in mfg_part_numbers:
        get_part_details(part, bearer_token)
