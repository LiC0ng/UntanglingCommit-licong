mkdir -p dataset/cluster/3/argouml
mkdir -p dataset/cluster/3/gwt
mkdir -p dataset/cluster/3/jruby
mkdir -p dataset/cluster/3/xstream
mkdir -p dataset/cluster/3/all

python ./model3_idPACE_otherPACE.py --type ins
python ./model3_idPACE_otherPACE.py --type ino
python ./model3_idPACE_otherPACE.py --type its
python ./model3_idPACE_otherPACE.py --type ito