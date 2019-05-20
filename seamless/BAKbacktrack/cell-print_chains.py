import numpy as np

f1=open("chains.txt","w")
f2=open("chains.occurencies","w")
for i, a in result["chains"]:
    for j in a:
        print(j, end=' ', file=f1)
    print('',end='\n',  file=f1)
    print(i, file=f2)
f1.close()
f2.close()


return
