import numpy as np
import cv2

def piqe(I):

    #   This is a python version of matlab's piqe method
    #   https://www.mathworks.com/help/images/ref/piqe.html
    #
    #   [Score, ActivityMask, NoticeableArtifactsMask, NoiseMask] = PIQE(I)
    #   calculates the no-reference image quality score and also returns
    #   spatial quality masks i.e., ActivityMask, NoticeableArtifactsMask and
    #   NoiseMask for image I. Size of spatial quality masks is always M-by-N.
    #   Image I can be either a 2-D grayscale image or an RGB image.
    #
    #   Class Support
    #   -------------
    #   I must be a real, non-sparse, M-by-N or M-by-N-by-3 matrix of one of
    #   the following classes: uint8, uint16, int16, single or double. Score is
    #   a scalar of class double, where as ActivityMask,
    #   NoticeableArtifactsMask and NoiseMask are of class logical.
    #
    #   Notes
    #   -----
    #   1. The main objective of PIQE is to measure the amount of distortion
    #      present in a given test image and produce a quality score. It also
    #      returns block-level spatial quality masks. These masks are useful
    #      for categorizing and localizing image distortions.
    #
    #   2. PIQE is inspired by two human perception based criteria for
    #      image quality assessment.
    #      
    #      a. Human visual attention is highly directed towards salient
    #         regions in the image. Hence, salient regions contribute more
    #         towards overall image quality assessment.
    #
    #      b. Local quality at region level adds up to the overall image
    #         quality.
    #
    #      In PIQE, the image is divided into non-overlapping blocks of size
    #      16x16. Each block is verified towards saliency(2(a)). The blocks
    #      that are spatially active are considered as salient blocks. The
    #      distortion measurement at each of these blocks will contribute to
    #      the overall image quality(2(b)).
    #
    #   3. The PIQE score is a scalar value in the range [0, 100], where 0
    #      indicates excellent quality and 100 indicates bad quality. PIQE
    #      score increases with image quality degradation.
    #
    #   4. Representation of ActivityMask, NoticeableArtifactsMask and
    #      NoiseMask:
    #
    #      ActivityMask: 
    #      It represents high spatially active blocks(i.e., salient blocks) in
    #      the image.
    #
    #      NoticeableArtifactsMask: 
    #      It represents high spatially active blocks of an image that are
    #      affected by compression artifacts(i.e., blockiness) (or) any sudden
    #      artifacts.
    #    
    #      NoiseMask: 
    #      It represents high spatially active blocks of an image that are
    #      affected by Gaussian noise. 
    #
    #   5. If input image I, is uniform or homogeneous, PIQE provides 100 as
    #      output score indicating bad image quality.
    #
    #   6. This method does not involve prior modelling of the image features
    #      and hence, the accuracy of the spatial quality masks depends on
    #      image texture.
    #
    #   Example
    #   -------
    #   # This example shows how to compute the quality score and spatial
    #   # quality masks like ActivityMask, NoticeableArtifactsMask and
    #   # NoiseMask for a JP2K compressed image with added AWGN noise patch.
    #
    #   I = imread('DistortedImage.png');
    #   [Score, ActivityMask, NoticeableArtifactsMask, NoiseMask] = piqe(I);
    #   J  = labeloverlay(I, ActivityMask, 'Colormap', 'winter', 'Transparency', 0.25);
    #   K  = labeloverlay(I, NoticeableArtifactsMask, 'Colormap', 'autumn', 'Transparency', 0.25);
    #   L  = labeloverlay(I, NoiseMask, 'Colormap', 'hot', 'Transparency', 0.25);
    #
    #   # Visualization of Fused High Spatial Activity, Noticeable Artifact 
    #   # and Noisy Labels over the Input Image I.
    #   
    #   figure;
    #   imshow(I);
    #   title('Input Image: JP2K Compressed Image with added AWGN noise patch');
    #   figure;
    #   imshow(J);
    #   title('Fused High Spatial Activity Labels over Input Image I');
    #   figure;
    #   imshow(K);
    #   title('Fused Noticeable Artifact Labels over Input Image I');
    #   figure;
    #   imshow(L);
    #   title('Fused Noisy Labels over Input Image I');
    #
    #   fprintf('PIQE score for the Input Image I is  #0.4f \n', Score);
    #
    #   References:
    #   -----------
    #   [1] Venkatanath N, D. Praneeth, Maruthi Chandrasekhar Bh, Sumohana
    #       S.Channappayya, and Swarup S. Medasani. "Blind image quality
    #       evaluation using perception based features." In
    #       Communications(NCC), 2015 Twenty First National Conference on,
    #       pp.1-6. IEEE, 2015.
    #
    #   See also IMMSE, SSIM, PSNR, BRISQUE, NIQE.


    # Validate Input Image
    ipImage = validateInputImage(I)
    blockSize = 16  # Considered 16x16 block size for overall analysis
    activityThreshold = 0.1  # Threshold used to identify high spatially prominent blocks
    blockImpairedThreshold = 0.1  # Threshold used to identify blocks having noticeable artifacts
    windowSize = 6  # Considered segment size in a block edge.
    nSegments = blockSize-windowSize+1  # Number of segments for each block edge
    distBlockScores = 0  # Accumulation of distorted block scores
    NHSA = 0  # Number of high spatial active blocks.

    # RGB to Gray Conversion
    if ipImage.ndim == 3:
        ipImage = cv2.cvtColor(ipImage, cv2.COLOR_BGR2GRAY)

    # Pad if size(ipImage) is not divisible by blockSize.
    originalSize = ipImage.shape  # Actual image size
    rows, columns = originalSize[:2]
    rowsPad = rows % blockSize
    columnsPad = columns % blockSize
    isPadded = False
    if rowsPad > 0 or columnsPad > 0:
        if rowsPad > 0:
            rowsPad = blockSize - rowsPad
        if columnsPad > 0:
            columnsPad = blockSize - columnsPad
        isPadded = True
        ipImage = np.pad(ipImage, ((0, rowsPad), (0, columnsPad)), mode='symmetric')

    # Convert input image to double and scaled to the range 0-255
    ipImage = np.round(255 * (ipImage / np.max(ipImage)))

    # Normalize image to zero mean and ~unit std
    # used circularly-symmetric Gaussian weighting function sampled out 
    # to 3 standard deviations.
    mu = cv2.GaussianBlur(ipImage, ksize=(7, 7), sigmaX=7/6, borderType=cv2.BORDER_REPLICATE)
    sigma = np.sqrt(np.abs(cv2.GaussianBlur(ipImage * ipImage, ksize=(7, 7), sigmaX=7/6, borderType=cv2.BORDER_REPLICATE) - mu * mu))
    imnorm = (ipImage - mu) / (sigma + 1)

    # Preallocation for masks
    NoticeableArtifactsMask = np.zeros_like(imnorm, dtype=bool)
    NoiseMask = np.zeros_like(imnorm, dtype=bool)
    ActivityMask = np.zeros_like(imnorm, dtype=bool)

    # Start of block by block processing
    for i in range(0, imnorm.shape[0], blockSize):
        for j in range(0, imnorm.shape[1], blockSize):

            # Weights Initialization
            WNDC = 0
            WNC = 0

            # Compute block variance
            Block = imnorm[i:i+blockSize, j:j+blockSize]
            blockVar = np.var(Block, ddof=1)

            # Considering spatially prominent blocks 
            if blockVar > activityThreshold:
                ActivityMask[i:i+blockSize, j:j+blockSize] = True
                WHSA = 1
                NHSA += 1

                # Analyze Block for noticeable artifacts
                blockImpaired = noticeDistCriterion(Block, nSegments, blockSize-1, windowSize, blockImpairedThreshold, blockSize)

                if blockImpaired:
                    WNDC = 1
                    NoticeableArtifactsMask[i:i+blockSize, j:j+blockSize] = True

                # Analyze Block for Gaussian noise distortions
                blockSigma, blockBeta = noiseCriterion(Block, blockSize-1, blockVar)

                if blockSigma > 2 * blockBeta:
                    WNC = 1
                    NoiseMask[i:i+blockSize, j:j+blockSize] = True

                # Pooling/ distortion assignment
                distBlockScores += WHSA * WNDC * (1 - blockVar) + WHSA * WNC * blockVar
                a='a'

    # Quality score computation
    # C is a positive constant, it is included to prevent numerical instability
    C = 1
    Score = ((distBlockScores + C) / (C + NHSA)) * 100

    # if input image is padded then remove those portions from ActivityMask,
    # NoticeableArtifactsMask and NoiseMask and ensure that size of these masks
    # are always M-by-N.
    if isPadded:
        NoticeableArtifactsMask = NoticeableArtifactsMask[:originalSize[0], :originalSize[1]]
        NoiseMask = NoiseMask[:originalSize[0], :originalSize[1]]
        ActivityMask = ActivityMask[:originalSize[0], :originalSize[1]]

    return Score, NoticeableArtifactsMask, NoiseMask, ActivityMask
    #return Score


