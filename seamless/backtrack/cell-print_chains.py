import numpy as np

f1=open("chains.txt","w")
f2=open("chains.occurencies","w")
occ = result['occurencies']
for i, a in enumerate(result["chains"]):
    for j in a:
        print(j+1, end=' ', file=f1)
    print('',end='\n',  file=f1)
    print(occ[i], file=f2)
f1.close()
f2.close()


return
