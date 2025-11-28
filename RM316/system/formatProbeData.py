import statistics 

probes_strings = [x for x in input().split("(")]

trimmed_probes = []

for i, p in enumerate(probes_strings):
    if p == '':
        continue

    p = p.strip()

    if p[-1] == ')':
        p = p[:-1]

    trimmed_probes.append(p)
    
probes = [[float(y) for y in x.split(" ")] for x in trimmed_probes]
probes = [pow(x[0]*x[0] + x[1]*x[1] + x[2]*x[2], 0.5) for x in probes]

for vel in probes:
    print(vel)