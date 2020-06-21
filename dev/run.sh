#!/bin/bash

cd jiant

AIQ="jiant/config/aiq.yml"

for i in "copa" "boolq" "cb" "rte" "wic" "wsc"
do
  for j in "copa" "boolq" "cb" "rte" "wic" "wsc"
  do

cat > $AIQ <<-EOF
proportion: 0.5
test_name_1: "$i"
test_name_2: "$j"
EOF
   
  python main.py --config_file jiant/config/aiq.conf

  done
done
