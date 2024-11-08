
        @echo off
        echo Iniciando o treinamento do modelo...
        "C:\Users\abvit\Documents\BPK\IC\projeto-placas\opencv\build\x64\vc15\bin\opencv_traincascade.exe" ^
        -data "C:\Users\abvit\Documents\BPK\IC\projeto-placas\train_dir" ^
        -info positives.txt ^
        -vec positives20k.vec ^
        -bg negatives.txt ^
        -numPos 500 ^
        -numNeg 750 ^
        -numStages 19 ^
        -precalcValBufSize 4096 ^
        -precalcIdxBufSize 4096 ^
        -featureType LBP ^
        -w 60 ^
        -h 24 ^
        -mode ALL ^
        -maxFalseAlarmRate 0.01 ^
        -minHitRate 0.98 ^
        -maxDepth 15 ^
        -maxWeakCount 100
        