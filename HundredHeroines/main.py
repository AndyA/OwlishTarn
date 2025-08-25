from rdflib import Graph

g = Graph()
g.parse("ref/vra.html")
print(len(g))