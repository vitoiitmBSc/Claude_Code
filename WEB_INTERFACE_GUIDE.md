# Material Selector Web Interface Guide

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the web server**:
   ```bash
   python app.py
   ```

3. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## How to Use

### Step 1: Describe Your Application

Enter a description of what you're building or what the material will be used for.

**Examples**:
- "aerospace structural components"
- "marine environment piping"
- "high-temperature furnace parts"
- "biomedical implants"
- "automotive engine components"

### Step 2: Specify Material Type (Optional)

If you have a preference for a specific type of material, enter it here.

**Examples**:
- "stainless steel"
- "aluminum alloy"
- "titanium"
- "polymer"
- "ceramic"
- "composite"

### Step 3: Add Required Characteristics

Click the "Add" button to include specific characteristics you need.

**Examples**:
- "corrosion resistant"
- "lightweight"
- "high strength"
- "heat resistant"
- "biocompatible"
- "electrically conductive"
- "wear resistant"

### Step 4: Set Property Requirements (Optional)

Enter specific numeric requirements for material properties:

#### Tensile Strength (MPa)
- Min: Minimum required tensile strength
- Max: Maximum acceptable tensile strength
- Example: Min 400, Max 800 for moderate strength applications

#### Density (g/cm³)
- Min: Minimum density
- Max: Maximum density
- Example: Max 3.0 for lightweight applications

#### Operating Temperature (°C)
- Min: Minimum operating temperature
- Max: Maximum operating temperature
- Example: -40 to 150 for outdoor automotive applications

#### Hardness (HRC/HB)
- Min: Minimum hardness
- Max: Maximum hardness
- Example: Min 50 for wear-resistant applications

### Step 5: Search

Click the "Find Materials" button to start the search. The system will:

1. Search multiple material databases (MatWeb, AZoM)
2. Retrieve detailed properties for matching materials
3. Evaluate each material against your requirements
4. Rank results by match score (0-100%)
5. Display results sorted by best match first

## Understanding Results

### Match Score
Each material receives a score from 0-100% based on:
- **Application match** (30%): How well the material suits your application
- **Property requirements** (40%): How well numeric properties match your specs
- **Material type** (15%): Match with your preferred material type
- **Characteristics** (15%): How well it matches required characteristics

### Material Cards
Each result shows:
- **Material Name**: Official designation/name
- **Source**: Which database provided the information
- **Match Score**: Percentage match to your requirements
- **Description**: Brief overview of the material
- **Applications**: Known uses for this material
- **Key Properties**: Important characteristics
- **Mechanical Properties**: Strength, hardness, etc.
- **Link**: View full details in the original database

## Example Scenarios

### Scenario 1: Aerospace Component

**Requirements**:
- Application: "aerospace structural component"
- Material Type: "aluminum alloy"
- Characteristics: ["lightweight", "high strength", "fatigue resistant"]
- Density: Max 3.0 g/cm³
- Tensile Strength: Min 400 MPa

**Expected Results**: Aluminum 7075, 6061, 2024 alloys with high scores

### Scenario 2: Marine Equipment

**Requirements**:
- Application: "saltwater marine environment"
- Characteristics: ["corrosion resistant", "durable"]
- No specific property ranges

**Expected Results**: Stainless steel 316, bronze alloys, titanium

### Scenario 3: High-Temperature Application

**Requirements**:
- Application: "furnace components"
- Characteristics: ["oxidation resistant", "high temperature"]
- Operating Temperature: Min 800°C

**Expected Results**: Superalloys, ceramics, refractory metals

### Scenario 4: Lightweight Consumer Product

**Requirements**:
- Application: "consumer electronics housing"
- Characteristics: ["lightweight", "easy to manufacture", "aesthetic"]
- Density: Max 2.0 g/cm³

**Expected Results**: Magnesium alloys, engineering polymers, aluminum

## Tips for Best Results

### 1. Start Broad, Then Refine
- Begin with just application and characteristics
- If too many results, add property constraints
- If no results, remove some constraints

### 2. Use Common Terms
- Use industry-standard terminology
- Examples: "corrosion resistant" not "doesn't rust"
- "high strength" not "very strong"

### 3. Be Realistic with Ranges
- Don't make ranges too narrow
- Consider measurement tolerances
- Leave some margin for variation

### 4. Prioritize Requirements
- Only add property ranges for critical requirements
- Too many constraints may eliminate good options
- Focus on 2-3 most important properties

### 5. Review Multiple Results
- Don't just pick the top result
- Check multiple high-scoring materials
- Click through to see full specifications
- Consider trade-offs between properties

## Technical Details

### How Evaluation Works

The evaluation engine:
1. **Searches databases** using your application/material type as keywords
2. **Retrieves properties** for up to 15 top search results
3. **Scores each material** across four dimensions:
   - Application relevance
   - Property matching
   - Material type matching
   - Characteristic matching
4. **Weights scores** based on importance
5. **Ranks materials** by total weighted score

### Data Sources

Materials data comes from:
- **MatWeb**: Comprehensive material property database
- **AZoM**: Materials science and engineering resources

All data is retrieved in real-time from these sources.

### Limitations

- **Coverage**: Only materials in MatWeb/AZoM databases
- **Properties**: Some materials may have incomplete data
- **Real-time**: Searches can take 10-30 seconds
- **Accuracy**: Scores are algorithmic estimates, not engineering analysis
- **Network**: Requires internet connection

## Troubleshooting

### No Results Found

**Problem**: Search returns no materials

**Solutions**:
- Check if at least one field is filled (application OR material type)
- Remove very specific property constraints
- Try more general search terms
- Check internet connection

### Low Match Scores

**Problem**: All results have low scores (< 50%)

**Meaning**: No materials match your requirements well

**Solutions**:
- Relax some requirements
- Reconsider if requirements are realistic
- Try different characteristic keywords
- Widen property ranges

### Slow Searches

**Problem**: Search takes a long time

**Reason**: System is:
- Searching multiple databases
- Retrieving detailed properties
- Evaluating against requirements

**Normal duration**: 15-30 seconds

**If longer**:
- Check internet connection
- Database might be slow
- Try again later

### Error Messages

**Problem**: Red error message appears

**Common causes**:
- Network connectivity issues
- Database temporarily unavailable
- Server error

**Solutions**:
- Wait a moment and try again
- Check internet connection
- Refresh the page

## Advanced Usage

### Combining Constraints

You can combine multiple types of constraints:

```
Application: "automotive brake system"
Material Type: "steel"
Characteristics: ["wear resistant", "high strength"]
Tensile Strength: Min 600 MPa
Hardness: Min 45 HRC
```

This will find high-strength, wear-resistant steels suitable for brakes.

### Comparative Analysis

To compare material classes:

1. First search: Material Type = "aluminum alloy"
2. Note top results and scores
3. Second search: Material Type = "titanium alloy"
4. Compare scores and properties

### Property-First Search

If you know exact requirements but not application:

1. Leave Application blank
2. Add Characteristics
3. Set all relevant property ranges
4. Material Type optional

## Support

If you encounter issues:

1. Check this guide
2. Review example scenarios
3. Try simplifying requirements
4. Check console for error messages
5. Report issues on GitHub

---

**Happy Material Hunting!** 🔍
