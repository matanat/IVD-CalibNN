import torch.nn as nn

class RegressionNet(nn.Module):
    def __init__(self, hparams):
        super(RegressionNet, self).__init__()
        
        layers = list()
        for i in range(hparams['num_layers'] - 1):
            i_dim = hparams['input_dim'] if i == 0 else hparams['num_units'] // (2 ** (i - 1))
            o_dim = hparams['num_units'] // (2 ** i)

            layers.append(nn.Linear(i_dim, o_dim))
            if 'activation' not in hparams or hparams['activation'] == 'relu':
                layers.append(nn.ReLU())
            elif hparams['activation'] == 'prelu':
                layers.append(nn.PReLU())
            layers.append(nn.Dropout(p=hparams['dropout_p']))

        # Adding the final layer
        layers.append(nn.Linear(o_dim, hparams['output_dim']))

        # Store layers in ModuleList
        self.layers = nn.ModuleList(layers)

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

