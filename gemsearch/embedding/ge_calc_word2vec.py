import numpy as np
import csv
import random
import sys
import scipy.spatial.distance
from gemsearch.core.data_loader import traverseTypes
import gensim.models


class GeCalcWord2Vec:
    '''Class to load and query embeddings. word2vec keyed vectors are used as backend
    to compute similarities.
    '''

    def __init__(self):
        self.word2vecWv = None  # embeddings array
        self.lookup = None  # type lookup, maps embedding key to type data

    def load_lookup(self, typeFile):
        '''Loads type mapping.
        '''

        self.lookup = list(traverseTypes(typeFile))

    def load_node2vec_data(self, embeddingFile, typeFile):
        '''Loads embedding (stored in node2vec format) and type mapping.
        '''

        self.word2vecWv = gensim.models.KeyedVectors.load_word2vec_format(
            embeddingFile, binary=False)
        self.load_lookup(typeFile)

    def get_item_info_by_index(self, index):
        '''Get item by embedding index.
        '''
        return self.lookup[index]

    def get_items_from_word2vec(self,
                                resWords,
                                typeFilter=None,
                                limit=sys.maxsize,
                                offset=0,
                                skipIds=[]):
        '''Maps embedding words to items. Optional type Filter can be applied. Items are skiped if id is in skipIds.
        '''
        result = []
        found = 0
        for embeddingIndex, weight in resWords:
            itemInfo = self.lookup[int(embeddingIndex)]

            # filter type based on typeFilter
            if (typeFilter is
                    not None) and (itemInfo['type'] not in typeFilter):
                continue

            # check if item should be skiped
            if itemInfo['id'] in skipIds:
                continue

            # check offset
            if offset > 0:
                offset -= 1
                continue

            # valid item
            result.append(itemInfo)
            found += 1
            if found == limit:
                break

        return result

    def get_item_by_item_id(self, itemId):
        '''Returns item info for obj id.
        '''
        for item in self.lookup:
            if item['id'] == itemId:
                return item
        return None

    def get_embedding_for_id(self, id):
        ''' Returns embedding vector of given id.
        '''
        searchItem = self.get_item_by_item_id(id)
        if searchItem is None:
            raise ValueError('item id not found: ' + id)
        itemVec = self.word2vecWv.word_vec(str(searchItem['embeddingIndex']))

        return itemVec

    def query_by_ids(self,
                     ids,
                     typeFilter=None,
                     limit=20,
                     offset=0,
                     skipIds=[]):
        '''Query by obj ids.
        '''
        weightedIds = [(searchId, 1.0) for searchId in ids]
        return self.query_by_ids_weighted(weightedIds, typeFilter, limit, offset, skipIds)

    def query_by_ids_weighted(self,
                              ids,
                              typeFilter=None,
                              limit=20,
                              offset=0,
                              skipIds=[]):
        '''Query by obj ids.
        '''
        searchWords = []
        for searchId, weight in ids:
            item = self.get_item_by_item_id(searchId)
            searchWords.append((str(item['embeddingIndex']), weight))

        simEmbeddingVecs = self.word2vecWv.most_similar(searchWords, topn=1000)
        # make sure search item itself is also contained:
        # TODO: test effect with multiple ids!!
        simEmbeddingVecs.insert(0, searchWords[0])
        result_items = self.get_items_from_word2vec(
            simEmbeddingVecs, typeFilter, limit, offset, skipIds)

        return result_items

    def query_by_ids_cosmul(self,
                            ids,
                            typeFilter=None,
                            limit=20,
                            offset=0,
                            skipIds=[]):
        '''Query by obj ids.
        '''
        searchWords = []
        for searchId in ids:
            item = self.get_item_by_item_id(searchId)
            searchWords.append(item['embeddingIndex'])

        simEmbeddingVecs = self.word2vecWv.most_similar_cosmul(
            searchWords, topn=1000)
        result_items = self.get_items_from_word2vec(
            simEmbeddingVecs, typeFilter, limit, offset, skipIds)

        return result_items

    def query_by_vec(self,
                     searchVec,
                     typeFilter=None,
                     limit=20,
                     offset=0,
                     skipIds=[]):
        ''' Query by embeddings searchVec
        '''
        simEmbeddingVecs = self.word2vecWv.similar_by_vector(
            searchVec, topn=1000)
        result_items = self.get_items_from_word2vec(
            simEmbeddingVecs, typeFilter, limit, offset, skipIds)

        return result_items

    def random_query_results(self, typeFilter=None, limit=20):
        '''Returns random entries with given optional typeFilter
        '''
        maxIndex = len(self.lookup)
        result = []

        while len(result) < limit:
            randomIndex = random.randint(0, maxIndex - 1)
            itemInfo = self.get_item_info_by_index(randomIndex)
            if (typeFilter is None) or (itemInfo['type'] in typeFilter):
                result.append(itemInfo)

        return result

    def get_lookup(self):
        #TODO: still used by api?
        return self.lookup
