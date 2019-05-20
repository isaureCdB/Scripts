convert-cg-aa.py lastrna.npy lastrna-aa.npy  \
    --libcg Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy \
#    --libaa Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy Ur.npy \
    --libaa U.npy U.npy U.npy U.npy U.npy U.npy U.npy U.npy U.npy U.npy U.npy


npy2pdb.py lastrna-aa.npy boundfrag/n1-11-aa.pdb > lastrna-aa.pdb
#npy2pdb.py lastrna-aa.npy boundfrag/n1-11r.pdb > lastrna-aa.pdb
