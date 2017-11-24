import os
from ._download_gtsrb import download_gtsrb, download_gtsrb_testdata
from ._generate_64x64 import generate_64x64


def get_folderpath(subset: str, original_images=False) -> str:
    
    # check if we are on phoenix workstation
    phx_srv_path = '/data/Images'
    if os.path.isdir(phx_srv_path):
        path = phx_srv_path
    else:
        path = os.path.join(os.path.realpath('.'), '..', '..')
    
    # download correct dataset
    if subset not in ['test', 'train']:
        raise Exception("subset parameter must be either 'test' or 'train " + subset)
    if subset == 'train':
        if original_images:
            return download_gtsrb(path)
        else:
            return generate_64x64(path, test=False)
    elif subset == 'test':
        if original_images:
            return download_gtsrb_testdata(path)
        else:
            return generate_64x64(path, test=True)
