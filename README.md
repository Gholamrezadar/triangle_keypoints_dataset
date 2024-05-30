# Triangle Keypoints Dataset

This is a the most basic dataset you can use for keypoint localization tasks. I created this dataset for experimenting on doing keypoint localization using deep learning.

The dataset consists of images of a triangle on a `512x512` RGB image.
![demo](https://huggingface.co/datasets/Gholamreza/triangle_keypoints/resolve/main/demo/demo.png)

# Splits
| Split | Number of Images |
|-------|------------------|
| Train | 8,000            |
| Test  | 2,000            |
| Valid | 1,000            |

You can download the dataset from this link: https://huggingface.co/datasets/Gholamreza/triangle_keypoints

# Example
Here is an example notebook: TODO NOTEBOOK

## Create the dataset
```bash
python create_dataset.py --num-images 100 --output train --min-angle 20
```

TODO:

- [x] create the dataset
- [x] upload the dataset
- [ ] train a model on the dataset and post the result here

