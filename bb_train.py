from Options.bb_train_options import TrainOptions
import numpy as np
import pandas as pd
import os

import os

if __name__ == '__main__':
    opt =  TrainOptions().parse()  

    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = str(opt.gpu_id) 
    from medmnist import ChestMNIST
    from torch.utils.data import Subset
    from fastai.vision.all import *
    from fastai.callback.wandb import *
    from Dsets.KDataset import KDataset
    from Dsets.XDataset import XDataset
    from fastai.callback.wandb import *
    from transformers import AutoModelForImageClassification
    batch_size = opt.b_size
    num_workers = opt.n_cpu
    print(f'Num of cpus is {opt.n_cpu}')
    
    print(f'Batch size is {opt.b_size}')
    if opt.dataset == 'kermany':

        dataset = KDataset(opt.meta_csv,
                            opt.meta_csv,
                            opt.data_dir,
                            data_format='jpeg',
                            pathologies= [p for p in opt.pathologies.split(',')] )
        df=pd.read_csv(opt.meta_csv)
        splts=[p.split('/')[1] for p in df['Path'].values]
        
        valid_dataset = Subset(dataset,np.argwhere(np.array(splts)=='test') )
        train_dataset = Subset(dataset, np.argwhere(np.array(splts)=='train'))
        model2 = AutoModelForImageClassification.from_pretrained("facebook/convnext-base-224",return_dict=False,num_labels=len(opt.pathologies.split(',')),
                                                            ignore_mismatched_sizes=True)
    elif opt.dataset == 'chestmnist':
        opt.meta_csv='NA'
        opt.data_dir='NA'
        opt.pathologies='NA'

        test_dataset = ChestMNIST(split="test", download=True)
        train_dataset = ChestMNIST(split="train", download=True)
        valid_dataset= ChestMNIST(split="val", download=True)
        train_dataset = XDataset(train_dataset)
        valid_dataset = XDataset(valid_dataset)
        model2 = AutoModelForImageClassification.from_pretrained("facebook/convnext-base-224",return_dict=False,num_labels=14,
                                                            ignore_mismatched_sizes=True)
    else:

        dataset = CDataset(opt.meta_csv,
                            opt.meta_csv,
                            opt.data_dir,
                            data_format='jpeg',
                            pathologies= [p for p in opt.pathologies.split(',')] )
        df=pd.read_csv(opt.meta_csv)
        splts=[p.split('/')[1] for p in df['Path'].values]
        
        valid_dataset = Subset(dataset,np.argwhere(np.array(splts)=='test') )
        train_dataset = Subset(dataset, np.argwhere(np.array(splts)=='train'))
        model2 = AutoModelForImageClassification.from_pretrained("facebook/convnext-base-224",return_dict=False,num_labels=len(opt.pathologies.split(',')),
                                                            ignore_mismatched_sizes=True)



    train_loader = DataLoader(train_dataset, batch_size=batch_size, num_workers=num_workers, drop_last=True)
    print(f'# of train batches is {len(train_loader)}')
    valid_loader = DataLoader(valid_dataset, batch_size=batch_size, num_workers=num_workers, drop_last=True) 
    print(f'# of validation batches is {len(valid_loader)}')
    dls = DataLoaders(train_loader, valid_loader)
    dls.c = 2

    
    class ConvNext(nn.Module):
        def __init__(self, model):
            super(ConvNext, self).__init__()
            self.model=model

        def forward(self, x):
            x = self.model(x)[0]
            return x
        
    model=ConvNext(model2)
    model.to(device='cuda')
    learner = Learner(dls, model, model_dir=opt.out_dir,
                    loss_func=torch.nn.BCEWithLogitsLoss())
    
    learner.metrics = [RocAucMulti(average=None), APScoreMulti(average=None)]

    learner.fit_one_cycle(n_epoch=opt.n_epochs, cbs=SaveModelCallback(fname='convnext_bb_'+opt.dataset))


