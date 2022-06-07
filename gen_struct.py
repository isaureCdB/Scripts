header="""#pivot auto
#centered receptor: false
#centered ligands: false
"""

template = """0           0           0           0           0           0
           {:.3f}    {:.3f}   {:.3f}   {:.3f}    {:.3f}   {:.3f}
"""
#0 and 2*PI
import math
# math.pi

seed = sys.argv[1]

result = header
for i in range(10): 
    ran = [random.seed(seed), random.seed(seed), random.seed(seed)] 
    r = ran * 2 * math.pi
    result += "#%i\n"%n
    result += template.format(r[0], r[1], r[2], offset["x"], offset["y"], offset["z"])
