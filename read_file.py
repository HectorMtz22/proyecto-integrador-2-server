import pandas as pd
import matplotlib.pyplot as plt
file_data_location = 'data/R3DET 8.0.xlsx'
file_sheet = "TG"

def main():
    semestre = input("Ingresa el Periodo (e.g., A2020): ")
    data = load_data(file_data_location, file_sheet)
    filtered_data = filter_data(data, semestre)
    print(filtered_data)
    plot_egresados_titulados(filtered_data, semestre)
    plot_cambios_carrera(filtered_data, semestre)

def load_data(file_location, sheet_name):
    return pd.read_excel(file_location, sheet_name=sheet_name)

def filter_data(data, semestre):
    filtered_data = data[data['PE'] == 'ITS']
    filtered_data = filtered_data[filtered_data['CC'].str.contains('Cohorte', na=False)]
    return filtered_data[filtered_data['Cohorte'].str.lower() == semestre.lower()]

def plot_egresados_titulados(filtered_data, semestre):
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_data['Per'], filtered_data['Eg'], marker='o', color='blue')
    plt.plot(filtered_data['Per'], filtered_data['STit'], marker='o', color='green')
    plt.legend(['Egresados', 'Titulados'], loc='upper right')
    plt.title(f"Cantidad de alumnos ITS del periodo {semestre.upper()}")
    plt.xlabel('Periodo')
    plt.ylabel('Cantidad')
    plt.tight_layout()
    plt.gca().yaxis.get_major_locator().set_params(integer=True)
    plt.savefig(f"images/good_{semestre}.png")

def plot_cambios_carrera(filtered_data, semestre):
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_data['Per'], filtered_data['ECC6'], marker='o', color='red')
    plt.plot(filtered_data['Per'], filtered_data['ECC'], marker='o', color='orange')
    plt.gca().yaxis.get_major_locator().set_params(integer=True)
    plt.legend(['Cambio por 6ta oportunidad', 'Cambio de carrera'], loc='upper right')
    plt.title(f"Cantidad de alumnos ITS del periodo {semestre.upper()}")
    plt.xlabel('Periodo')
    plt.ylabel('Cantidad')
    plt.tight_layout()
    plt.savefig(f"images/bad_{semestre}.png")

if __name__ == "__main__":
    main()
