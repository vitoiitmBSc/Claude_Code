# Material Properties Web Scraper & Selector

A comprehensive Python tool for fetching material properties from professional databases including MatWeb, AZoM, and other materials science resources. Now featuring an intelligent web interface for material selection based on your requirements!

## Features

- **Web Interface**: User-friendly web application for material selection
- **Intelligent Material Evaluation**: AI-powered ranking based on your requirements
- **Multiple Database Support**: Search across MatWeb, AZoM, and more
- **Comprehensive Property Extraction**: Physical, mechanical, thermal, electrical properties
- **Application-Based Search**: Find materials suitable for specific applications
- **Multiple Export Formats**: JSON, CSV, Markdown
- **Rate Limiting**: Respectful scraping with configurable delays
- **Error Handling**: Robust retry logic and error recovery
- **CLI Interface**: Easy-to-use command-line tool
- **Programmatic API**: Use as a Python library in your projects

## Supported Databases

### MatWeb (www.matweb.com)
- Comprehensive material property database
- Metals, polymers, ceramics, composites, semiconductors
- Detailed datasheets with extensive properties

### AZoM (www.azom.com)
- Materials science and engineering database
- Technical articles and material datasheets
- Wide range of material categories

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Claude_Code
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web Interface (Recommended for Material Selection)

The easiest way to find materials is using the web interface:

1. **Start the web application**:
   ```bash
   python app.py
   ```

2. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

3. **Enter your requirements**:
   - Describe your application (e.g., "aerospace components", "marine environment")
   - Specify material type if preferred (e.g., "aluminum alloy", "stainless steel")
   - Add required characteristics (e.g., "corrosion resistant", "lightweight")
   - Set property ranges if needed (tensile strength, density, temperature, hardness)

4. **Get results**:
   - Materials are automatically ranked by how well they match your requirements
   - View detailed properties, applications, and specifications
   - Each material gets a match score (0-100%)
   - Click through to see full database entries

**Example Use Case**:
- Application: "high-temperature aerospace component"
- Characteristics: ["lightweight", "oxidation resistant", "high strength"]
- Temperature Range: 500-1000°C
- The system will search databases, evaluate materials, and return ranked results!

### Command Line Interface

The tool provides a CLI for easy access to material data.

#### Search for Materials

```bash
# Basic search
python src/material_scraper.py search "stainless steel 316"

# Search specific database
python src/material_scraper.py search "aluminum alloy" --source matweb

# Limit results
python src/material_scraper.py search "titanium" --limit 5

# Export results
python src/material_scraper.py search "copper" --export json --output results.json
```

#### Get Material Properties

```bash
# Get detailed properties from URL
python src/material_scraper.py get-properties "https://www.matweb.com/..."

# Export to different formats
python src/material_scraper.py get-properties <url> --export json --output material.json
python src/material_scraper.py get-properties <url> --export markdown --output material.md
python src/material_scraper.py get-properties <url> --export csv --output material.csv
```

#### Search by Application

```bash
# Find materials for specific applications
python src/material_scraper.py search-app "high corrosion resistance"
python src/material_scraper.py search-app "high temperature" --export csv --output high_temp.csv
python src/material_scraper.py search-app "aerospace" --limit 10
```

### Programmatic Usage

Use the scraper as a Python library in your projects:

```python
from scrapers import MatWebScraper, AZoMScraper

# Search for materials
with MatWebScraper() as scraper:
    results = scraper.search("stainless steel 316")

    for result in results:
        print(f"{result['name']}: {result['url']}")

    # Get detailed properties
    if results:
        properties = scraper.get_material_properties(results[0]['url'])
        print(properties['mechanical_properties'])
```

#### Search by Application

```python
with MatWebScraper() as scraper:
    # Find corrosion-resistant materials
    results = scraper.search_by_application("high corrosion resistance")

    for material in results:
        print(material['name'])
```

#### Export Data

```python
from utils.export import export_to_json, export_to_markdown

# Export to JSON
export_to_json(properties, 'material.json')

# Export to Markdown
export_to_markdown(properties, 'material.md')
```

#### Search Multiple Databases

```python
from scrapers import MatWebScraper, AZoMScraper

query = "titanium alloy"
all_results = []

# Search MatWeb
with MatWebScraper() as scraper:
    results = scraper.search(query)
    all_results.extend(results)

# Search AZoM
with AZoMScraper() as scraper:
    results = scraper.search(query)
    all_results.extend(results)

print(f"Found {len(all_results)} total results")
```

## Examples

Check out the `examples/usage_examples.py` file for comprehensive examples:

```bash
python examples/usage_examples.py
```

Examples include:
1. Basic material search
2. Getting detailed properties
3. Searching by application
4. Searching multiple databases
5. Exporting data to files
6. Filtering results
7. Error handling
8. Custom rate limiting

## Application-Based Searches

The tool includes intelligent mapping for common applications:

| Application | Recommended Materials |
|-------------|----------------------|
| High Corrosion Resistance | Stainless steels, titanium alloys, nickel alloys |
| High Temperature | Superalloys, ceramics, refractory metals |
| Aerospace | Aluminum alloys, titanium alloys, composites |
| Marine | Marine grade stainless steel, bronze |
| Cryogenic | Aluminum alloys, austenitic stainless steels |
| Wear Resistant | Hardened steels, tool steels, ceramics |
| Lightweight | Aluminum, titanium, composites |

