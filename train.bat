
        @echo off
        echo Iniciando o treinamento do modelo...
        "C:\Users\abvit\Documents\BPK\IC\projeto-placas\opencv\build\x64\vc15\bin\opencv_traincascade.exe" ^
        -data "C:\Users\abvit\Documents\BPK\IC\projeto-placas\train_dir" ^
        -info positives.txt ^
        -vec positives20k.vec ^
        -bg negatives.txt ^
        -numPos 450 ^
        -numNeg 354 ^
        -numStages 12 ^
        -precalcValBufSize 4096 ^
        -precalcIdxBufSize 4096 ^
        -featureType LBP ^
        -w 60 ^
        -h 24 ^
        -mode ALL ^
        -maxFalseAlarmRate 0.22 ^
        -minHitRate 0.87 ^
        -maxDepth 14 ^
        -maxWeakCount 170
        