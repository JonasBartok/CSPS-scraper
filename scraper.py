import requests
import json
import time
import sys
from urllib.parse import quote_plus

class CzechSwimmingScraper:
    def __init__(self):
        self.base_url = "https://vysledky.czechswimming.cz/cz.zma.csps.portal.rest/api/public/search"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://vysledky.czechswimming.cz/',
            'Origin': 'https://vysledky.czechswimming.cz',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'max-age=0'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def search_person(self, name, surname):
        """Search for a person in the Czech Swimming database"""
        query = f"{name} {surname}"
        params = {'query': query}
        
        try:
            print(f"Searching for: {query}")
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            # Add a small delay to be respectful to the server
            time.sleep(0.5)
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching for {query}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response for {query}: {e}")
            return None
    
    def filter_pkhk_members(self, results):
        """Filter results to only include PKHK club members"""
        if not results:
            return []
        
        pkhk_members = []
        for person in results:
            if person.get('clubAbbrev') == 'PKHK':
                pkhk_members.append(person)
        
        return pkhk_members
    
    def read_names_from_file(self, filename):
        """Read names from input file"""
        names = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        # Split by space and assume first name is everything except last word
                        parts = line.split()
                        if len(parts) >= 2:
                            surname = parts[-1]
                            name = ' '.join(parts[:-1])
                            names.append((name, surname))
                        else:
                            print(f"Warning: Could not parse line: {line}")
        except FileNotFoundError:
            print(f"Error: File {filename} not found")
            return []
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            return []
        
        return names
    
    def write_results_to_file(self, results, output_filename):
        """Write PKHK members to output file"""
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                for person in results:
                    # Write name and surname on one line
                    f.write(f"{person['firstName']} {person['lastName']}\n")
                    # Write userId on the next line
                    f.write(f"{person['userId']}\n")
            
            print(f"Results written to {output_filename}")
            
        except Exception as e:
            print(f"Error writing to file {output_filename}: {e}")
    
    def run_scraper(self, input_filename, output_filename):
        """Main function to run the scraper"""
        print("Czech Swimming Scraper - Looking for PKHK members")
        print("=" * 50)
        
        # Read names from input file
        names = self.read_names_from_file(input_filename)
        if not names:
            print("No names to process.")
            return
        
        print(f"Found {len(names)} names to search for")
        
        all_pkhk_members = []
        
        # Search for each person
        for name, surname in names:
            results = self.search_person(name, surname)
            
            if results:
                pkhk_members = self.filter_pkhk_members(results)
                if pkhk_members:
                    print(f"✓ Found {len(pkhk_members)} PKHK member(s) for {name} {surname}")
                    all_pkhk_members.extend(pkhk_members)
                else:
                    print(f"✗ No PKHK members found for {name} {surname}")
            else:
                print(f"✗ No results found for {name} {surname}")
        
        # Write results to output file
        if all_pkhk_members:
            print(f"\nTotal PKHK members found: {len(all_pkhk_members)}")
            self.write_results_to_file(all_pkhk_members, output_filename)
        else:
            print("\nNo PKHK members found in the search results.")

def main():
    scraper = CzechSwimmingScraper()
    
    # Default filenames
    input_file = "names_list.txt"
    output_file = "pkhk_members.txt"
    
    # Allow command line arguments
    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    
    scraper.run_scraper(input_file, output_file)

if __name__ == "__main__":
    main()