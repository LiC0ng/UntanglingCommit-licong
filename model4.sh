mkdir -p dataset/cluster/4/argouml
mkdir -p dataset/cluster/4/gwt
mkdir -p dataset/cluster/4/jruby
mkdir -p dataset/cluster/4/xstream
mkdir -p dataset/cluster/4/all

python ./model4_idPACE_otherN2N.py --type ins
python ./model4_idPACE_otherN2N.py --type ino
python ./model4_idPACE_otherN2N.py --type its
python ./model4_idPACE_otherN2N.py --type ito