python train.py --id gray-resnet34_dilated8-psp_bilinear --arch_encoder resnet34_dilated8 --arch_decoder psp_bilinear --weights_encoder ckpt/gray-resnet34_dilated8-psp_bilinear/encoder_best.pth  --weights_decoder ckpt/gray-resnet34_dilated8-psp_bilinear/decoder_best.pth --batch_size_per_gpu 8 --num_epoch 5

python predict.py --id gray-resnet34_dilated8-psp_bilinear --list_predict ./data/ADE20K_object150_val_gray.txt
