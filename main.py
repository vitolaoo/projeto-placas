import cv2
import pytesseract
import mysql.connector
from os import getenv

from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env


from database_scripts.plate_processing import detect_recognize_plate

if __name__ == "__main__":
    print("Variáveis de ambiente:")
    print("MYSQL_HOST:", getenv("MYSQL_HOST"))
    print("MYSQL_PORT:", getenv("MYSQL_PORT"))
    print("MYSQL_USER:", getenv("MYSQL_USER"))
    print("MYSQL_PASSWORD:", getenv("MYSQL_PASSWORD"))
    print("MYSQL_DB:", getenv("MYSQL_DB"))
    print("TESSERACT_CMD:", getenv('TESSERACT_CMD'))
    print("HAAR_MODEL_PATH:", getenv('HAAR_MODEL_PATH'))

    # Conexao com o banco
    try:
        conn = mysql.connector.connect(
            host=getenv("MYSQL_HOST"),   
            port=getenv("MYSQL_PORT"),          
            user=getenv("MYSQL_USER"),        
            password=getenv("MYSQL_PASSWORD"),    
            database=getenv("MYSQL_DB")
        )
        cursor = conn.cursor()

    except mysql.connector.Error as err:
        print(f'Atencao!\nErro ao tentar se conectar com o banco de dados.\n{err}')
        exit()
            
    # Diretorio do Tesseract
    pytesseract.pytesseract.tesseract_cmd = getenv('TESSERACT_CMD')

    # Modelo HAAR Cascade (xml)
    model = getenv('HAAR_MODEL_PATH')

    #cap = cv2.VideoCapture(0) # webcam
    #cap = cv2.VideoCapture("C:/Users/abvit/Documents/BPK/IC/projeto-placas/videos_teste/videocarros.MTS") # video
    #cap = cv2.VideoCapture("C:/Users/abvit/Documents/BPK/IC/projeto-placas/videos_teste/focus.mp4")
    #cap = cv2.VideoCapture("C:/Users/abvit/Documents/BPK/IC/projeto-placas/videos_teste/ruas1.mp4")
    cap = cv2.VideoCapture("C:/Users/abvit/Documents/BPK/IC/projeto-placas/videos_teste/BOSTA.mp4")

    desired_width = 1240
    desired_height = 860

    valid_plate_total = 0 #variavel global de pontuacao

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("erro ao capturar o frame.")
            break

        frame = cv2.resize(frame, (desired_width, desired_height))

        valid_plate_count = detect_recognize_plate(frame=frame, model=model, conn=conn, cursor=cursor)
        valid_plate_total += valid_plate_count  # Soma a contagem do frame ao total

        plate_result = detect_recognize_plate(frame=frame, model=model, conn=conn, cursor=cursor)
        # print(f'Resultado da detecção: {plate_result}')

        if plate_result == "sim":
            print("Placa autorizada!")
        
        elif plate_result == "não":
            print("Placa não autorizada. Acesso negado!")

        cv2.imshow('Video com Placas Detectadas', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print(f"Total de placas válidas detectadas: {valid_plate_total}")  # Exibe o total ao final

    cap.release()
    cv2.destroyAllWindows()
    cursor.close()
    conn.close()
