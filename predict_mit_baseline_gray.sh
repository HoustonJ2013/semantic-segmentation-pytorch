python predict.py --id baseline-resnet34_dilated8-psp_bilinear_predict_on_gray --list_predict ./data/ADE20K_object150_val_gray.txt --arch_encoder resnet34_dilated8 --arch_decoder psp_bilinear

zip -r mit_baseline_predict_gray.zip result/baseline-resnet34_dilated8-psp_bilinear_predict_on_gray/

aws s3 cp mit_baseline_predict_gray.zip s3://aws-logs-075604225829-us-east-2/mit_baseline_predict_gray.zip

#aws ec2 stop-instances --instance-ids i-080fb52b517c0cb5d
