
def run_pipeline(dataDir, iterator, embeddings, evaluations):
    print('=== started pipeline ===')

    # create items
    for item in iterator['iterator'].iterate(iterator['typeHandlers']):
        for generator in iterator['generators']:
            generator.generateItem(item)
    
    # close handlers
    for generator in iterator['generators']:
        generator.close_generation()
    for typeHandler in iterator['typeHandlers']:
        typeHandler.close_type_handler()

    # embed
    print('\n=== embedding ===')
    for embedding in embeddings:
        em = embedding.start_embedding(dataDir)

        # evaluation
        print('\n=== evaluation ===')
        for evaluation in evaluations:
            print('run evaluation: ' + evaluation.name)
            evaluation.evaluate(em)

    print('\n=== finished pipeline ===')
