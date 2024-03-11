# SLIViT: a general AI framework for clinical-feature diagnosis from limited 3D biomedical-imaging data


<img src="SLIViT.png" width="900px"/>


SLIViT is a deep-learning framework that accurately measures disease-related risk factors in volumetric biomedical imaging, such as magnetic resonance imaging (MRI) scans, optical coherence tomography (OCT) scans, ultrasound videos, and Computed Tomography (CT) scans (for further details please refer to <a href="https://www.researchsquare.com/article/rs-3044914/latest">our manuscript</a>). 

Before running SLIViT.ipynb, please make sure to have an appropriate Python environment with the relevant packages (listed in requirements.txt) properly installed:
```bash
conda create --name slivit --file requirements.txt
```

A pre-trained backbone is provided (see backbone.pth.zip) although one may wish to train the model from scratch.

A code snippet with an example of loading a pre-trained SLIViT model and running inference on a given volume is provided at the end of the SLIViT.ipynb notebook.

# Convnext Backbone Pre-Training

|F_Name | Path | CNV ( Pathology 1 ) | DME ( Pathology 2 ) | Drusen ( Pathology 3 ) | Normal ( Pathology 4 ) | 
|--- | --- | --- | --- |--- |--- |
| CNV-6116901-21.jpeg  | /data/slivit/Kermany/train/CNV/CNV-6116901-21.... | 1.0 | 0.0   |  0.0  |   0.0| 
  |   DME-4616882-33.jpeg  |   /data/slivit/Kermany/train/DME/DME-4616882-33.... | 0.0 | 1.0  |   0.0   |  0.0| 
 |    CNV-7907754-23.jpeg  |  /data/slivit/Kermany/train/CNV/CNV-7907754-23.... | 1.0 | 0.0   |  0.0    | 0.0| 
 | NORMAL-3757443-31.jpeg  | /data/slivit/Kermany/train/NORMAL/NORMAL-37574... | 0.0  |0.0  |   0.0   |  1.0
 |  NORMAL-6434323-2.jpeg |  /data/slivit/Kermany/train/NORMAL/NORMAL-64343...  |0.0|  0.0   |  0.0 |    1.0|
  |  NORMAL-910422-8.jpeg | /data/slivit/Kermany/train/NORMAL/NORMAL-91042... | 0.0 | 0.0  |   0.0   |  1.0|
 | DRUSEN-8086850-28.jpeg |  /data/slivit/Kermany/train/DRUSEN/DRUSEN-80868... | 0.0 | 0.0   |  1.0   |  0.0|


```bash
python bb_train.py --meta_csv /path/to/meta.csv --pathologies CNV,Drusen,DME,Normal --out_dir /output/dir/to/pretrained_bb.pth --b_size 4 --gpu_id 1 --n_cpu=32
```





Feel free to <a href="mailto:orenavram@gmail.com,berkin1997@g.ucla.edu?subject=A%20SLIViT%20question"> reach out</a> regarding any concerns/issues you are experiencing with SLIViT.

# Acknowledgements
Parts of the code are taken from the <a href="https://github.com/lucidrains/vit-pytorch/tree/main"> vit-pytorch</a> repository.
