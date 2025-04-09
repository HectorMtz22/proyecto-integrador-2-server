import pandas as pd
import matplotlib.pyplot as plt
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

# Plotting the data
# First plot Egresados and Titulados
plt.figure(figsize=(10, 5))
plt.plot(filtered_data['Per'], filtered_data['Eg'], marker='o', color='blue')
plt.plot(filtered_data['Per'], filtered_data['STit'], marker='o', color='green')
plt.legend(['Egresados', 'Titulados'], loc='upper right')
plt.title(f"Cantidad de alumnos ITS del periodo {semestre.upper()}")
plt.xlabel('Periodo')
plt.ylabel('Cantidad')
plt.tight_layout()
plt.gca().yaxis.get_major_locator().set_params(integer=True)

# Save image
plt.savefig(f"images/good_{semestre}.png")

# New plot
# Cambios de carrera y 6ta oportunidad
plt.figure(figsize=(10, 5))
plt.plot(filtered_data['Per'], filtered_data['ECC6'], marker='o', color='red')
plt.plot(filtered_data['Per'], filtered_data['ECC'], marker='o', color='orange')

plt.gca().yaxis.get_major_locator().set_params(integer=True)
plt.legend(['Cambio por 6ta oportunidad', 'Cambio de carrera'], loc='upper right')
plt.title(f"Cantidad de alumnos ITS del periodo {semestre.upper()}")
plt.xlabel('Periodo')
plt.ylabel('Cantidad')
plt.tight_layout()
# Save image
plt.savefig(f"images/bad_{semestre}.png")
