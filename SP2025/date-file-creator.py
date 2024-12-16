import os
from datetime import datetime

def create_markdown_files(input_filename):
    """
    Read dates from a text file and create corresponding markdown files.
    
    Args:
        input_filename (str): Name of the input text file containing dates
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = "lectures"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Read dates from input file
        with open(input_filename, 'r') as file:
            dates = file.readlines()
        
        # Process each date
        for date_str in dates:
            # Strip whitespace and skip empty lines
            date_str = date_str.strip()
            if not date_str:
                continue
            
            # Parse the date string
            try:
                # Assuming input format is "MM.DD.YYYY.DAY"
                date_parts = date_str.split('.')
                if len(date_parts) != 4:
                    print(f"Skipping invalid date format: {date_str}")
                    continue
                
                # Create filename
                filename = f"DATA-5695-{date_str}.md"
                filepath = os.path.join(output_dir, filename)
                
                # Create markdown file with basic template
                with open(filepath, 'w') as md_file:
                    md_file.write(f"# {date_str}\n\n")
                    md_file.write("## Notes\n\n")
                    md_file.write("- \n\n")
                    md_file.write("## Tasks\n\n")
                    md_file.write("- [ ] \n")
                
                print(f"Created: {filename}")
                
            except Exception as e:
                print(f"Error processing date {date_str}: {str(e)}")
                
    except FileNotFoundError:
        print(f"Input file '{input_filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    input_filename = "dates.txt"  # Name of your input file
    create_markdown_files(input_filename)

if __name__ == "__main__":
    main()
