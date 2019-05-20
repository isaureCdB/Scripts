"""
meanrank_filter.py
Filters the connectivity graph (generated by connect.py) by (geometric) meanrank
Eliminates all connections that cannot participate in chains with a good-enough mean rank
prints out (to stdout) the total number of chains that can be formed

If a output filename is provided, the filtered connectivity graph is written there

Copyright 2015-2017 Sjoerd de Vries, Isaure Chauvot de Beauchene, TUM
"""

import sys, json
import numpy as np
from math import log

# Implementation feature
# chunks contain the logrank of 10000 of the downstream chains
# starting from the considered pose.
CHUNKSIZE = 10000

# Global variables:
# List of poses/connections to be deleted
# because they don't have any valid downstream chain
deletions = []
connection_deletions = []

voidarray = np.empty(dtype="float", shape=(0,))
class Cluster(object):
  def __init__(self, frag, rank):
    self.frag = frag # index of fragment in chain
    self.rank = rank # ATTRACT rank of the pose
    self.logrank = log(rank)
    self.connections = [] # list of downstream connections
    self.has_chunks = True # has no chunk if optimus already above threshold
    self.back_connections = 0 # number of upstream connections
    self.good_connections = set() # downstream connections that can give chunks
    self.done_once = False # all downstream connections have been visited
                           # and good connections have been defined
    self.pos = -1 # to which of its downstream connection it is asking for chunks
    self.done = False  # self.pos has reached the end (all chunks have been given)
  def cut_connection(self):
    # delete a connection with an upstream pose
    # e.g. if no chain with good score can be built
    assert self.back_connections > 0 #e.g. we're not at he 1st pool
    self.back_connections -= 1
    if self.back_connections == 0:
      # delete a pose if it has no upstream connection
      # and cut all its downstream connections
      deletions.append(self)
      if self.done_once:
        # all downstream connections have been visited
        for cnr, c in enumerate(self.connections):
          if cnr in self.good_connections:
            # the connection was not yet cut
            # (e.g. for having a bad optimus)
            c.cut_connection()
      else:
        for c in self.connections:
          c.cut_connection()
  def reset(self):
    if self.has_chunks:
      self.pos = -1
      self.done = False  
  def precalc(self):
    # determine self.optimus = the lowest optimus in its 
    # downstream connections + self.logrank
    opt = self.logrank
    if len(self.connections):
      opt += min([con.optimus for con in self.connections])
    self.optimus = opt
    if self.optimus > max_logrank:
      # there is no possible chain from this pose with an acceptable score
      self.has_chunks = False
      self.chunk = voidarray
  def make_chunk(self):
    if not self.has_chunks:
      return
    assert not self.done
    if self.frag == nfrags: # we are at the last fragment in chain => return
      self.done = True
      self.has_chunks = False
      self.chunk = np.array([self.logrank])
      assert min(self.chunk) == self.logrank
      return
    
    assert len(self.connections), self.frag # chech there are downstream connections
    chunk = np.zeros(CHUNKSIZE)
    chunksize = 0
    oldpos = self.pos
    if self.pos == -1:
      self.connections[0].reset()
      self.connections[0].make_chunk()
      self.pos = 0 # index of downstream connection to call, in list of connected poses
    con = self.connections[self.pos] # downstream connection to call
    while 1:            
      bad_optimus = (self.logrank + con.optimus > max_logrank)
      if bad_optimus:
        # if all downstream chains would give a bad score (>threshold)
        self.connections[self.pos].reset()
        self.pos += 1
        if self.pos < len(self.connections): # go to next connection
          con = self.connections[self.pos]
          con.reset()
          con.make_chunk()
          continue
        else:
          self.done = True
          break
      else:    
        # add the current logrank to each value of the chunk 
        cchunk = con.chunk
        cchunk = cchunk + self.logrank
        cchunk = cchunk[cchunk<max_logrank] # discard too high scores
        if len(cchunk):
          if len(cchunk) + chunksize > CHUNKSIZE:
            break
          if not self.done_once:
            self.good_connections.add(self.pos)
          chunk[chunksize:chunksize+len(cchunk)] = cchunk      
          chunksize += len(cchunk)
      
      if con.done:
        self.pos += 1
        if self.pos < len(self.connections):
          con = self.connections[self.pos]
          con.reset()                  
        else:
          self.done = True
          break
      con.make_chunk()
          
    if self.frag > 0:
      assert chunksize > 0, (self.frag, self.optimus, self.logrank, max_logrank, oldpos, self.pos, len(self.connections), [c.optimus for c in self.connections], [len(c.chunk) for c in self.connections])
    self.chunk = chunk[:chunksize]
    if self.done and oldpos == -1: #we got everything in one go      
      self.has_chunks = False 
    if self.done and not self.done_once:
      self.done_once = True
      for cnr,c in enumerate(self.connections):
        if cnr not in self.good_connections:
          c.cut_connection()
          connection_deletions.append((self, c))
        
