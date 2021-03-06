import math
import torch 
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter

class GraphConvolution(nn.Module):
    """
    Based on Thomas Kipf's Pygcn ( https://github.com/tkipf/pygcn/blob/master/pygcn/layers.py )
    (Simple GCN layer, similar to https://arxiv.org/abs/1609.02907)
    """

    def __init__(self, in_features, out_features, bias=None):
        super(GraphConvolution, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = Parameter(torch.FloatTensor(in_features, out_features))
        if bias:
            self.bias = Parameter(torch.FloatTensor(out_features))
        else:
            self.register_parameter('bias', None)
        self.reset_parameters()

    def reset_parameters(self):
        stdv = 1. / math.sqrt(self.weight.size(1))
        self.weight.data.uniform_(-stdv, stdv)
        if self.bias is not None:
            self.bias.data.uniform_(-stdv, stdv)

    def forward(self, input, adj):
        #check if correct reshape
        #print("X@W",input.shape,self.weight.shape)
        support = torch.matmul(input, self.weight)
        dims = support.shape[:2]
        #print("L@Res",adj.shape,support.shape)
        output = torch.matmul(adj, support.reshape(-1,self.weight.shape[-1]))
        if self.bias is not None:
            return output + self.bias
        else:
            return output.reshape(dims[0],dims[1],self.weight.shape[-1])

    def __repr__(self):
        return self.__class__.__name__ + ' (' \
               + str(self.in_features) + ' -> ' \
               + str(self.out_features) + ')'
