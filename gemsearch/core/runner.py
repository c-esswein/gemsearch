from time import time

from gemsearch.embedding.ge_calc import GeCalc

def run_pipeline(dataDir, iterator, embeddings, evaluations):
    print('=== started pipeline ===')
    startTime = time()

    # create items
    for item in iterator['iterator'].iterate(iterator['typeHandlers']):
        for generator in iterator['generators']:
            generator.generateItem(item)
    
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
            print('run evaluation: ' + evaluation.name)
            evaluation.evaluate(ge)

    print('\n=== finished pipeline ===')
    print('%% total time: {}s'.format(time() - startTime))
