
def run_pipeline(dataDir, itemIterator, typeHandlers, graphGenerator, embedding, evaluations):
    print('=== started pipeline ===')

    # create items
    for item in itemIterator.iterate(typeHandlers):
        graphGenerator.processItem(item)
    graphGenerator.close_generation()

    # embed
    print('=== embedding ===')
    embedding.start_embedding()

    # evaluation
    print('=== evaluation ===')
    for evaluation in evaluations:
        print('run evaluation: ' + evaluation.name)
        evaluation.evaluate()

    print('=== finished pipeline ===')
