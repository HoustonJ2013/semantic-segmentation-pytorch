# System libs
import os
import datetime
import argparse
# Numerical libs
import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
from scipy.io import loadmat
from scipy.misc import imsave
from scipy.ndimage import zoom
# Our libs
from dataset import Dataset
from models import ModelBuilder
from utils import AverageMeter, colorEncode, accuracy, intersectionAndUnion
<<<<<<< HEAD

=======
from torch.nn.modules.module import _addindent
>>>>>>> 607f96b77148489a4fefbca6e4034ee57e5fa902

# forward func for evaluation
def forward_multiscale(nets, batch_data, args):
    (net_encoder, net_decoder, crit) = nets
    (imgs, segs, infos) = batch_data

    segSize = (segs.size(1), segs.size(2))
    pred = torch.zeros(imgs.size(0), args.num_class, segs.size(1), segs.size(2))
    pred = Variable(pred, volatile=True).cuda()

    for scale in args.scales:
        imgs_scale = zoom(imgs.numpy(),
                          (1., 1., scale, scale),
                          order=1,
                          prefilter=False,
                          mode='nearest')

        # feed input data
        input_img = Variable(torch.from_numpy(imgs_scale),
                             volatile=True).cuda()

        # forward
        pred_scale = net_decoder(net_encoder(input_img), segSize=segSize)

        # average the probability
        pred = pred + pred_scale / len(args.scales)

    pred = torch.log(pred)

    label_seg = Variable(segs, volatile=True).cuda()
    err = crit(pred, label_seg)
    return pred, err


def visualize_result(batch_data, pred, args):
    colors = loadmat('data/color150.mat')['colors']
    (imgs, segs, infos) = batch_data
    for j in range(len(infos)):
        # get/recover image
        # img = imread(os.path.join(args.root_img, infos[j]))
        img = imgs[j].clone()
        for t, m, s in zip(img,
                           [0.485, 0.456, 0.406],
                           [0.229, 0.224, 0.225]):
            t.mul_(s).add_(m)
        img = (img.numpy().transpose((1, 2, 0)) * 255).astype(np.uint8)

        # segmentation
        lab = segs[j].numpy()
        lab_color = colorEncode(lab, colors)

        # prediction and save as png
        pred_ = np.argmax(pred.data.cpu()[j].numpy(), axis=0)

        np.save(os.path.join(args.result,
                            infos[j]
                            .replace('/', '_')
                            .replace('.jpg', ''))
                            .replace("validation_",""), pred_.astype("int16") + 1)


        pred_color = colorEncode(pred_, colors)

        # aggregate images and save
        im_vis = np.concatenate((img, lab_color, pred_color),
                                axis=1).astype(np.uint8)
        imsave(os.path.join(args.result,
                            infos[j].replace('/', '_')
                            .replace('.jpg', '.png')), im_vis)


def predict(nets, loader, args):
    loss_meter = AverageMeter()
    acc_meter = AverageMeter()
    intersection_meter = AverageMeter()
    union_meter = AverageMeter()

    # switch to eval mode
    for net in nets:
        net.eval()

    for i, batch_data in enumerate(loader):
        # forward pass
        pred, err = forward_multiscale(nets, batch_data, args)
        loss_meter.update(err.data[0])

        # calculate accuracy
        acc, pix = accuracy(batch_data, pred)
<<<<<<< HEAD
        intersection, union, area_pred, area_lab, pred_img, segs_img = intersectionAndUnion(batch_data, pred,args.num_class)
        acc_meter.update(acc, pix)
        intersection_meter.update(intersection)
        union_meter.update(union)
        np.save("intersec" + str(i), intersection)
        np.save("union" + str(i), union)
        np.save("area_pred" + str(i), area_pred)
        np.save("area_lab" + str(i), area_lab)
        np.save("pred_img" + str(i), pred_img)
        np.save("segs_img" + str(i), segs_img)
        
        
=======
        intersection, union = intersectionAndUnion(batch_data, pred,
                                                   args.num_class)
        acc_meter.update(acc, pix)
        intersection_meter.update(intersection)
        union_meter.update(union)
>>>>>>> 607f96b77148489a4fefbca6e4034ee57e5fa902
        print('[{}] iter {}, loss: {}, accuracy: {}'
              .format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      i, err.data[0], acc))

        # visualization
        if args.visualize:
            visualize_result(batch_data, pred, args)
    iou = intersection_meter.sum / (union_meter.sum + 1e-10)
    for i, _iou in enumerate(iou):
        print('class [{}], IoU: {}'.format(i, _iou))

    print('[Eval Summary]:')
    print('Loss: {}, Mean IoU: {:.4}, Accurarcy: {:.2f}%'
          .format(loss_meter.average(), iou.mean(), acc_meter.average()*100))