Example:
```bash
python src/material_scraper.py search-app "marine corrosion resistance"
```

## Data Extracted

The scraper extracts comprehensive material data:

### Physical Properties
- Density
- Melting point
- Boiling point
- Specific gravity
- Molecular weight

### Mechanical Properties
- Tensile strength
- Yield strength
- Elongation
- Hardness
- Young's modulus
- Impact resistance
- Fatigue strength

### Thermal Properties
- Thermal conductivity
- Coefficient of thermal expansion
- Specific heat capacity
- Maximum service temperature

### Electrical Properties
- Electrical resistivity
- Electrical conductivity
- Dielectric constant

### Chemical Composition
- Element percentages
- Alloy composition
- Material grades

### Additional Information
- Common applications
- Key properties
- Material notes
- Source database and URL

## Export Formats

### JSON
Complete material data in JSON format for programmatic use.

### CSV
Flattened property data in CSV format for spreadsheet analysis.

### Markdown
Human-readable format with formatted tables and sections.

## Best Practices

1. **Rate Limiting**: The default rate limit is 2 seconds between requests. Adjust if needed:
   ```python
   scraper = MatWebScraper(rate_limit=3.0)  # 3 seconds
   ```

2. **Error Handling**: Always use context managers or try-finally:
   ```python
   with MatWebScraper() as scraper:
       results = scraper.search("material")
   ```

3. **Export Data**: Save important results to files:
   ```python
   export_to_json(properties, 'backup.json')
   ```

4. **Limit Results**: Use the limit parameter to avoid excessive requests:
   ```bash
   python src/material_scraper.py search "steel" --limit 10
   ```

## Project Structure

```
Claude_Code/
├── src/
│   ├── scrapers/
│   │   ├── base_scraper.py      # Base scraper class
│   │   ├── matweb_scraper.py    # MatWeb scraper
│   │   └── azom_scraper.py      # AZoM scraper
│   ├── utils/
│   │   ├── parser.py            # HTML parsing utilities
│   │   └── export.py            # Export utilities
│   ├── material_scraper.py      # Main CLI tool
│   └── material_evaluator.py    # Material evaluation engine
├── templates/
│   ├── index.html               # Web interface
│   └── about.html               # About page
├── examples/
│   └── usage_examples.py        # Usage examples
├── app.py                       # Flask web application
├── requirements.txt             # Dependencies
├── README.md                    # This file
└── CLAUDE.md                    # AI assistant guide
```

## Common Use Cases

### 1. Material Selection for Engineering Projects
```bash
python src/material_scraper.py search-app "aerospace lightweight" --export csv --output aerospace_materials.csv
```

### 2. Research and Comparison
```bash
# Compare multiple stainless steel grades
python src/material_scraper.py search "stainless steel 304 316 410" --limit 20
```

### 3. Database Building
```python
# Build a custom materials database
materials = ["aluminum 6061", "steel 4140", "titanium Ti-6Al-4V"]

for material in materials:
    with MatWebScraper() as scraper:
        results = scraper.search(material)
        if results:
            props = scraper.get_material_properties(results[0]['url'])
            export_to_json(props, f'{material.replace(" ", "_")}.json')
```

### 4. Material Property Lookup
```bash
# Quick lookup of specific material
python src/material_scraper.py search "PEEK polymer" --source azom
```

## Troubleshooting

### No Results Found
- Check your internet connection
- Verify the search query is spelled correctly
- Try a more general search term
- Try a different database with `--source`

### Rate Limiting Errors
- Increase the rate limit: `rate_limit=3.0`
- The scraper has automatic retry logic
- Wait a few minutes before retrying

### Export Failures
- Ensure the output directory exists
- Check file permissions
- Verify disk space

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Follow PEP 8 style guidelines
4. Add tests for new functionality
5. Submit a pull request

See `CLAUDE.md` for detailed development guidelines.

## License

This tool is for educational and research purposes. Please respect the terms of service of the databases you access.

## Disclaimer

This tool is designed for legitimate research and educational purposes. Users are responsible for:
- Complying with website terms of service
- Respecting rate limits
- Not overwhelming servers with requests
- Using data ethically and legally

The scrapers implement respectful rate limiting and identify themselves with a proper User-Agent header.

## Future Enhancements

Planned features:
- [ ] Support for more databases (Total Materia, ASM)
- [ ] Graphical comparison of materials
- [ ] Database caching for offline access
- [ ] Integration with CAD/FEA software
- [ ] RESTful API interface
- [x] Web interface
- [x] Advanced filtering by property ranges
- [x] Material recommendation engine

## Support

For issues, questions, or suggestions:
- Check the examples in `examples/usage_examples.py`
- Review this README
- Consult `CLAUDE.md` for development details
- Open an issue on GitHub

## Acknowledgments

This tool aggregates data from:
- [MatWeb](https://www.matweb.com/) - Material Property Data
- [AZoM](https://www.azom.com/) - Materials Science Database

Please support these excellent resources!

---

**Version**: 1.0.0
**Last Updated**: 2025-11-15
**Maintained By**: vitoiitmBSc
