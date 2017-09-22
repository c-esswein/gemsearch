import numpy as np
import scipy.spatial.distance
from gemsearch.embedding.ge_calc import cos_cdist

def calc_viz_data(items, vizEmbedding):
    ''' Resolve visualization 3d positions, calculate relative position to first position.
    '''

    if len(items) < 1:
        return items

    # resolve 3d position and calc relative pos to first point
    centerPos = None
    for idx, item in enumerate(items):
        absPosition = vizEmbedding[item['embeddingIndex']]

        if idx > 0:
            item['position'] = np.subtract(absPosition, centerPos).tolist()
        else:
            # center point
            centerPos = absPosition
            item['position'] = [0, 0, 0]

    return items

def cluster_items(items, minClusterDistance):
    ''' Clusters items with distances smaller than minClusterDistance (percentage of bounding box)
    '''
    boundingBox =[[0, 0, 0], [0, 0, 0]]

    if len(items) < 1:
        return items, boundingBox

    # calculate distances to center (center is 0,0,0 --> length of vector)
    for item in items:
        item['distanceToCenter'] = np.linalg.norm(item['position'])

        # calculating boundingBox
        boundingBox = [
            np.minimum(boundingBox[0], item['position']),
            np.maximum(boundingBox[1], item['position'])
        ]

    # total max axis bounding size
    boundingSize = np.amax([np.absolute(boundingBox[0]), boundingBox[1]]) * 2

    # ---- calculate clusters ----
    minElementDistance = minClusterDistance * boundingSize
    print('boundingSize {}'.format(boundingSize))    
    print('minElementDistance {}'.format(minElementDistance))

    clusters = []
    for item in items:
        isInCluster = False
        # check if element can be appended to existing cluster
        for cluster in clusters:
            dist = scipy.spatial.distance.euclidean(item['position'], cluster[0]['position'])
            if dist < minElementDistance:
                cluster.append(item)
                isInCluster = True # to continue also in second loop
                break
        
        if not isInCluster:
            # create new cluster
            clusters.append([item])

    return clusters, np.array(boundingBox)
