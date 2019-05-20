./scripts/trilib-to-dilib-print.py

for a in T G ; do for b in T G; do for c in T G; do
    m=$a$b$c
    fastcluster_npy.py dilib/$m/conf-aa-all.npy 1.0
    subcluster_npy.py dilib/$m/conf-aa-all.npy dilib/$m/conf-aa-all-clust1.0 0.2
done
