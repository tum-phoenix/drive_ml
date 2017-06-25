from ._download_gtsrb import download_gtsrb, download_gtsrb_testdata
from ._generate_64x64 import generate_64x64


def get_folderpath(subset: str, original_images=False) -> str:
    if subset not in ['test', 'train']:
        raise Exception("subset parameter must be either 'test' or 'train " + subset)
    if subset == 'train':
        if original_images:
            return download_gtsrb()
        else:
            return generate_64x64(test=False)
    elif subset == 'test':
        if original_images:
            return download_gtsrb_testdata()
        else:
            return generate_64x64(test=True)
