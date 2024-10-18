@echo off
echo Iniciando o treinamento do modelo...

"C:\Users\abvit\Documents\BPK\IC\projeto-placas\opencv\build\x64\vc15\bin\opencv_traincascade.exe" ^
-data "C:\Users\abvit\Documents\BPK\IC\projeto-placas\train_dir" ^
-info positives.txt ^
-vec positives20k.vec ^
-bg negatives.txt ^
-numPos 40 ^
-numNeg 40 ^
-numStages 8 ^
-precalcValBufSize 1024 ^
-precalcIdxBufSize 1024 ^
-featureType HAAR ^
-w 60 ^
-h 24 ^
-mode ALL ^
-maxFalseAlarmRate 0.3 ^
-minHitRate 0.9 ^
-maxDepth 6 ^
-maxWeakCount 200
