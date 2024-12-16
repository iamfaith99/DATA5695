from datetime import datetime, timedelta

def get_tuesdays_thursdays(start_date_str, end_date_str):
    """
    Generate a list of all Tuesdays and Thursdays between two dates.
    
    Args:
        start_date_str (str): Start date in 'YYYY-MM-DD' format
        end_date_str (str): End date in 'YYYY-MM-DD' format
        
    Returns:
        list: List of datetime objects for all Tuesdays and Thursdays
    """
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    # Find first Tuesday or Thursday after start date
    current_date = start_date
    while current_date.weekday() not in [1, 3]:  # 1 = Tuesday, 3 = Thursday
        current_date += timedelta(days=1)
    
    # Generate list of dates
    dates = []
    while current_date <= end_date:
        if current_date.weekday() in [1, 3]:
            dates.append(current_date)
        current_date += timedelta(days=1)
    
    return dates

# Generate dates
start_date = "2025-01-06"
end_date = "2025-05-02"

dates = get_tuesdays_thursdays(start_date, end_date)

# Print the dates
print(f"Tuesdays and Thursdays between {start_date} and {end_date}:")
print("-" * 50)

# Dictionary to map weekday numbers to three-letter abbreviations
day_abbrev = {
    1: "TUE",
    3: "THU"
}

for date in dates:
    # Format: MM.DD.YYYY.DAY
    formatted_date = f"{date.strftime('%m.%d.%Y')}.{day_abbrev[date.weekday()]}"
    print(formatted_date)
