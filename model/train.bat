@echo off
echo Iniciando o treinamento do modelo...

"C:\Users\abvit\Documents\BPK\IC\projeto-placas\opencv\build\x64\vc15\bin\opencv_traincascade.exe" ^
-data "C:\Users\abvit\Documents\BPK\IC\projeto-placas\train_dir" ^
-info positives.txt ^
-vec positives20k.vec ^
-bg negatives.txt ^
-numPos 4000 ^
-numNeg 2000 ^
-numStages 6 ^
-precalcValBufSize 8192 ^
-precalcIdxBufSize 8192 ^
-featureType HAAR ^
-w 60 ^
-h 24 ^
-mode ALL ^
-maxFalseAlarmRate 0.2 ^
-minHitRate 0.98 ^
-maxDepth 10 ^
-maxWeakCount 300
