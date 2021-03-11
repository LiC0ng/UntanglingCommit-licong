#!/usr/bin/env bash
###########################################################

cat<<-eof
Input corresponding number:
1-Initialize all (Start from step 1 again)
2-Clear experiment data (Start from step 1 again)
notice: Please save the experiment data before if necessary
eof
read -p "*cmd meau**:" cmd
case $cmd in
1)
        echo "1";;
2)
        echo "2";;
*)
        echo "errpr:please in input (1,2)";;
esac
