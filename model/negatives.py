import os

diretorio = 'negatives'
base_path = r'C:\Users\abvit\Documents\BPK\IC\projeto-placas\negatives'
output_file = './model/negatives.txt'

with open(output_file, 'w') as f:
    for arquivo in os.listdir(diretorio):
        if arquivo.lower().endswith('.jpg'):
            caminho_completo = os.path.join(base_path, arquivo)
            f.write(caminho_completo + f'\n')

