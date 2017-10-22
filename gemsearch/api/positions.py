import numpy as np
import scipy.spatial.distance
from gemsearch.embedding.ge_calc import cos_cdist
import sys

def calc_viz_data(items, vizEmbedding):
    ''' Resolve visualization 3d positions.
    '''

    if len(items) < 1:
        return items

    # resolve 3d position and calc relative pos to first point
    for idx, item in enumerate(items):
        absPosition = vizEmbedding[item['embeddingIndex']]
        item['position'] = absPosition.tolist()

    return items

def cluster_items(items, minClusterDistance):
    ''' Clusters items with distances smaller than minClusterDistance (percentage of bounding box)
    '''
    minInt = -sys.maxsize - 1
    boundingBox =[[sys.maxsize, sys.maxsize, sys.maxsize], [minInt, minInt, minInt]]

    if len(items) < 1:
        return items, boundingBox

    # calculate bounding box
    for item in items:
        boundingBox = [
            np.minimum(boundingBox[0], item['position']),
            np.maximum(boundingBox[1], item['position'])
        ]

    # total max axis bounding size
    boundingSize = np.amax([np.absolute(boundingBox[0]), boundingBox[1]]) * 2

    # ---- calculate clusters ----
    minElementDistance = minClusterDistance * boundingSize
    ''' print('boundingSize {}'.format(boundingSize))    
    print('minElementDistance {}'.format(minElementDistance)) '''

    clusters = []
    for item in items:
        isInCluster = False
        # check if element can be appended to existing cluster
        for cluster in reversed(clusters):
            centerPos = cluster['center']
            dist = scipy.spatial.distance.euclidean(item['position'], centerPos)
            if dist < minElementDistance:
                # append to existing cluster
                cluster['items'].append(item)
                isInCluster = True

                # update position to be relative from center
                item['position'] = np.subtract(item['position'], centerPos).tolist()
                break
        
        if not isInCluster:
            # create new cluster
            centerPos = item['position']
            item['position'] = [0, 0, 0]
            clusters.append({
                'items': [item],
                'center': centerPos
            })

    # reset positions for cluster with only one element
    for cluster in clusters:
        if len(cluster['items']) == 1:
            cluster['items'][0]['position'] = cluster['center']

    return clusters, np.array(boundingBox)
