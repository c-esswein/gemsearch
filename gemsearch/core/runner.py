from time import time
import sys
import codecs
from pprint import pprint

from gemsearch.embedding.ge_calc import GeCalc

# use utf-8 for stdout (playlist names contain sometimes strange chars)
if sys.stdout.encoding != 'utf-8':
  sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'utf-8':
  sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def run_pipeline(dataDir, iterator, embeddings, evaluations):
    print('=== started pipeline ===')
    startTime = time()

    # create items
    for item in iterator['iterator'].iterate(iterator['typeHandlers']):
        for generator in iterator['generators']:
            if generator.generateItem(item) == True:
                item['trainingOnly'] = True
    
    # close handlers
    for generator in iterator['generators']:
        generator.close_generation()
    for typeHandler in iterator['typeHandlers']:
        typeHandler.close_type_handler()

    print('\n%% generation took: {}s'.format(time() - startTime))

    # embed
    print('\n=== embedding ===')
    # TODO: multiple embeddings require multiple datadir (work in memory otherwise...)
    for embedding in embeddings:
        em = embedding.start_embedding(dataDir)
        ge = GeCalc(dataDir)

        # evaluation
        print('\n=== evaluation ===')
        for evaluation in evaluations:
            print('\n>>> run evaluation: ' + evaluation.name)
            # try:
            evaluation.evaluate(ge)
            # except Exception as e:
                # print('Evaluation crashed')

    print('\n=== finished pipeline ===')
    print('%% total time: {}s'.format(time() - startTime))
