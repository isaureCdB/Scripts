xpmrenum=function(XPM){

r=as.matrix(read.table(paste(XPM,'.num', sep='')))
R=r
for (i in 1:200){R[i,]=r[201-i,]}
R=t(R)
write.table(R,file=paste(XPM,'.renum',sep=''),row.names=FALSE, col.names=FALSE)
}
