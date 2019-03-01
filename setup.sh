wget http://www.utm.inf.uec.ac.jp/JWSAN/jwsan.zip -O corpus/jwsan.zip
cd corpus
unzip jwsan.zip
cd ..
wget https://github.com/singletongue/WikiEntVec/releases/download/20181001/jawiki.word_vectors.200d.txt.gz -O corpus/jawiki.word_vectors.200d.txt.gz
gzip -d  corpus/jawiki.all_vectors.200d.txt.gz