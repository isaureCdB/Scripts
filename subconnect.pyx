#%%cython --a
cimport numpy as np
cimport cython
import numpy as np
ctypedef int[2] two_int
@cython.boundscheck(False)
@cython.wraparound(False)  # turn off negative index wrapping for entire function
@cython.cdivision(True)
def subconnect(double[:,:,:] preatoms,
               double[:,:,:] postatoms,
               int[:,:] connections, float max_msd):
    cdef float r
    cdef int i, x, at, c0, c1, c, nat
    cdef double[:,:] coor1, coor2
    cdef int nconn = len(connections)
    cdef np.ndarray[char, ndim=1, mode="c"] new_connections = np.zeros(nconn, dtype=np.uint8)
    c = 999
    nat = preatoms.shape[1]
    for i in range(nconn):
        c0, c1 = connections[i,0],connections[i,1] 
        if c0 != c:
            c = c0
            coor1 = preatoms[c0]
        coor2 = postatoms[c1]
        r = 0
        for at in range(nat):
            for x in range(3):
                r += (coor2[at,x]-coor1[at,x])**2
        r = r/nat
        if r <= max_msd:
            new_connections[i] = 1
    return np.array(connections)[new_connections.astype(np.bool)]
