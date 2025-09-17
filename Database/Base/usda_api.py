import os
import requests
import re

# ========= CONFIG =========
API_KEY = "aCrTfyqv6LOLNUnoumPFEsuJ8v0srNS670PleDrX"
SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
DETAIL_URL = "https://api.nal.usda.gov/fdc/v1/food/{}"
# ==========================

# Expand/modify this dictionary if you want more coverage
ALLERGEN_KEYWORDS = {
    "milk/dairy": ["milk", "lactose", "whey", "casein", "butter", "cream", "milk chocolate"],
    "peanuts": ["peanut", "peanuts", "peanut butter"],
    "tree nuts": ["almond", "hazelnut", "cashew", "pistachio", "pecan", "walnut", "brazil nut", "macadamia", "coconut"],
    "soy": ["soy", "soya", "soybean", "soy lecithin"],
    "gluten/wheat": ["wheat", "barley", "rye", "malt", "spelt"],
    "eggs": ["egg", "albumen", "egg white", "egg yolk"],
    "fish": ["fish", "salmon", "tuna", "anchovy", "cod"],
    "shellfish": ["shrimp", "crab", "lobster", "prawn"],
    "sesame": ["sesame", "tahini", "sesamol"],
    "mustard": ["mustard"],
}

def jq_search(food_name, page_size=3):
    params = {"query": food_name, "pageSize": page_size, "api_key": API_KEY}
    r = requests.get(SEARCH_URL, params=params, timeout=15)
    r.raise_for_status()
    return r.json().get("foods", [])

def get_food_details(fdc_id):
    r = requests.get(DETAIL_URL.format(fdc_id), params={"api_key": API_KEY}, timeout=15)
    r.raise_for_status()
    return r.json()

def normalize_text_field(x):
    if not x:
        return ""
    if isinstance(x, list):
        return " ".join([str(i) for i in x])
    return str(x)

def detect_allergens_from_text(text):
    text = (text or "").lower()
    found = set()
    # normalize punctuation
    text_for_search = re.sub(r"[^\w']", " ", text)
    for allergen, keywords in ALLERGEN_KEYWORDS.items():
        for kw in keywords:
            pattern = r"\b" + re.escape(kw.lower()) + r"\b"
            if re.search(pattern, text_for_search):
                found.add(allergen)
                break
    return found

def extract_nutrients(food_detail):
    nutrients = {}

    # 1. foodNutrients (generic/common foods)
    for n in food_detail.get("foodNutrients", []) or []:
        name = n.get("nutrientName", "").lower()
        val = n.get("value")
        unit = n.get("unitName")
        if not name or val is None:
            continue
        nutrients[name] = (val, unit)

    # 2. labelNutrients (branded/packaged products)
    ln = food_detail.get("labelNutrients") or {}
    for key, v in ln.items():
        if isinstance(v, dict) and "value" in v:
            unit = "g"
            if key.lower() in ["calories", "energy"]:
                unit = "kcal"
            nutrients[key.lower()] = (v["value"], unit)

    return nutrients

def pretty_calories(nutrients):
    for key in ["energy", "calories"]:
        if key in nutrients:
            val, unit = nutrients[key]
            return f"{val} {unit}"
    return "N/A"

def pretty_protein(nutrients):
    for key in nutrients:
        if "protein" in key:
            val, unit = nutrients[key]
            return f"{val} {unit}"
    return "N/A"

def search_and_report(food_name):
    try:
        foods = jq_search(food_name)
    except requests.RequestException as e:
        return {"error": f"Network/API error during search: {e}"}

    if not foods:
        return {"error": f"No USDA results found for: {food_name}"}

    candidate = foods[0]
    fdc_id = candidate.get("fdcId")
    description = normalize_text_field(candidate.get("description"))
    brand = candidate.get("brandOwner") or candidate.get("brandName") or "N/A"
    search_ingredients = normalize_text_field(candidate.get("ingredients"))

    # fetch detailed record
    details = {}
    try:
        if fdc_id:
            details = get_food_details(fdc_id)
    except requests.RequestException:
        details = {}

    # gather text for allergen detection
    detail_ingredients = normalize_text_field(details.get("ingredients"))
    other_text = " ".join(filter(None, [
        description,
        brand,
        search_ingredients,
        detail_ingredients,
        normalize_text_field(details.get("dataType")),
        normalize_text_field(details.get("foodCategory")),
        normalize_text_field(details.get("subtypeDescription"))
    ])).strip()

    detected_allergens = detect_allergens_from_text(other_text)

    # nutrients (calories/protein)
    nutrients = extract_nutrients(details or candidate)
    calories = pretty_calories(nutrients)
    protein = pretty_protein(nutrients)

    return {
        "fdcId": fdc_id,
        "name": description,
        "brand": brand,
        "calories": calories,
        "protein": protein,
        "ingredients_search": search_ingredients or "N/A",
        "ingredients_details": detail_ingredients or "N/A",
        "allergens": sorted(detected_allergens) if detected_allergens else ["No major allergens found"],
    }

if __name__ == "__main__":
    term = input("Enter food to search: ").strip()
    if not term:
        print("Please type a food name (e.g. 'Peanut M&M').")
    else:
        result = search_and_report(term)
        print(result)