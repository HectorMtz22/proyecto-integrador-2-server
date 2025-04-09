import pandas as pd
file_data_location = 'data/R3DET 8.0.xlsx'
file_sheet = "TG"

semestre = input("Ingresa el Periodo (e.g., A2020): ")

# Check the second sheet
data = pd.read_excel(file_data_location, sheet_name=file_sheet)

# Filter the data to include only rows where the column PE is ITS
filtered_data = data[data['PE'] == 'ITS']
# Filter data to include only Cohorte on the CC column
filtered_data = filtered_data[filtered_data['CC'].str.contains('Cohorte', na=False)]
# Filter data to include only rows where the column Semestre matches the input
filtered_data = filtered_data[filtered_data['Cohorte'].str.lower() == semestre.lower()]

# Display the filtered data
print(filtered_data)
