import pandas as pd

# Sarakkeiden määritykset
column_types = {
    'Alv-koodi': 'nvarchar',
    'Nimi': 'nvarchar',
    'Tunnus': 'nvarchar',
    'Verotunnus': 'nvarchar',
    'Alue': 'nvarchar',
    'Verokanta': 'int',
    'Mava': 'int',
    'V/S-tili': 'nvarchar',
    'Eu-saatava': 'nvarchar',
    'Muu kirjaustili': 'nvarchar',
    'Kirjauskoodi': 'int',
    'Verokirjaus': 'nvarchar',
    'Laskelmaan': 'nvarchar',
    'Vientien verokäsittely': 'nvarchar',
    'Merkinkääntö': 'nvarchar',
    'VL VAT-koodi': 'nvarchar',
    'Alkukausi[1]': 'nvarchar',
    'Alv-lisäprosentti[1]': 'decimal',
    'Alv-vähennysprosentti[1]': 'decimal',
    'Alkukausi[2]': 'nvarchar',
    'Alv-lisäprosentti[2]': 'decimal',
    'Alv-vähennysprosentti[2]': 'decimal',
    'Alkukausi[3]': 'nvarchar',
    'Alv-lisäprosentti[3]': 'decimal',
    'Alv-vähennysprosentti[3]': 'decimal',
    'Alkukausi[4]': 'nvarchar',
    'Alv-lisäprosentti[4]': 'decimal',
    'Alv-vähennysprosentti[4]': 'decimal',
    'Alkukausi[5]': 'nvarchar',
    'Alv-lisäprosentti[5]': 'decimal',
    'Alv-vähennysprosentti[5]': 'decimal',
    'Alkukausi[6]': 'nvarchar',
    'Alv-lisäprosentti[6]': 'decimal',
    'Alv-vähennysprosentti[6]': 'decimal',
    'Alkukausi[7]': 'nvarchar',
    'Alv-lisäprosentti[7]': 'decimal',
    'Alv-vähennysprosentti[7]': 'decimal',
    'Alkukausi[8]': 'nvarchar',
    'Alv-lisäprosentti[8]': 'decimal',
    'Alv-vähennysprosentti[8]': 'decimal',
    'Ohjaus': 'int'
}

# lukee alkuperäisen arvon tyypin taulukosta ja muuttaa tarvittaessa vastaamaan SQLn saraketyyppiä
def transform_value(value, target_type):
    if target_type == 'int':
        return int(value)
    elif target_type == 'decimal':
        return float(value)
    elif target_type == 'nvarchar':
        return str(value)
    return value

def generate_insert_statements(file_path, table_name):
    # Read the Excel file with the specified engine
    df = pd.read_excel(file_path, engine='openpyxl')

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Initialize a list to store the insert statements
    insert_statements = []
    transformations = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Extract column names and values
        columns = ", ".join(df.columns)
        values = []
        for col, value in zip(df.columns, row.values):
            target_type = column_types[col]
            if pd.isna(value):
                values.append("NULL")
            else:
                try:
                    transformed_value = transform_value(value, target_type)
                    if transformed_value != value:
                        transformations.append(f"Transformed column '{col}' from {type(value).__name__} to {target_type}")
                    if target_type == 'nvarchar':
                        values.append(f"'{transformed_value}'")
                    else:
                        values.append(f"{transformed_value}")
                except ValueError:
                    values.append(f"'{value}'")

        # Create the insert statement
        insert_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({', '.join(values)});"
        
        # Append the insert statement to the list
        insert_statements.append(insert_statement)

    return insert_statements, transformations

def main():
    # Ask for the Excel file path
    file_path = input("Please enter the Excel file path: ")

    # Ask for the table name
    table_name = input("Please enter the table name: ")

    # Ask for the filename and location to save the file
    output_file_path = input("Please enter the output text file path (including file name): ")

    # Generate the insert statements
    insert_statements, transformations = generate_insert_statements(file_path, table_name)

    # Save the insert statements to a text file
    with open(output_file_path, 'w') as f:
        for statement in insert_statements:
            f.write(statement + '\n')

    # Print out the transformations
    if transformations:
        print("Transformations performed:")
        for transformation in transformations:
            print(transformation)

    print(f"Insert statements have been saved to {output_file_path}")

if __name__ == "__main__":
    main()