<<<<<<< HEAD
=======
def torch_summarize(model, show_weights=True, show_parameters=True):
    """Summarizes torch model by showing trainable parameters and weights."""
    tmpstr = model.__class__.__name__ + ' (\n'
    for key, module in model._modules.items():
        # if it contains layers let call it recursively to get params and weights
        if type(module) in [
            torch.nn.modules.container.Container,
            torch.nn.modules.container.Sequential
        ]:
            modstr = torch_summarize(module)
        else:
            modstr = module.__repr__()
        modstr = _addindent(modstr, 2)

        params = sum([np.prod(p.size()) for p in module.parameters()])
        weights = tuple([tuple(p.size()) for p in module.parameters()])

        tmpstr += '  (' + key + '): ' + modstr
        if show_weights:
            tmpstr += ', weights={}'.format(weights)
        if show_parameters:
            tmpstr +=  ', parameters={}'.format(params)
        tmpstr += '\n'

    tmpstr = tmpstr + ')'
    return tmpstr

>>>>>>> 607f96b77148489a4fefbca6e4034ee57e5fa902
def main(args):
    # Network Builders
    builder = ModelBuilder()
    net_encoder = builder.build_encoder(arch=args.arch_encoder,
                                        fc_dim=args.fc_dim,
                                        weights=args.weights_encoder)
    net_decoder = builder.build_decoder(arch=args.arch_decoder,
                                        fc_dim=args.fc_dim,
                                        segSize=args.segSize,
                                        weights=args.weights_decoder,
                                        use_softmax=True)

    crit = nn.NLLLoss2d(ignore_index=-1)

    # Dataset and Loader
    dataset_val = Dataset(args.list_predict, args,
                          max_sample=args.num_val, is_train=0)
    loader_val = torch.utils.data.DataLoader(
        dataset_val,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=2,
        drop_last=True)

    nets = (net_encoder, net_decoder, crit)
    for net in nets:
        net.cuda()

<<<<<<< HEAD
    # Main loop
    predict(nets, loader_val, args)

=======
    print(torch_summarize(nets[0]))
    print(torch_summarize(nets[1]))
    print(torch_summarize(nets[2]))
    # Main loop
    predict(nets, loader_val, args)
>>>>>>> 607f96b77148489a4fefbca6e4034ee57e5fa902
    print('Evaluation Done!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Model related arguments
    parser.add_argument('--id', required=True,
                        help="a name for identifying the model to load")
    parser.add_argument('--suffix', default='_best.pth',
                        help="which snapshot to load")
    parser.add_argument('--arch_encoder', default='resnet34_dilated8',
                        help="architecture of net_encoder")
    parser.add_argument('--arch_decoder', default='c1_bilinear',
                        help="architecture of net_decoder")
    parser.add_argument('--fc_dim', default=512, type=int,
                        help='number of features between encoder and decoder')

    # Path related arguments
    parser.add_argument('--list_predict',
                        default='./data/ADE20K_object150_val.txt')
    parser.add_argument('--root_img',
                        default='./data/ADEChallengeData2016/images')
    parser.add_argument('--root_seg',
                        default='./data/ADEChallengeData2016/annotations')

    # Data related arguments
    parser.add_argument('--num_val', default=-1, type=int,
                        help='number of images to evalutate')
    parser.add_argument('--num_class', default=150, type=int,
                        help='number of classes')
    parser.add_argument('--batch_size', default=1, type=int,
                        help='batchsize')
<<<<<<< HEAD
    parser.add_argument('--imgSize', default=500, type=int,
                        help='input image size, -1 = keep original')
    parser.add_argument('--segSize', default=500, type=int,
=======
    parser.add_argument('--imgSize', default=-1, type=int,
                        help='input image size, -1 = keep original')
    parser.add_argument('--segSize', default=-1, type=int,
>>>>>>> 607f96b77148489a4fefbca6e4034ee57e5fa902
                        help='output image size, -1 = keep original')

    # Misc arguments
    parser.add_argument('--ckpt', default='./ckpt',
                        help='folder to output checkpoints')
    parser.add_argument('--visualize', default=1,
                        help='output visualization?')
    parser.add_argument('--result', default='./result',
                        help='folder to output visualization results')

    args = parser.parse_args()
    print(args)

    # scales for evaluation
    # args.scales = (1, )
<<<<<<< HEAD
    args.scales = (0.75, 1, 1.25)
=======
    args.scales = (0.5, 0.75, 1, 1.25, 1.5)
>>>>>>> 607f96b77148489a4fefbca6e4034ee57e5fa902

    ## Handle memeory issue If image size > 1000, crop to 1000

    # absolute paths of model weights
    args.weights_encoder = os.path.join(args.ckpt, args.id,
                                        'encoder' + args.suffix)
    args.weights_decoder = os.path.join(args.ckpt, args.id,
                                        'decoder' + args.suffix)

    args.result = os.path.join(args.result, args.id)
    if not os.path.isdir(args.result):
        os.makedirs(args.result)

    main(args)
