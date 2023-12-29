from pyswip import Prolog

prolog = Prolog()


prolog.consult('temp.pl')
print(list(prolog.query('solve(X)'))[0]['X'])

