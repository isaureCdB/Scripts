Plot=function(a,d){
plot(d, pch=16,cex=1,ylim=c(0,max(a)),xlim=c(0,length(d)+1))
barplot(a$V2,space=c(0.5,0,0,0,0,0),add=T)
barplot(a$V3, add=T, col='yellow', space=c(0.5,0,0,0,0,0))
barplot(a$V4, add=T, col='red', space=c(0.5,0,0,0,0,0))
points(d, pch=16,cex=1)
}
