import re

def extract_city_from_address(address):
    """
    Extract and normalize city name from address string.
    Supports formats like: "Kota Semarang", "Semarang City", "Semarang 50181", etc.
    """
    if not address:
        return None
    
    # Split by comma to analyze each part
    parts = [p.strip() for p in address.split(',')]
    
    # Priority 1: Look for "Kota xxx" or "Kabupaten xxx" in any part
    for part in parts:
        match = re.search(r'^(?:Kota|Kabupaten)\s+(.+)$', part, re.IGNORECASE)
        if match:
            city_name = match.group(1).strip()
            city_name = re.sub(r'\s+(?:City|city)$', '', city_name).strip()
            return city_name
    
    # Priority 2: Look for "xxx City" in any part
    for part in parts:
        match = re.search(r'^(.+?)\s+(?:City|city)$', part)
        if match:
            return match.group(1).strip()
    
    # Priority 3: Check last part for "CityName PostalCode" pattern
    if parts:
        last_part = parts[-1].strip()
        # Match pattern like "Semarang 50276"
        match = re.search(r'^(\D+?)\s+\d', last_part)
        if match:
            return match.group(1).strip()
    
    # Priority 4: Check second-to-last part if it doesn't look like postal code
    if len(parts) >= 2:
        second_last = parts[-2].strip()
        # Skip if it looks like province name
        province_keywords = ['java', 'jawa', 'sumatera', 'sulawesi', 'kalimantan', 'papua', 'riau', 'bengkulu', 'jambi', 'aceh', 'banten', 'yogyakarta', 'nusa', 'maluku', 'timur', 'barat']
        if not any(word in second_last.lower() for word in province_keywords):
            city_name = re.sub(r'^(?:Kec|Kota|Kabupaten|Kelurahan)\s+', '', second_last, flags=re.IGNORECASE).strip()
            if city_name and not city_name[0].isdigit():
                return city_name
    
    return None


# Test dengan data contoh
test_addresses = [
    "WCWP+3QP, Tembalang, Semarang City, Central Java 50275",
    "XC3C+C5 Tinjomoyo, Semarang City, Central Java",
    " Jl. Gondang Tim. II No.1, Bulusan, Kec. Tembalang, Kota Semarang, Jawa Tengah 50277",
    "Jl. Tembalang Baru No.11, Tembalang, Kec. Tembalang, Kota Semarang, Jawa Tengah 50275",
    "Jl. Panembahan Senopati No.274L, Ngaliyan, Semarang 50181",
    "Jl. Mangunharjo, Sambiroto, Tembalang, Semarang 50276",
]

print("Test extract_city_from_address():")
print("=" * 60)
for addr in test_addresses:
    city = extract_city_from_address(addr)
    print(f"Address: {addr[:50]}...")
    print(f"City: {city}")
    print(f"City (lower): {city.lower() if city else None}")
    print("---")

