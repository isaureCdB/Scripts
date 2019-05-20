a9nS=read.table('1a9n-fragments')[,3]
b7fS=read.table('1b7f-fragments')[,3]
cvjS=read.table('1cvj-fragments')[,3]
cjkS=read.table('2cjk-fragments')[,3]
mgzS=read.table('2mgz-fragments')[,3]
yh1S=read.table('2yh1-fragments')[,3]
nnhS=read.table('3nnh-fragments')[,3]
bs2S=read.table('4bs2-fragments')[,3]
n0tS=read.table('4n0t-fragments')[,3]

totS=list(a9nS,b7fS,cvjS,cjkS,mgzS,yh1S,nnhS,bs2S,n0tS)
names = c("1a9n","1b7f","1cvj","2cjk","2mgz","2yh1","3nnh","4bs2","4n0t")
minim = c(min(a9nS),min(b7fS),min(cvjS),min(cjkS),min(mgzS),min(yh1S),min(nnhS),min(bs2S),min(n0tS))
maxim = c(max(a9nS),max(b7fS),max(cvjS),max(cjkS),max(mgzS),max(yh1S),max(nnhS),max(bs2S),max(n0tS))
postscript(file='bestrmsdpercomplex-2.ps',horiz=FALSE,onefile=FALSE,width=8,height=10)
boxplot(tot, varwidth = TRUE, outline = FALSE, names=names, outwex = 0, las=1,main="Lrmsd of all docking poses per complex",ylab="LRMSD (A)",,pars=list(ylim=c(0,36)))
points(minim,col="red")
points(maxim,col="red")
dev.off()


