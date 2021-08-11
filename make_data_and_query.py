
from rdflib import Namespace, Graph, Literal
from rdflib.namespace import RDFS

# TODO: change instances to dates
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


# TODO: change query to take in string
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
    result_list = []
    for row in graph.query(q):
        # print(f'{row[0]}, {row[1]}')
        print(row[0],row[1])
        result_list.append((row[0],row[1]))
    return result_list


if __name__ == "__main__":
    data = make_fake_data()
    results = query_data(data)
    print(results)


