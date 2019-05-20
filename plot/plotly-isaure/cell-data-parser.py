import glob

files = glob.glob("data/*-%s" % tailstr)
data = []
nfrag = {}
for f in files:
    complexname = f.split("/")[1][:-len(tailstr)-1]
    lines = list(open(f).readlines())
    assembly_schemes = []
    for lnr, l in enumerate(lines):
        l = l.strip()
        if l.startswith("**************"):
            assembly_schemes.append(lnr)
    assert len(assembly_schemes)
    frag = None
    try:
        pstart = assembly_schemes[assembly_scheme]
    except IndexError:
        continue
    assembly_schemes.append(len(lines))
    pend = assembly_schemes[assembly_schemes.index(pstart)+1]
    for l in lines[pstart+1:pend]:
        ll = l.split()
        if ll[0] == "fragment":
            frag = int(ll[1])
            continue
        if float(ll[0]) != cutoff:
            continue
        attract_hits = int(ll[1])
        ad_hits = int(ll[2])
        nfrag[complexname] = frag
        data.append((complexname, frag, attract_hits, ad_hits))
data.sort(key = lambda l : (nfrag[l[0]], l[0]))
#header = "complex,fragment,attract_hits,autodock_hits,attract_best,autodock_best"
header = "complex,fragment,attract_hits,autodock_hits"
data2 = ""
for l in data:
    data2 += ",".join([str(ll) for ll in l]) + "\n"
return header + "\n" + data2
