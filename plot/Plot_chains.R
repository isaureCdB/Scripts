colors=c(col_1cvj,col_2yh1,col_2cjk,col_1b7f,col_1a9n,col_3nnh,col_4bs2,col_2mgz,col_4n0t)

Nb=c(Nb_1cvj,c(0),Nb_2yh1,c(0),Nb_2cjk,c(0),Nb_1b7f,c(0),Nb_1a9n,c(0),Nb_3nnh,c(0),Nb_4bs2,c(0),Nb_2mgz,c(0),Nb_4n0t)

inf2=c(inf2_1cvj,c(0),inf2_2yh1,c(0),inf2_2cjk,c(0),inf2_1b7f,c(0),inf2_1a9n,c(0),inf2_3nnh,c(0),inf2_4bs2,c(0),inf2_2mgz,c(0),inf2_4n0t)

inf3=c(inf3_1cvj,c(0),inf3_2yh1,c(0),inf3_2cjk,c(0),inf3_1b7f,c(0),inf3_1a9n,c(0),inf3_3nnh,c(0),inf3_4bs2,c(0),inf3_2mgz,c(0),inf3_4n0t)

inf4=c(inf4_1cvj,c(0),inf4_2yh1,c(0),inf4_2cjk,c(0),inf4_1b7f,c(0),inf4_1a9n,c(0),inf4_3nnh,c(0),inf4_4bs2,c(0),inf4_2mgz,c(0),inf4_4n0t)

min=c(min_1cvj,c(0),min_2yh1,c(0),min_2cjk,c(0),min_1b7f,c(0),min_1a9n,c(0),min_3nnh,c(0),min_4bs2,c(0),min_2mgz,c(0),min_4n0t)


N=c(Nb,1,10,100,1000)
Nblog=log(N+1)
ad5=c(inf5,0,0,0,0)
inf5log=log(ad5+1)
ad4=c(inf4,0,0,0,0)
inf4log=log(ad4+1)
ad3=c(inf3,0,0,0,0)
inf3log=log(ad3+1)
ad2=c(inf2,0,0,0,0)
inf2log=log(ad2+1)

m=c(min,0.5,1,1.5,2)

postscript("re2chains_5e4-e5-2e5.eps",width=60,height=7)
barplot(Nblog, col=c(colors), ylim=c(0,8), axes=FALSE)
par(new=TRUE)
barplot(inf5log, col=1, angle=45, axes=FALSE, ylim=c(0,8), density=10)
par(new=TRUE)
barplot(inf4log, col=1, angle=45, axes=FALSE, ylim=c(0,8), density=20)
par(new=TRUE)
barplot(inf3log, col=1, angle=-45, axes=FALSE, ylim=c(0,8), density=20)
par(new=TRUE)
barplot(inf2log, col=1, angle=0, axes=FALSE, ylim=c(0,8), density=100)
par(new=TRUE)
plot(m,xlim=c(0.6,81.4), axes=FALSE,pch=21,bg="white",)
axis(4,at=c(0,1,2,3,4,5,6,7,8,9),pos=82,las=1,font=0.5)
axis(2,at=c(0,log(2),log(11),log(101),log(1001)),labels=c(0,1,10,100,1000),pos=0,las=1,font=0.5)
dev.off()


postscript("chains_5e4-e5-2e5_inf23_draft6.eps",width=30,height=5)
barplot(Nblog, col=c(colors), ylim=c(0,8), axes=FALSE)
par(new=TRUE)
barplot(inf3log, col=1, angle=45, axes=FALSE, ylim=c(0,8), density=20)
par(new=TRUE)
barplot(inf2log, col="black",axes=FALSE, ylim=c(0,8))
par(new=TRUE)
plot(m,xlim=c(0.6,79.4), axes=FALSE,pch=21,bg="white",)
axis(4,at=c(0,1,2,3,4,5,6,7,8,9),pos=82,las=1,font=0.5)
axis(2,at=c(0,log(2),log(11),log(101),log(1001)),labels=c(0,1,10,100,1000),pos=0,las=1,font=0.5)
dev.off()