## Function to Validate Input Image
def validateInputImage(I):
    # Check if input is a numpy array
    if not isinstance(I, np.ndarray):
        raise ValueError('Input image is not a numpy array')

    # Check for non-empty, non-sparse, real, non-NaN, finite
    if I.size == 0:
        raise ValueError('Input image is empty')
    
    if np.isnan(I).any():
        raise ValueError('Input image contains NaN values')
    
    if np.isinf(I).any():
        raise ValueError('Input image contains infinite values')
    
    if np.iscomplexobj(I):
        raise ValueError('Input image is not real')

    # Check for supported classes (data types)
    supported_dtypes = [np.uint8, np.uint16, np.int16, np.float32, np.float64]
    if I.dtype not in supported_dtypes:
        raise ValueError('Input image data type is not supported')

    # Check for valid image dimensions
    if len(I.shape) not in [2, 3]:
        raise ValueError('Invalid image format: Expected 2D or 3D array')

    if len(I.shape) == 3 and I.shape[2] != 3:
        raise ValueError('Invalid image format: Expected 3-channel color image')
        
    return I


# Function to analyze block for Gaussian noise distortions
def noiseCriterion(Block, blockSize, blockVar):
    # Compute block standard deviation
    blockSigma = np.sqrt(blockVar)    
    # Compute ratio of center and surround standard deviation
    cenSurDev = centerSurDev(Block, blockSize)    
    # Relation between center-surround deviation and the block standard deviation
    blockBeta = np.abs(blockSigma - cenSurDev) / np.maximum(blockSigma, cenSurDev)
    
    return blockSigma, blockBeta


