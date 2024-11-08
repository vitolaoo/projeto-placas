import os
import csv
import random
import subprocess
import time
import shutil

# Defina os intervalos dos parâmetros
param_ranges = {
    "numPos": (200, 200),
    "numNeg": (34, 34),
    "numStages": (15, 20),
    "maxFalseAlarmRate": (0.009, 0.009),
    "minHitRate": (0.98, 0.98),
    "maxDepth": (15, 15),
    "maxWeakCount": (100, 100)
}

# Caminho para o train.bat e o diretório do train_dir
train_bat_dir = "C:/Users/abvit/Documents/BPK/IC/projeto-placas/model"
train_bat = os.path.join(train_bat_dir, "train.bat")
train_dir = "C:/Users/abvit/Documents/BPK/IC/projeto-placas/train_dir"

# Variável global para armazenar o processo do CMD
cmd_process = None

# Função para limpar o train_dir, mantendo apenas a pasta temp
def clean_train_dir():
    for item in os.listdir(train_dir):
        item_path = os.path.join(train_dir, item)
        if os.path.isdir(item_path) and item == "temp":
            continue  # Mantém a pasta temp
        elif os.path.isfile(item_path) or os.path.isdir(item_path):
            shutil.rmtree(item_path) if os.path.isdir(item_path) else os.remove(item_path)

# Função para gerar parâmetros aleatórios
def generate_random_params():
    params = {}
    for key, (low, high) in param_ranges.items():
        if isinstance(low, int):  # Parâmetros inteiros
            params[key] = random.randint(low, high)
        else:  # Parâmetros de ponto flutuante
            params[key] = round(random.uniform(low, high), 2)
    return params


# Função para atualizar e rodar o arquivo train.bat com novos parâmetros
def run_training_with_params(params):
    global cmd_process

    # Atualiza o train.bat com os novos parâmetros
    with open(train_bat, "w") as f:
        f.write(f"""
        @echo off
        echo Iniciando o treinamento do modelo...
        "C:\\Users\\abvit\\Documents\\BPK\\IC\\projeto-placas\\opencv\\build\\x64\\vc15\\bin\\opencv_traincascade.exe" ^
        -data "C:\\Users\\abvit\\Documents\\BPK\\IC\\projeto-placas\\train_dir" ^
        -info positives.txt ^
        -vec positives20k.vec ^
        -bg negatives.txt ^
        -numPos {params["numPos"]} ^
        -numNeg {params["numNeg"]} ^
        -numStages {params["numStages"]} ^
        -precalcValBufSize 4096 ^
        -precalcIdxBufSize 4096 ^
        -featureType LBP ^
        -w 60 ^
        -h 24 ^
        -mode ALL ^
        -maxFalseAlarmRate {params["maxFalseAlarmRate"]} ^
        -minHitRate {params["minHitRate"]} ^
        -maxDepth {params["maxDepth"]} ^
        -maxWeakCount {params["maxWeakCount"]}
        """)

    # Limpa o diretório de treino antes de iniciar o novo treinamento
    clean_train_dir()

    # Executa o train.bat e espera até que termine
    training_process = subprocess.run(f'cmd /c "{train_bat}"', shell=True, cwd=train_bat_dir)

    if training_process.returncode == 0:
        print("Treinamento concluído com sucesso.")
    else:
        print("Houve um erro durante o treinamento.")


# Função para rodar main.py e coletar a precisão, total de detecções e placas válidas
def run_main_and_get_metrics():
    result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    output = result.stdout
    # Extraindo a precisão, total de detecções e placas válidas da saída
    precision_line = [line for line in output.splitlines() if "Precisão da detecção" in line]
    detections_line = [line for line in output.splitlines() if "Total de detecções" in line]
    valid_plates_line = [line for line in output.splitlines() if "Total de placas válidas detectadas" in line]

    precision = float(precision_line[0].split(":")[1].strip().replace("%", "")) / 100 if precision_line else 0
    total_detections = int(detections_line[0].split(":")[1].strip()) if detections_line else 0
    valid_plates = int(valid_plates_line[0].split(":")[1].strip()) if valid_plates_line else 0

    return precision, total_detections, valid_plates

# Função para salvar resultados no CSV
def save_results_to_csv(params, precision, total_detections, valid_plates):
    with open("training_results.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Se o arquivo estiver vazio, escreva o cabeçalho
            writer.writerow(["numPos", "numNeg", "numStages", "maxFalseAlarmRate", "minHitRate", "maxDepth", "maxWeakCount", 
                             "Precision", "Total_Detections", "Valid_Plates"])
        writer.writerow([params[key] for key in params] + [precision, total_detections, valid_plates])

# Função principal para rodar iterações de teste
def optimize_training(iterations=10):
    for _ in range(iterations):
        params = generate_random_params()
        run_training_with_params(params)
        # Após o treinamento, execução do main.py para coleta das métricas
        precision, total_detections, valid_plates = run_main_and_get_metrics()
        save_results_to_csv(params, precision, total_detections, valid_plates)
        print(f"Parâmetros: {params} -> Precisão: {precision:.2%}, Detecções: {total_detections}, Placas Válidas: {valid_plates}")

# Executar a otimização
optimize_training(10)
