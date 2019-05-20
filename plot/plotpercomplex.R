b7f=c()
foo = seq(1,7)
for (i in foo){b7f=c(b7f,read.table(file=paste('1b7f-frag',i,'.lrmsd',sep=""))[,2])}

cvj=c()
foo = seq(1,6)
for (i in foo){
cvj=c(cvj,read.table(file=paste('1cvj-frag',i,'.lrmsd',sep=""))[,2])}

mgz=c()
foo = seq(1,10)
for (i in foo){mgz=c(mgz,read.table(file=paste('2mgz-frag',i,'.lrmsd',sep=""))[,2])}

yh1=c()
foo = seq(1,6)
for (i in foo){yh1=c(yh1,read.table(file=paste('2yh1-frag',i,'.lrmsd',sep=""))[,2])}

nnh=c()
foo = seq(1,8)
for (i in foo){nnh=c(nnh,read.table(file=paste('3nnh-frag',i,'.lrmsd',sep=""))[,2])}

bs2=c()
foo = seq(1,8)
for (i in foo){bs2=c(bs2,read.table(file=paste('4bs2-frag',i,'.lrmsd',sep=""))[,2])}

ub7f=c()
foo = seq(1,7)
for (i in foo){ub7f=c(ub7f,read.table(file=paste('unbound-1b7f-frag',i,'.lrmsd',sep=""))[,2])}

uyh1=c()
foo = seq(1,6)
for (i in foo){uyh1=c(uyh1,read.table(file=paste('unbound-2yh1-frag',i,'.lrmsd',sep=""))[,2])}

b7fS=read.table('1b7f-fragments')[,1]
cvjS=read.table('1cvj-fragments')[,1]
mgzS=read.table('2mgz-fragments')[,1]
yh1S=read.table('2yh1-fragments')[,1]
nnhS=read.table('3nnh-fragments')[,1]
bs2S=read.table('4bs2-fragments')[,1]

ub7fS=read.table('unbound-1b7f-fragments')[,1]
uyh1S=read.table('unbound-2yh1-fragments')[,1]

tot=list(b7f,b7fS,c(),c(),ub7f,ub7fS,c(),c(),cvj,cvjS,c(),c(),mgz,mgzS,c(),c(),yh1,yh1S,c(),c(),uyh1,uyh1S,c(),c(),nnh,nnhS,c(),c(),bs2,bs2S)

colors=c("green","magenta","white","white")

cols=c(colors,colors,colors,colors,colors,colors,colors,colors,colors)

names = c("1b7f","u-1b7f","1cvj","2mgz","2yh1","u-2yh1","3nnh","4bs2")

minim = c(min(b7f),min(b7fS),-1,-1,min(ub7f),min(ub7fS),-1,-1,min(cvj),min(cvjS),-1,-1,min(mgz),min(mgzS),-1,-1,min(yh1),min(yh1S),-1,-1,min(uyh1),min(uyh1S),-1,-1,min(nnh),min(nnhS),-1,-1,min(bs2),min(bs2S))
maxim = c(max(b7f),max(b7fS),-1,-1,max(ub7f),max(ub7fS),-1,-1,max(cvj),max(cvjS),-1,-1,max(mgz),max(mgzS),-1,-1,max(yh1),max(yh1S),-1,-1,max(uyh1),max(uyh1S),-1,-1,max(nnh),max(nnhS),-1,-1,max(bs2),max(bs2S))

postscript(file='bestrmsdpercomplex-2.ps',horiz=FALSE,onefile=FALSE,width=8,height=10)
boxplot(tot, outline = FALSE, axes = FALSE,las=1,main="Lrmsd of all docking poses per complex",ylab="LRMSD (A)",pars=list(ylim=c(0,36)),col=cols)
axis(1, at=c(1.5,5.5,9.5,13.5,17.5,21.5,25.5,29.5), lab=names,cex.axis=2,pos=0,las=0)
axis(2, at=seq(0,36,by=2), lab=seq(0,36,by=2),cex.axis=2,las=1)
points(minim,col=cols)
points(maxim,col=cols)
dev.off()


