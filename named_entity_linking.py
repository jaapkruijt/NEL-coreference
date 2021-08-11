"""
Upon encountering NE do:
1) select NE token text as name
2) Query brain to find URI's with name (entities_with_label.rq)
3) if multiple URI's found:
    4) Query brain to count number of denotedBy links for each URI
    5) Rank URI's by number of links
    6) Select highest ranking URI
    7) Add URI to Annotation
3) if one URI found:
    4) Add URI to Annotation
3) if no URI's found:
    4) Add URI to brain
    5) Add URI to Annotation
"""

from rdflib import Namespace, Graph, Literal
from rdflib.namespace import RDFS
from make_data_and_query import make_fake_data, query_data
import spacy
import simple_ner

def named_entity_linking(ne_label, ne_text, data):
    label_with_text = zip(ne_label, ne_text)
    for label, text in label_with_text:
        query_data(data) % label  # TODO get operand thing to work

if __name__ == '__main__':
    nlp = spacy.load('en_core_web_sm')
    entities = simple_ner.named_entity_recognition()