if __name__ == "__main__":
  # The json file is the output of connect.py
  # It contains the list of connected poses/custers
  # for each pair of consecutive fragments
  tree = json.load(open(sys.argv[1]))

  # Define a maximal score/energy for the whole chain,
  # which we'll use for pruning
  max_meanrank = float(sys.argv[2])

  # output (optional)
  outtree = sys.argv[3]

  nfrags = tree["nfrags"]
  max_logrank = log(max_meanrank) * nfrags
      
  clusters = [] #list-of-lists-of-Cluster objects, 1 list per frag
  for fragnr, tclus in enumerate(tree["clusters"]):
    clus = []
    for pose in tclus:  # tclus is a dictionary
      #for now, limit ourselves to fully collapsed trees
      # = there is only one pose per cluster, or, at least, all poses are within 0.1 A (deredundant)
      assert pose["radius"] == 0 # clustering radius = 0 (collapsed tree)
      ranks = np.array(pose["ranks"], dtype="int")
      if len(ranks) > 1:
        print >> sys.stderr, "Warning: duplicate structures detected: %s, selecting best structure" % ranks
      cc = Cluster(fragnr+1,ranks[0])
      clus.append(cc)
    clusters.append(clus)
  for fragnr, tinter in enumerate(tree["interactions"]):
    cluslist = clusters[fragnr]
    cluslist2 = clusters[fragnr+1]
    for source, target in tinter:  #(source, target) is a pair of connected poses
      # store the connections with next fragment
      # count number of connections with previous fragment
      cluslist[source].connections.append(cluslist2[target])
      cluslist2[target].back_connections += 1
    for clus in cluslist:
      clus.connections.sort(key = lambda con: con.rank)

  # for each frag, for each pose, compute what is the best-rank
  # half-chain from this pose to the end of the chain ("optimus")
  for cnr in reversed(range(len(clusters))): #from nfrag counting down 
    clus = clusters[cnr]
    for cc in clus:
      cc.precalc()

  supercluster = Cluster(0, 1)
  supercluster.optimus = 0
  supercluster.connections = clusters[0]
  for c in clusters[0]:
    c.back_connections = 1
  totcount = 0
  while not supercluster.done:
    supercluster.make_chunk()
    totcount += len(supercluster.chunk)
    print >> sys.stderr, totcount
  print totcount

  if outtree is not None:
    #write out tree
    otree = {"nfrags":nfrags, "max_rmsd": tree["max_rmsd"], "clusters": [], "interactions": []}
    tclusters = []
    clusmap = {}
    
    if supercluster not in deletions:
      deletions = set(deletions)
      connection_deletions = set(connection_deletions)
      for c in clusters:
        c[:] = [cc for cc in c if cc not in deletions]
        for cc in c:
          cc.connections = [con for con in cc.connections if con not in deletions and (cc, con) not in connection_deletions]      
        for ccnr, cc in enumerate(c):
          clusmap[id(cc)] = ccnr

      tclusters = otree["clusters"]
      for c in clusters:
        tc = []
        for cc in c:
          tcc = {"radius": 0, "ranks" : [cc.rank]}    
          tc.append(tcc)
        tclusters.append(tc)
      tinter = otree["interactions"]
      for cnr, c in enumerate(clusters[:-1]):
        tint = []
        for ccnr, cc in enumerate(c):
          for con in cc.connections:
            ind = clusmap[id(con)]
            tint.append((ccnr, ind))
        tinter.append(tint)     
    json.dump(otree, open(outtree, "w"))
