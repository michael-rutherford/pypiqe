# Perception based Image Quality Evaluator (PIQE) 
## No-reference image quality assessment score for Python

Converted from and tested against the [MATLAB function](https://www.mathworks.com/help/images/ref/piqe.html).

Based on the paper: 

> Venkatanath N, Praneeth D, Maruthi Chandrasekhar Bh, S. S. Channappayya and S. S. Medasani, "Blind image quality evaluation using perception based features," 2015 Twenty First National Conference on Communications (NCC), Mumbai, India, 2015, pp. 1-6, doi: [10.1109/NCC.2015.7084843](http://www.doi.org/10.1109/NCC.2015.7084843).

## Syntax

```
pip install pypiqe
```

```
from pypiqe import piqe

score, activityMask, noticeableArtifactMask, noiseMask = piqe(I)
```

## Description


## Examples


## Input Arguments

| Name | Type | Description |
| ---- | ---- | ----------- |
| I | 2D Image | Input image, specified as a 2-D grayscale image of size m-by-n or 2-D RGB image of size m-by-n-by-3. |

## Output Arguments

| Name | Type | Description |
| ---- | ---- | ----------- |
| score | nonnegative double | PIQE score for the input image A, returned as a nonnegative scalar in the range [0, 100]. The PIQE score is the no-reference image quality score and it is inversely correlated to the perceptual quality of an image. A low score value indicates high perceptual quality and high score value indicates low perceptual quality. |
| activityMask | 2D Binary Image | Spatial quality mask of active blocks, returned as a 2-D binary image of size m-by-n, where m and n are the dimensions of the input image A. The activityMask is composed of high spatially active blocks in the input image. The high spatially active blocks in the input image are the regions with more spatial variability due to factors that include compression artifacts and noise. The high spatially active blocks are assigned a value '1' in the activityMask. |
| noticeableArtifactMask | 2D Binary Image | Spatial quality mask of noticeable artifacts, returned as a 2-D binary image of size m-by-n, where m and n are the dimensions of the input image A. The noticeableArtifactsMask is composed of blocks in activityMask that contain blocking artifacts (due to compression) or sudden distortions. |
| noiseMask | 2D Binary Image | Spatial quality mask of Gaussian noise, returned as a 2-D binary image of size m-by-n, where m and n are the dimensions of the input image A. The noiseMask is composed of blocks in activityMask that contain Gaussian noise. |

## Algorithm

PIQE calculates the no-reference quality score for an image through block-wise distortion estimation, using these steps:

1. Compute the Mean Subtracted Contrast Normalized (MSCN) coefficient for each pixel in the image using the algorithm proposed by N. Venkatanath and others [1].
2. Divide the input image into nonoverlapping blocks of size 16-by-16.
3. Identify high spatially active blocks based on the variance of the MSCN coefficients.
4. Generate activityMask using the identified high spatially active blocks.
5. In each block, evaluate distortion due to blocking artifacts and noise using the MSCN coefficients.
6. Use threshold criteria to classify the blocks as distorted blocks with blocking artifacts, distorted blocks with Gaussian noise, and undistorted blocks.
7. Generate noticeableArtifactsMask from the distorted blocks with blocking artifacts and noiseMask from the distorted blocks with Gaussian noise.
8. Compute the PIQE score for the input image as the mean of scores in the distorted blocks.
9. The quality scale of the image based on its PIQE score is given in this table.

| Quality Scale | Score Range |
| ------------- | ----------- |
| Excellent     | (0, 20)     |
| Good          | (20, 40)    |
| Fair          | (40, 60)    |
| Poor          | (60, 80)    |
| Bad           | (80, 100)   |