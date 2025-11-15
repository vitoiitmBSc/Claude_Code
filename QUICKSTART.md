# Quick Start Guide - Material Properties Web Scraper

Get started with the Material Properties Web Scraper in 5 minutes!

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd Claude_Code

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### 1. Search for Materials

```bash
# Search for stainless steel
python src/material_scraper.py search "stainless steel 316"

# Search for aluminum alloys in MatWeb only
python src/material_scraper.py search "aluminum 6061" --source matweb
```

### 2. Find Materials for Specific Applications

```bash
# Find corrosion-resistant materials
python src/material_scraper.py search-app "high corrosion resistance"

# Find high-temperature materials
python src/material_scraper.py search-app "high temperature" --limit 5
```

### 3. Get Detailed Material Properties

```bash
# Get properties and export to JSON
python src/material_scraper.py get-properties <material_url> --export json --output material.json

# Export to Markdown
python src/material_scraper.py get-properties <material_url> --export markdown --output material.md
```

## Common Searches

### By Material Type
```bash
# Metals
python src/material_scraper.py search "titanium alloy"
python src/material_scraper.py search "bronze"
python src/material_scraper.py search "inconel"

# Polymers
python src/material_scraper.py search "PEEK polymer"
python src/material_scraper.py search "nylon"

# Ceramics
python src/material_scraper.py search "alumina ceramic"
python src/material_scraper.py search "silicon carbide"
```

### By Application
```bash
# Aerospace
python src/material_scraper.py search-app "aerospace lightweight"

# Marine
python src/material_scraper.py search-app "marine corrosion"

# High Temperature
python src/material_scraper.py search-app "high temperature oxidation"

# Cryogenic
python src/material_scraper.py search-app "cryogenic low temperature"

# Wear Resistance
python src/material_scraper.py search-app "wear resistant"
```

## Programmatic Usage

```python
from scrapers import MatWebScraper

# Search and get properties
with MatWebScraper() as scraper:
    # Search
    results = scraper.search("stainless steel 316")
    print(f"Found {len(results)} materials")

    # Get properties for first result
    if results:
        properties = scraper.get_material_properties(results[0]['url'])
        print(f"Material: {properties['name']}")
        print(f"Properties: {properties['mechanical_properties']}")
```

## Export Data

```bash
# Export search results to CSV
python src/material_scraper.py search "steel" --export csv --output steel_results.csv

# Export material properties to JSON
python src/material_scraper.py get-properties <url> --export json --output props.json

# Export to Markdown for documentation
python src/material_scraper.py get-properties <url> --export markdown --output props.md
```

## Examples

Run the comprehensive examples:

```bash
python examples/usage_examples.py
```

## Tips

1. **Rate Limiting**: The scraper automatically waits 2 seconds between requests to be respectful to servers

2. **Limit Results**: Use `--limit` to control the number of results:
   ```bash
   python src/material_scraper.py search "steel" --limit 5
   ```

3. **Multiple Databases**: Omit `--source` to search all databases, or specify one:
   ```bash
   python src/material_scraper.py search "titanium" --source matweb
   python src/material_scraper.py search "titanium" --source azom
   ```

4. **Error Handling**: The scraper has automatic retry logic for network errors

## Testing

Run the test suite:

```bash
python tests/test_basic.py
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [examples/usage_examples.py](examples/usage_examples.py) for code examples
- See [CLAUDE.md](CLAUDE.md) for development guidelines

## Common Use Cases

### Material Selection for Design
```bash
# Compare aluminum alloys
python src/material_scraper.py search "aluminum 2024 6061 7075" --limit 15 --export csv --output aluminum_comparison.csv
```

### Research Database Building
```python
from scrapers import MatWebScraper
from utils.export import export_to_json

materials = ["stainless steel 304", "aluminum 6061", "titanium Ti-6Al-4V"]

for material in materials:
    with MatWebScraper() as scraper:
        results = scraper.search(material)
        if results:
            props = scraper.get_material_properties(results[0]['url'])
            export_to_json(props, f'{material.replace(" ", "_")}.json')
```

### Quick Property Lookup
```bash
# Find and display properties
python src/material_scraper.py search "PEEK" --source azom --limit 1
```

## Troubleshooting

**No results found?**
- Check your internet connection
- Try a more general search term
- Try a different database with `--source`

**Slow performance?**
- This is normal - the scraper respects rate limits
- You can see progress in the logs

**Export failed?**
- Ensure the output directory exists
- Check you have write permissions

## Support

For more help:
- Check the [README.md](README.md)
- Review the [examples](examples/)
- Consult the inline documentation

---

Happy material searching! 🔍
