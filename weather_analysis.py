
import csv
from datetime import datetime
import matplotlib.pyplot as plt

def load_data(file_path):
    data_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Ler o cabeçalho
        for row in reader:
            data_list.append(row)
    return data_list

def filter_data_by_date(data, start_date, end_date):
    start_date_obj = datetime.strptime(start_date, "%m/%Y")
    end_date_obj = datetime.strptime(end_date, "%m/%Y")
    filtered_data = []
    for row in data:
        date_obj = datetime.strptime(row[0], "%d/%m/%Y")
        if start_date_obj <= date_obj <= end_date_obj:
            filtered_data.append(row)
    return filtered_data

def display_data(data, data_type):
    headers_map = {
        1: ["data", "precip", "maxima", "minima", "um_relativa", "vel_vento"],
        2: ["data", "precip"],
        3: ["data", "maxima", "minima"],
        4: ["data", "um_relativa", "vel_vento"]
    }
    headers = ["data", "precip", "maxima", "minima", "um_relativa", "vel_vento"]
    selected_headers = headers_map[data_type]
    display_list = [selected_headers]
    for row in data:
        display_row = [row[headers.index(header)] for header in selected_headers]
        display_list.append(display_row)
    return display_list

def get_month_year_with_least_rain(data):
    monthly_rain = {}
    for row in data:
        month_year = row[0][3:]
        rain = float(row[1])
        monthly_rain[month_year] = monthly_rain.get(month_year, 0) + rain

    least_rain_month_year = min(monthly_rain, key=monthly_rain.get)
    least_rain_value = monthly_rain[least_rain_month_year]

    return least_rain_month_year, least_rain_value

def average_min_temp_for_month(data, month):
    yearly_avg_min_temps = {}
    total_min_temps = []
    for year in range(2006, 2017):
        monthly_min_temps = [float(row[3]) for row in data if row[0][3:5] == month and int(row[0][6:]) == year]
        if monthly_min_temps:
            avg_temp_for_year = sum(monthly_min_temps) / len(monthly_min_temps)
            yearly_avg_min_temps[year] = avg_temp_for_year
            total_min_temps.extend(monthly_min_temps)
    
    if total_min_temps:
        overall_avg = sum(total_min_temps) / len(total_min_temps)
    else:
        overall_avg = 0
    
    return yearly_avg_min_temps, overall_avg

def plot_avg_min_temp(data, month):
    yearly_avg_min_temps, _ = average_min_temp_for_month(data, month)
    years = list(yearly_avg_min_temps.keys())
    avg_temps = list(yearly_avg_min_temps.values())
    plt.figure(figsize=(10,6))
    plt.bar(years, avg_temps, color='lightblue')
    plt.title(f"Médias de Temperatura Mínima para o mês {month}/2006-2016")
    plt.xlabel("Ano")
    plt.ylabel("Temperatura Mínima Média (°C)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def main():
    data = load_data("Anexo_Arquivo_Dados_Projeto_Logica_e_programacao_de_computadores.csv")
    # Interface de usuário simples
    while True:
        print("\nMenu:")
        print("1. Visualizar intervalo de dados")
        print("2. Ver mês/ano com menor precipitação")
        print("3. Média da temperatura mínima de um mês entre 2006-2016")
        print("4. Gráfico da média da temperatura mínima de um mês entre 2006-2016")
        print("5. Sair")
        choice = input("Escolha uma opção: ")
        if choice == "1":
            start_date = input("Informe o mês/ano inicial (formato mm/aaaa): ")
            end_date = input("Informe o mês/ano final (formato mm/aaaa): ")
            data_type = int(input("Escolha o tipo de dado (1: Todos, 2: Precipitação, 3: Temperatura, 4: Umidade e Vento): "))
            filtered_data = filter_data_by_date(data, start_date, end_date)
            displayed_data = display_data(filtered_data, data_type)
            for row in displayed_data:
                print(" | ".join(row))
        elif choice == "2":
            month_year, rain_value = get_month_year_with_least_rain(data)
            print(f"O mês/ano com a menor precipitação foi {month_year} com {rain_value}mm.")
        elif choice == "3":
            month = input("Informe o mês (formato mm): ")
            # Garantindo que o mês tenha dois dígitos
            month = month.zfill(2)
            yearly_avg, overall_avg = average_min_temp_for_month(data, month)
            for year, avg in yearly_avg.items():
                print(f"Média de temperatura mínima em {month}/{year}: {avg:.2f}°C")
            print(f"Média geral da temperatura mínima para todos os meses de {month} entre 2006-2016: {overall_avg:.2f}°C")
        elif choice == "4":
            month = input("Informe o mês (formato mm): ")
            # Garantindo que o mês tenha dois dígitos
            month = month.zfill(2)
            plot_avg_min_temp(data, month)
        elif choice == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()
