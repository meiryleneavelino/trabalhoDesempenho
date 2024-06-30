import json
import matplotlib.pyplot as plt
import csv
import numpy as np

# Caminho para o arquivo JSON
json_file_path = r'C:\Users\meiry\OneDrive\Área de Trabalho\packet-trace.json'

csv_file_path = r'C:\Users\meiry\OneDrive\Área de Trabalho\extracted_data.csv'

# Carregar o arquivo JSON
with open(json_file_path, 'r') as file:
    data = json.load(file)

extracted_data = []

# Extrair os dados relevantes
for entry in data:
    ts = entry['ts']
    for val in entry['val']:
        if 'ttl' in val and 'query' in val and 'success' in val and 'ip' in val and 'rtt' in val:
            extracted_data.append({
                'timestamp': ts,
                'ttl': val['ttl'],
                'query': val['query'],
                'success': val['success'],
                'ip': val['ip'],
                'hostname': val.get('hostname', 'N/A'),
                'as_owner': val.get('as', {}).get('owner', 'N/A'),
                'as_number': val.get('as', {}).get('number', 'N/A'),
                'rtt': val['rtt']
            })


# Converter os dados extraídos para um formato numpy
rtts = np.array([entry['rtt'] for entry in extracted_data])
ttls = np.array([entry['ttl'] for entry in extracted_data])

# Calcular estatísticas descritivas para RTT
mean_rtt = np.mean(rtts) #Média
variance_rtt = np.var(rtts) #variância
std_dev_rtt = np.std(rtts) #desvio padrão
min_rtt = np.min(rtts) #Mínimo
max_rtt = np.max(rtts) #Máximo

# Calcular estatísticas descritivas para TTL
mean_ttl = np.mean(ttls) #Média
variance_ttl = np.var(ttls) #variância
std_dev_ttl = np.std(ttls) #desvio padrão
min_ttl = np.min(ttls) #Mínimo
max_ttl = np.max(ttls) #Máximo


# Listas para armazenar os dados extraídos
timestamps = []
rtts = []
service_times = []

#with open(csv_file_path, 'w') as file:
 #   json.dump(extracted_data, file, indent=4)
        

# Carregar o arquivo JSON
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Ordenar os dados pelo timestamp (caso não estejam ordenados)
data.sort(key=lambda x: x['ts'])

# Calcular intervalos entre chegadas consecutivas
arrivals = np.diff([entry['ts'] for entry in data])

# Calcular taxa de chegada (λ) - mean -> média aritmética
lambda_estimated = 1 / np.mean(arrivals)

for entry in extracted_data:
    if 'rtt' in entry:
        service_times.append(entry['rtt'])

# Calcular taxa de atendimento (μ)
mu_estimated = 1 / np.mean(service_times)


rho = lambda_estimated / mu_estimated  # Utilização do servidor
Lq = rho**2 / (1 - rho)  # Número médio de pacotes na fila
Wq = Lq / lambda_estimated  # Tempo médio na fila


    
# Extrair os dados relevantes
for entry in data:
    ts = entry['ts']
    for val in entry['val']:
        rtt = val['rtt']
        timestamps.append(ts)
        rtts.append(rtt)

# Plotar os dados usando Matplotlib
plt.figure(figsize=(10, 5))
plt.plot(timestamps, rtts, marker='o', linestyle='-', color='b')
plt.xlabel('Timestamp')
plt.ylabel('RTT (ms)')
plt.title('RTT em função do Timestamp')
plt.grid(True)
plt.show()



# Exibir resultados estimados

print(f"RTT - Média: {mean_rtt}, Variância: {variance_rtt}, Desvio Padrão: {std_dev_rtt}, Mínimo: {min_rtt}, Máximo: {max_rtt}")
print(f"TTL - Média: {mean_ttl}, Variância: {variance_ttl}, Desvio Padrão: {std_dev_ttl}, Mínimo: {min_ttl}, Máximo: {max_ttl}")
print(f'Taxa de chegada (λ): {lambda_estimated}')
print(f'Taxa de atendimento (μ): {mu_estimated}')
print(f'Número médio de pacotes na fila (Lq): {Lq}')
print(f'Tempo médio na fila (Wq): {Wq}')






