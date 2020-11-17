mkdir -p dataset/cluster/2/argouml
mkdir -p dataset/cluster/2/gwt
mkdir -p dataset/cluster/2/jruby
mkdir -p dataset/cluster/2/xstream
mkdir -p dataset/cluster/2/all

python ./model2_idN2N_otherN2N.py --type ins
python ./model2_idN2N_otherN2N.py --type ino
python ./model2_idN2N_otherN2N.py --type its
python ./model2_idN2N_otherN2N.py --type ito