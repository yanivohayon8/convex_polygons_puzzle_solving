from src.factory import Factory

factory = Factory()

def pairwise_pieces(bag_of_pieces,matchers,**kwargs):

    for matcher in matchers:
        matcher_ = factory.create(matcher,pieces=bag_of_pieces,**kwargs)
        matcher_.pairwise()

