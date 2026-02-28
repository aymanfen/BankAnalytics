import pandas as pd
from openpyxl import Workbook
import json
import os
import re


filename = "CDMQ32025.xlsx"

# Configuration
input_file = f"Reports/{filename}"
config_file = "ETL/indicators.json"
output_file = f"Reports/Cleaned/{filename}"


# -------------------------------------------------------
# Load Configuration
# -------------------------------------------------------
def load_config(config_file):
    file_ext = os.path.splitext(config_file)[1].lower()

    if file_ext == ".json":
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


# -------------------------------------------------------
# Normalize Indicator Names
# -------------------------------------------------------
def normalize_indicator(text):
    """
    Clean indicator name:
    - lowercase
    - remove everything from start until first letter OR digit
    - remove dots
    - remove +/- or ± inside text
    - normalize spaces
    """
    if not isinstance(text, str):
        return text

    text = text.strip().lower()

    # 🔥 Remove everything before first letter OR digit
    text = re.sub(r"^[^a-zA-Z0-9]+", "", text)

    # Remove dots
    text = text.replace(".", "")

    # Remove +/- and ± inside text
    text = text.replace("+/-", "")
    text = text.replace("±", "")

    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -------------------------------------------------------
# Number Detection
# -------------------------------------------------------
def is_number(s):
    s = s.strip()
    test = s.replace(" ", "").replace(",", "")

    if test.startswith("-"):
        test = test[1:]

    if test.startswith("(") and test.endswith(")"):
        test = test[1:-1]

    return test.isdigit()


# -------------------------------------------------------
# Process Sheet
# -------------------------------------------------------
def process_sheet(lines, indicator_names):
    result = []

    normalized_indicators = set(indicator_names)

    # Preserve first 3 rows (cleaned)
    if len(lines) >= 3:
        result.extend([normalize_indicator(x) for x in lines[:3]])
        i = 3
    else:
        i = 0

    while i < len(lines):

        original_line = lines[i]

        # Skip standalone numbers
        if is_number(original_line):
            i += 1
            continue

        normalized_line = normalize_indicator(original_line)

        # --------------------------------------------------
        # 1️⃣ Exact Match (ONLY if in JSON)
        # --------------------------------------------------
        if normalized_line in normalized_indicators:
            result.append(normalized_line)

            numbers = []
            j = i + 1

            while j < len(lines) and is_number(lines[j]) and len(numbers) < 2:
                numbers.append(lines[j])
                j += 1

            while len(numbers) < 2:
                numbers.append("-")

            result.extend(numbers)
            i = j
            continue

        # --------------------------------------------------
        # 2️⃣ Multi-line Match (ONLY if in JSON)
        # --------------------------------------------------
        combined = normalized_line
        j = i + 1
        found_match = False

        while j < len(lines) and not is_number(lines[j]):
            combined += " " + normalize_indicator(lines[j])

            if combined in normalized_indicators:
                found_match = True
                break

            j += 1

        if found_match:
            result.append(combined)

            numbers = []
            k = j + 1

            while k < len(lines) and is_number(lines[k]) and len(numbers) < 2:
                numbers.append(lines[k])
                k += 1

            while len(numbers) < 2:
                numbers.append("-")

            result.extend(numbers)
            i = k
            continue

        # --------------------------------------------------
        # ❌ NOT in JSON → IGNORE COMPLETELY
        # --------------------------------------------------
        i += 1

    return result

# -------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------

indicators_config = load_config(config_file)

# Normalize config indicators once
for sheet in indicators_config:
    indicators_config[sheet] = [
        normalize_indicator(ind) for ind in indicators_config[sheet]
    ]

excel_file = pd.ExcelFile(input_file)
sheet_names = excel_file.sheet_names

wb = Workbook()
wb.remove(wb.active)

for sheet_name in sheet_names:
    print(f"Processing sheet: {sheet_name}")

    df = pd.read_excel(input_file, sheet_name=sheet_name, header=None)

    raw_lines = df[0].dropna().astype(str).tolist()
    lines = [line.strip() for line in raw_lines if line.strip()]

    indicator_names = indicators_config.get(sheet_name, [])

    result = process_sheet(lines, indicator_names)

    ws = wb.create_sheet(title=sheet_name)

    

    for idx, value in enumerate(result, start=1):
        ws[f"A{idx}"] = value

    ws["A1"] = "Results"
    ws.column_dimensions["A"].width = 80

    print(f"  Completed: {len(result)} rows created")

wb.save(output_file)

print("\nAll sheets processed successfully!")
print(f"Output file saved as: {output_file}")
print(f"Total sheets processed: {len(sheet_names)}")
