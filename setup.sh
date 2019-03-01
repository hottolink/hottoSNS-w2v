
if [ ! -e "./corpus/jwsan.zip" ];then
    wget http://www.utm.inf.uec.ac.jp/JWSAN/jwsan.zip -O corpus/jwsan.zip
fi

if [ ! -d "./corpus/JWSAN" ];then
    cd corpus
    unzip jwsan.zip
    cd ..
fi

if [ ! -e "./corpus/jawiki.word_vectors.200d.txt" ];then
    wget https://github.com/singletongue/WikiEntVec/releases/download/20181001/jawiki.word_vectors.200d.txt.gz -O corpus/jawiki.word_vectors.200d.txt.gz
    gzip -d  corpus/jawiki.word_vectors.200d.txt.gz
fi

if [ ! -e "./corpus/w2v_all_vector200_win5_sgns0.vec" ];then
    cd corpus
    tar jvxf hottoSNS-w2v_20190301.tar.bz2 
    cd ..
fi
