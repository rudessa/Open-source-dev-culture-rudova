import csv

def parse_csv(csv_string):
    """
    Parses a CSV-formatted string into a list of dictionaries.

    This function takes a CSV string, splits it into lines, and processes it into
    a structured format where each row is represented as a dictionary with column
    names as keys.

    Parameters:
        csv_string (str): The raw CSV content as a string.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a row 
        of the CSV file with column headers as keys.

    Example:
        Input:
            "name,age,city\nAlice,25,New York\nBob,30,Los Angeles"

        Output:
            [
                {"name": "Alice", "age": "25", "city": "New York"},
                {"name": "Bob", "age": "30", "city": "Los Angeles"}
            ]

    Raises:
        No explicit exceptions are raised, but malformed CSV input may cause unexpected behavior.
    """
    data = []
    lines = csv_string.strip().split("\n")

    if not lines:
        return data  # Return an empty list if there are no lines

    reader = csv.reader(lines)
    header = next(reader)  # Extract the header row

    for row in reader:
        row_dict = {}
        for col_name, value in zip(header, row):
            row_dict[col_name] = value.strip()  # Strip whitespace from values
        data.append(row_dict)

    return data
