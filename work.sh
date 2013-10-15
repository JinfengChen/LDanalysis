python HaploView.py --input ../input/BGI.SNP.Jap.matrix.1
qsub ld.sh

echo "random 2% SNP from genome"
python RandomLine.py --input ../input/BGI.SNP.Jap.matrix.1 --proportion 2 --output ../input/BGI.SNP.Jap.matrix.4

