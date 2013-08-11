from haystack import indexes

from . import models

class PresentationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    presenter = indexes.CharField(model_attr='presenter')
    mytitle = indexes.CharField(model_attr='title')
    def get_model(self):
        return models.Presentation
