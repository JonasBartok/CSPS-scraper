# Czech Swimming PKHK Scraper

This scraper searches the Czech Swimming database for people and filters results to show only members of the PKHK club.

## How it works

1. Reads a list of names from `names_list.txt` (one name per line: "FirstName LastName")
2. Searches the Czech Swimming API for each person
3. Filters results to only include members of the PKHK club
4. Writes the results to `pkhk_members.txt` in the format:
   ```
   Name Surname
   userId
   ```

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `names_list.txt` file with names to search for:
   ```
   Jonáš BARTOK
   John Smith
   Anna Novakova
   ```

3. Run the scraper:
   ```bash
   python3 scraper.py
   ```

   Or specify custom input/output files:
   ```bash
   python3 scraper.py input_names.txt output_results.txt
   ```

## Files

- `scraper.py` - Main scraper script
- `names_list.txt` - Sample input file with names to search for
- `pkhk_members.txt` - Output file with PKHK club members found
- `requirements.txt` - Python dependencies

## API

The scraper uses the Czech Swimming Federation's public search API:
`https://vysledky.czechswimming.cz/cz.zma.csps.portal.rest/api/public/search`

The scraper mimics browser behavior with appropriate headers to ensure compatibility.