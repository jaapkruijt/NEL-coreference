
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
    bart = leo.bart
    name_jaap = Literal("Jaap")
    name_bart = Literal("Bart")
    instance_1 = Literal("12/08/2021")
    instance_2 = Literal("05/07/2021")
    instance_3 = Literal("08/08/2021")
    g.add((jaap, RDFS.label, name_jaap))
    g.add((jaap, gaf.denotedIn, instance_1))
    g.add((jaap, gaf.denotedIn, instance_2))
    g.add((jaap, gaf.denotedIn, instance_3))
    g.add((jaap_2, RDFS.label, name_jaap))
    g.add((jaap_2, gaf.denotedIn, instance_1))
    g.add((bart, RDFS.label, name_bart))
    g.add((bart, gaf.denotedIn, instance_2))
    return g

def add_data(graph, name):
    gaf = Namespace('http://groundedannotationframework.org/gaf#')
    leo = Namespace('http://cltl.nl/leolani/world/')
    graph.bind('rdfs', RDFS)
    graph.bind('gaf', gaf)


def pop_query(graph, q_param):
    q = """
        prefix gaf: <http://groundedannotationframework.org/gaf#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        select ?ent (COUNT(DISTINCT ?e) as ?num_mentions) where{
            ?ent rdfs:label "%s".
            
            ?ent gaf:denotedIn ?e.
            }
            
        group by ?ent
            order by DESC(COUNT(DISTINCT ?e))
    
    """
    result_list = []
    for row in graph.query(q % q_param):
        uri = row[0][0:]
        occurrences = row[1][0:]
        result_list.append((uri, occurrences))
    return result_list

def rec_query(graph, q_param):
    q = """
        prefix gaf: <http://groundedannotationframework.org/gaf#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        select distinct ?inst ?s
        where{
            ?s rdfs:label "%s".
            ?s gaf:denotedIn ?inst
        }
        group by ?inst
            ORDER BY DESC (?s)
    """

    result_list = []
    for row in graph.query(q % q_param):
        # uri = row[0][0:]
        result_list.append(row)

    return result_list

if __name__ == "__main__":
    data = make_fake_data()
    popularity = pop_query(data, "Jaap")
    recency = rec_query(data, "Jaap")
    print(popularity)
    print(recency)


