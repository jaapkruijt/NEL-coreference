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

def make_fake_data():
    gaf = Namespace('http://groundedannotationframework.org/gaf#')
    leo = Namespace('http://cltl.nl/leolani/world/')
    g = Graph()
    g.bind('rdfs', RDFS)
    g.bind('gaf', gaf)
    jaap = leo.jaap
    jaap_2 = leo.jaap_2
    tae = leo.tae
    name_jaap = Literal("Jaap")
    name_tae = Literal("Tae")
    instance_1 = Literal("1")
    instance_2 = Literal("2")
    instance_56 = Literal("56")
    g.add((jaap, RDFS.label, name_jaap))
    g.add((jaap, gaf.denotedBy, instance_1 ))
    g.add((jaap, gaf.denotedBy, instance_2))
    g.add((jaap, gaf.denotedBy, instance_56))
    g.add((jaap_2, RDFS.label, name_jaap))
    g.add((jaap_2, gaf.denotedBy, instance_1))
    g.add((tae, RDFS.label, name_tae))
    g.add((tae, gaf.denotedBy, instance_2))
    return g

def query_data(graph):
    q = """
        prefix gaf: <http://groundedannotationframework.org/gaf#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        select* {
        select ?ent (COUNT(DISTINCT ?e) as ?num_mentions) where{
            ?ent rdfs:label "Jaap".
            
            ?ent gaf:denotedBy ?e.
            }
            
        group by ?ent
            order by DESC(COUNT(DISTINCT ?e))
        }
    
    """
    for row in graph.query(q):
        print(f'{row[0]}, {row[1]}')

if __name__ == "__main__":
    data = make_fake_data()
    query_data(data)



