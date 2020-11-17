mkdir -p dataset/cluster/1/argouml
mkdir -p dataset/cluster/1/gwt
mkdir -p dataset/cluster/1/jruby
mkdir -p dataset/cluster/1/xstream
mkdir -p dataset/cluster/1/all

python ./model1_idN2N_otherN2N.py --type ins
python ./model1_idN2N_otherN2N.py --type ino
python ./model1_idN2N_otherN2N.py --type its
python ./model1_idN2N_otherN2N.py --type ito