# Function to compute center surround Deviation of a block
def centerSurDev(Block, blockSize):
    # block center
    center1 = (blockSize+1)//2
    center2 = center1+1
    center = np.concatenate((Block[:, center1-1], Block[:, center2-1]), axis=0)

    # block surround
    Block = np.delete(Block, (center1-1), axis=1)
    Block = np.delete(Block, (center2-1), axis=1)

    # Compute standard deviation of block center and block surround
    center_std = np.std(center, ddof=1)
    surround_std = np.std(Block, ddof=1)
    
    # Ratio of center and surround standard deviation
    cenSurDev = center_std / surround_std
    
    # Check for nan's
    if np.isnan(cenSurDev):
        cenSurDev = 0
    
    return cenSurDev


# Function to analyze block for noticeable artifacts
def noticeDistCriterion(Block, nSegments, blockSize, windowSize, blockImpairedThreshold, N):

    # Top edge of block
    topEdge = Block[0, :]
    segTopEdge = segmentEdge(topEdge, nSegments, blockSize, windowSize)

    # Right side edge of block
    rightSideEdge = Block[:, N-1]
    rightSideEdge = rightSideEdge.T
    segRightSideEdge = segmentEdge(rightSideEdge, nSegments, blockSize, windowSize)

    # Down side edge of block
    downSideEdge = Block[N-1, :]
    segDownSideEdge = segmentEdge(downSideEdge, nSegments, blockSize, windowSize)

    # Left side edge of block
    leftSideEdge = Block[:, 0]
    leftSideEdge = leftSideEdge.T
    segLeftSideEdge = segmentEdge(leftSideEdge, nSegments, blockSize, windowSize)

    # Compute standard deviation of segments in left, right, top and down side edges of a block
    segTopEdge_stdDev = np.std(segTopEdge, axis=1, ddof=1)
    segRightSideEdge_stdDev = np.std(segRightSideEdge, axis=1, ddof=1)
    segDownSideEdge_stdDev = np.std(segDownSideEdge, axis=1, ddof=1)
    segLeftSideEdge_stdDev = np.std(segLeftSideEdge, axis=1, ddof=1)

    # Check for segment in block exhibits impairedness, if the standard deviation of the segment is less than blockImpairedThreshold.
    blockImpaired = 0
    for seg_index in range(segTopEdge.shape[0]):
        if ((segTopEdge_stdDev[seg_index] < blockImpairedThreshold) or 
            (segRightSideEdge_stdDev[seg_index] < blockImpairedThreshold) or 
            (segDownSideEdge_stdDev[seg_index] < blockImpairedThreshold) or 
            (segLeftSideEdge_stdDev[seg_index] < blockImpairedThreshold)):
            blockImpaired = 1
            break

    return blockImpaired

# Function to segment block edges
def segmentEdge(blockEdge, nSegments, blockSize, windowSize):
    # Segment is defined as a collection of 6 contiguous pixels in a block edge
    segments = np.zeros((nSegments, windowSize))
    for i in range(nSegments):
        segments[i, :] = blockEdge[i: windowSize]
        if windowSize <= (blockSize + 1):
            windowSize += 1
    return segments

