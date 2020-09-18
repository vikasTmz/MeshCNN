#!/usr/bin/env bash

## run the training
python train.py \
--dataroot datasets/3dfuture_chairs \
--name 3dfuture_chairs \
--arch meshunet \
--dataset_mode texturize \
--ncf 32 64 128 256 \
--ninput_edges 1623 \
--pool_res 1623 1143 811 \
--resblocks 3 \
--lr 0.001 \
--batch_size 12 \
--num_aug 20 \
--slide_verts 0 \
--export_folder 'intermediate_meshes'

#
# python train.py --dataroot datasets/coseg_vases --name coseg_vases --arch meshunet --dataset_mode
#segmentation --ncf 32 64 128 256 --ninput_edges 1500 --pool_res 1050 600 300 --resblocks 3 --lr 0.001 --batch_size 12 --num_aug 20
