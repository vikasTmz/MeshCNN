#!/usr/bin/env bash

## run the training
python train.py \
--dataroot datasets/3dfuture_chairs \
--name 3dfuture_chairs \
--arch meshunet \
--dataset_mode texturize \
--ncf 32 64 128 256 \
--ninput_edges 1728 \
--pool_res 1728 1728 1728 \
--resblocks 3 \
--lr 0.001 \
--batch_size 12 \
--num_aug 10 \
--slide_verts 0 \


#
# python train.py --dataroot datasets/coseg_vases --name coseg_vases --arch meshunet --dataset_mode
#segmentation --ncf 32 64 128 256 --ninput_edges 1500 --pool_res 1050 600 300 --resblocks 3 --lr 0.001 --batch_size 12 --num_aug 20
