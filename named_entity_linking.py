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

from cltl.brain.utils import base_cases
from cltl.brain.basic_brain import BasicBrain
from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.helper_functions import read_query

from cltl.brain.infrastructure.rdf_builder import RdfBuilder
from rdflib import RDFS, Literal

class NamedEntityLinker(LongTermMemory):

    def __init__(self, address, log_dir, clear_all=False):

        super(NamedEntityLinker, self).__init__(address, log_dir, clear_all)

    def link_entities(self, ne_list, baseline='popularity'):
        uri_list = []
        for ne_text in ne_list:
            if baseline == 'popularity':
                uri = self._get_most_popular(ne_text)
                uri_list.append((uri, ne_text))
            elif baseline == 'recency':
                uri = self._get_most_recent(ne_text)
                uri_list.append((uri, ne_text))
        return uri_list

    def _get_most_popular(self, ne_text):
        query = read_query('/Users/jaapkruijt/Documents/GitHub/NEL-coreference/popularity') % ne_text
        response = self._submit_query(query)
        # print(response)
        pop_ordered = []
        for row in response:
            print(row)
            uri = row['ent']['value']
            occurrences = row['num_mentions']['value']
            pop_ordered.append((uri, occurrences))
        if pop_ordered:
            uri, popularity = pop_ordered[0]
        else:
            uri_name = f'{ne_text}_1'
            uri = self._rdf_builder.create_resource_uri('LW', uri_name)
        return uri

    def _get_most_recent(self, ne_text):
        pass

    def add_labels(self, capsule, uri=None):
        ent_uri = self._rdf_builder.create_resource_uri('LW', capsule['subject']['id']) if not uri else uri
        for label in capsule['labels']:
            self.instance_graph.add((ent_uri, RDFS.label, Literal(label)))

    def add_labels_2(self, identity, labels, uri=None):
        ent_uri = self._rdf_builder.create_resource_uri('LW', identity) if not uri else uri
        for label in labels:
            self.instance_graph.add((ent_uri, RDFS.label, Literal(label)))

    def update_brain(self):

        data = self._serialize(self._brain_log())
        code = self._upload_to_brain(data)


if __name__ == "__main__":
    import pathlib

    log_path = pathlib.Path('./logs')
    print(type(log_path))
    nel = NamedEntityLinker(address="http://localhost:7200/repositories/sandbox",
                            log_dir=log_path)
    nel.add_labels_2('jaap_1', ['jaap', 'PhD', 'hij'])
    nel.update_brain()











