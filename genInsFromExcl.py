import pandas as pd

def generate_insert_statements(file_path, table_name):
    # Lue Excel-tiedosto määritetyllä moottorilla
    df = pd.read_excel(file_path, engine='openpyxl')

    # Poista päällekkäiset rivit
    df = df.drop_duplicates()

    # Convert all numeric columns to strings to avoid trailing zeros
    for col in df.select_dtypes(include=['number']).columns:
        df[col] = df[col].apply(lambda x: str(int(x)) if pd.notna(x) else x)

    # Alusta lista, johon tallennetaan insert-lauseet
    insert_statements = []

    # Käy läpi DataFrame:n jokainen rivi
    for index, row in df.iterrows():
        # Ota sarakenimet ja arvot
        columns = ", ".join([f"[{col}]" for col in df.columns])
        values = ", ".join([f"NULL" if pd.isna(value) else f"'{str(value)}'" for value in row.values])

        # Luo insert-lause
        insert_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"

        # Lisää insert-lause listaan
        insert_statements.append(insert_statement)

    return insert_statements

def main():
    # Kysy Excel-tiedoston polku
    file_path = input("Please enter the Excel file path: ")

    # Kysy taulun nimi
    table_name = input("Please enter the table name: ")

    # Kysy tiedoston nimi ja sijainti, johon tallennetaan
    output_file_path = input("Please enter the output text file path (including file name): ")

    # Luo insert-lauseet
    insert_statements = generate_insert_statements(file_path, table_name)

    # Tallenna insert-lauseet tekstitiedostoon
    with open(output_file_path, 'w') as f:
        for statement in insert_statements:
            f.write(statement + '\n')

    print(f"Insert statements have been saved to {output_file_path}")

if __name__ == "__main__":
    main()