import torch
from . import networks
from os.path import join
from util.util import seg_accuracy, print_network
import numpy as np

class TexturizeModel:
    """ Class for training Model weights

    :args opt: structure containing configuration params
    e.g.,
    --dataset_mode -> texturize)
    --arch -> network type
    """
    def __init__(self, opt, channel):
        self.opt = opt
        self.gpu_ids = opt.gpu_ids
        self.is_train = opt.is_train
        self.device = torch.device('cuda:{}'.format(self.gpu_ids[0])) if self.gpu_ids else torch.device('cpu')
        self.save_dir = join(opt.checkpoints_dir, opt.name)
        self.optimizer = None
        self.edge_features = None
        self.labels = None
        self.mesh = None
        self.soft_label = None
        self.loss = None
        self.channel = channel

        #
        self.nclasses = opt.nclasses

        # load/define networks
        self.net = networks.define_classifier(opt.input_nc, opt.ncf, opt.ninput_edges, opt.nclasses, opt,
                                              self.gpu_ids, opt.arch, opt.init_type, opt.init_gain)
        self.net.train(self.is_train)
        self.criterion = networks.define_loss(opt).to(self.device)

        if self.is_train:
            # SGD
            # self.optimizer = torch.optim.SGD(self.net.parameters(), lr=0.1, momentum=0.7)
            # Adam
            self.optimizer = torch.optim.Adam(self.net.parameters(), lr=opt.lr, betas=(opt.beta1, 0.4))
            self.scheduler = networks.get_scheduler(self.optimizer, opt)
            print_network(self.net)

        if not self.is_train or opt.continue_train:
            self.load_network(opt.which_epoch)

    def set_input(self, data):
        input_edge_features = torch.from_numpy(data['edge_features']).float()
        labels = torch.from_numpy(data['label']).float()
        # soft_label = torch.from_numpy(data['label']).float()
        # set inputs
        self.edge_features = input_edge_features.to(self.device).requires_grad_(self.is_train)
        self.labels = labels.to(self.device)
        # self.soft_label = soft_label.to(self.device)
        self.mesh = data['mesh']


    def forward(self):
        out = self.net(self.edge_features, self.mesh)
        return out

    def backward(self, out):
        # out = torch.cat((out1, out2, out3), 1)
        out = torch.reshape(out,self.labels.shape)
        self.loss = self.criterion(out, self.labels)
        # tv_loss = 0
        # if (self.loss * self.opt.lambda_L1).item() < 15:
        _, height, chan = self.labels.shape
        dy = torch.abs(self.labels[:,1:,:] - self.labels[:,:-1,:])
        dyhat = torch.abs(out[:,1:,:] - out[:,:-1,:])
        tv_loss = torch.norm(dy - dyhat, 1) / height
        print("TV Loss = ",(tv_loss * 10).item())

        print("L1 Loss = ",(self.loss * self.opt.lambda_L1).item())

        if self.opt.dataset_mode == "texturize":
            self.loss = self.loss * self.opt.lambda_L1 + tv_loss * 10
        self.loss.backward()
        # self.loss.backward(retain_graph=True)
        # self.optimizer.step()

    def optimize_parameters(self):
        self.optimizer.zero_grad()
        out = self.forward()
        # return out
        self.backward(out)
        self.optimizer.step()


##################

    def load_network(self, which_epoch):
        """load model from disk"""
        save_filename = '%s_%d_net.pth' % (which_epoch, self.channel)
        load_path = join(self.save_dir, save_filename)
        net = self.net
        if isinstance(net, torch.nn.DataParallel):
            net = net.module
        print('loading the model from %s' % load_path)
        # PyTorch newer than 0.4 (e.g., built from
        # GitHub source), you can remove str() on self.device
        state_dict = torch.load(load_path, map_location=str(self.device))
        if hasattr(state_dict, '_metadata'):
            del state_dict._metadata
        net.load_state_dict(state_dict)


    def save_network(self, which_epoch):
        """save model to disk"""
        save_filename = '%s_%d_net.pth' % (which_epoch, self.channel)
        save_path = join(self.save_dir, save_filename)
        if len(self.gpu_ids) > 0 and torch.cuda.is_available():
            torch.save(self.net.module.cpu().state_dict(), save_path)
            self.net.cuda(self.gpu_ids[0])
        else:
            torch.save(self.net.cpu().state_dict(), save_path)

    def update_learning_rate(self):
        """update learning rate (called once every epoch)"""
        self.scheduler.step()
        lr = self.optimizer.param_groups[0]['lr']
        print('learning rate = %.7f' % lr)

    def test(self):
        """tests model
        returns: number correct and total number
        """
        with torch.no_grad():
            out = self.forward()
            out = torch.reshape(out,self.labels.shape)

            correct = 1 - torch.nn.L1Loss()(out, self.labels)
            
            out = out.cpu().detach().numpy()
            out = np.clip(out[0], 0, 1)
            gt = self.labels.cpu().detach().numpy()
            gt = gt[0]
            print("TESTIME L1: for channel [", self.channel , "] ", correct*100)
        return correct, 1, out, gt
