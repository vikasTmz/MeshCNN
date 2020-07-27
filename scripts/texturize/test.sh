#!/usr/bin/env bash

## run the test and export collapses
python test.py \
--dataroot datasets/3dfuture_chairs \
--name 3dfuture_chairs \
--arch meshunet \
--dataset_mode texturize \
--ncf 32 64 128 256 \
--ninput_edges 1500 \
--pool_res 1050 600 300 \
--resblocks 3 \
--batch_size 12 \
--export_folder meshes \
