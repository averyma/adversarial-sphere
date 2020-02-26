import torch
import torch.nn as nn
from torch.autograd import grad
from utils_sphere import *

class pgd_sphere(object):
    """ projected gradient desscent, with random initialization within the ball """
    def __init__(self, **kwargs):
        # define default attack parameters here:
        self.param = {'alpha': 0.1,
                      'num_iter': 1,
                      'loss_fn': nn.BCEWithLogitsLoss()}
        # parse thru the dictionary and modify user-specific params
        self.parse_param(**kwargs) 
        
    def generate(self, model, x, y):
        alpha = self.param['alpha']
        num_iter = self.param['num_iter']
        loss_fn = self.param['loss_fn']
        
        r = get_norm(x) 
        delta = torch.rand_like(x, requires_grad=True)
        delta.data = r * normalize(x + delta) - x
        
        for t in range(num_iter):
            loss = loss_fn(model(x + delta), y)
            loss.backward()
            
            delta_grad = delta.grad.detach()
            delta.data = delta + alpha * normalize(delta_grad)
            delta.data = r * normalize(x + delta) - x
            delta.grad.zero_()

        return delta.detach()

    def parse_param(self, **kwargs):
        for key,value in kwargs.items():
            if key in self.param:
                self.param[key] = value
                