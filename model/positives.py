import os
import random

def convert_annotations_to_positives(directories, output_file, num_samples):
    # Divide o número total de samples igualmente entre os diretórios
    samples_per_dir = num_samples // len(directories)
    
    with open(output_file, 'w') as out_file:
        for input_dir in directories:
            # Lista todos os arquivos .txt no diretório atual
            txt_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
            
            # Embaralha os arquivos para garantir que não sejam escolhidos sempre na mesma ordem
            random.shuffle(txt_files)
            
            # Seleciona a quantidade necessária de arquivos para este diretório
            selected_txt_files = txt_files[:samples_per_dir]
            
            for filename in selected_txt_files:
                image_name = filename.replace('.txt', '.jpg')
                image_path = os.path.join(input_dir, image_name)
                txt_path = os.path.join(input_dir, filename)
                
                with open(txt_path, 'r') as f:
                    lines = f.readlines()
                    corners_line = [line for line in lines if line.startswith('corners')][0]
                    corners = corners_line.split(': ')[1].strip()
                    corners = corners.split(' ')
                    x1, y1 = map(int, corners[0].split(','))
                    x2, y2 = map(int, corners[2].split(','))
                    
                    width = x2 - x1
                    height = y2 - y1
                    
                    out_file.write(f"{image_path} 1 {x1} {y1} {width} {height}\n")

# Diretórios de entrada
directories = [
    'C:/Users/abvit/Documents/BPK/temp/positives/RodoSol-ALPR/images/cars-me',
    'C:/Users/abvit/Documents/BPK/temp/positives/RodoSol-ALPR/images/cars-br',
    'C:/Users/abvit/Documents/BPK/temp/positives/RodoSol-ALPR/images/motorcycles-me',
    'C:/Users/abvit/Documents/BPK/temp/positives/RodoSol-ALPR/images/motorcycles-br'
]

# Arquivo de saída
output_file = './model/positives.txt'

# Número de amostras que você deseja gerar
num_samples = 2400  # Altere esse valor conforme necessário

# Chama a função para gerar o arquivo
convert_annotations_to_positives(directories, output_file, num_samples)
