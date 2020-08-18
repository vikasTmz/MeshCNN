#!/usr/bin/env bash

## run the test and export collapses
python test.py \
--dataroot datasets/3dfuture_chairs_seg \
--name 3dfuture_chairs_seg \
--arch meshunet \
--dataset_mode segmentation \
--ncf 32 64 128 256 \
--ninput_edges 1500 \
--pool_res 1050 600 300 \
--resblocks 3 \
--batch_size 12 \
--export_folder meshes \
