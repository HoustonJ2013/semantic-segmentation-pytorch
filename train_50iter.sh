python train.py --id baseline50iter --arch_encoder resnet34_dilated8 --arch_decoder psp_bilinear --num_gpus 1 --batch_size_per_gpu 8 --num_epoch 100 >> train_100.logs

aws ec2 stop-instances --instance-ids i-080fb52b517c0cb5d
