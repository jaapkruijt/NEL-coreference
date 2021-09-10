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
from cltl.brain.utils.helper_functions import read_query


class NamedEntityLinker(BasicBrain):

    def __init__(self, address, log_dir, clear_all=False):

        super(NamedEntityLinker, self).__init__(address, log_dir, clear_all, is_submodule=True)

    # Problem: How are uri's defined right now in the brain? Is ambiguity taken into account?
    # Otherwise uri's are the same
    # E.g. if labels are firstname-lastname then query needs to be RE only looking at part before hyphen

    def link_entities(self, ne_text, baseline='popularity'):
        if baseline == 'popularity':
            uri = self._get_most_popular(ne_text)
        elif baseline == 'recency':
            uri = self._get_most_recent(ne_text)
        return uri

    def _get_most_popular(self, ne_text):
        query = read_query('/Users/jaapkruijt/Documents/GitHub/NEL-coreference/popularity') % ne_text
        response = self._submit_query(query)
        # print(response)
        pop_ordered = []
        for row in response:
            uri = row['ent']['value']
            occurrences = row['num_mentions']['value']
            pop_ordered.append((uri, occurrences))
        if pop_ordered:
            uri, popularity = pop_ordered[0]
        # else:
        #
        #     # TODO add functionality to add entity to graph
        return uri

    def _get_most_recent(self, ne_text):
        pass











