python predict_log.py --id baseline-resnet34_dilated8-psp_bilinear --list_predict ./data/test.txt --arch_encoder resnet34_dilated8 --arch_decoder psp_bilinear

#aws s3 cp mitbaseline_train.log s3://aws-logs-075604225829-us-east-2/mitbaseline_train.log

#aws ec2 stop-instances --instance-ids i-080fb52b517c0cb5d
