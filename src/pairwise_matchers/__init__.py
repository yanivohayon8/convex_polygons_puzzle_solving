from src.factory import Factory

factory = Factory()

def pairwise_pieces(bag_of_pieces,matchers_keys,**kwargs):
    key2matcher = {}

    for matcher_key in matchers_keys:
        matcher_obj = factory.create(matcher_key,pieces=bag_of_pieces,**kwargs)
        matcher_obj.pairwise()
        key2matcher[matcher_key] = matcher_obj 
    
    return key2matcher

