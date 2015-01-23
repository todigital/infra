#!/usr/bin/Rscript

args <- commandArgs(TRUE)
datafile <- args[1]
outfile <- paste0(datafile, ".c")
datafile
data = read.csv(datafile, header = TRUE)
wmatrix<-matrix(c(data$id,data$words,data$dots), ncol=3)
#xmatrix<-matrix(c(data$words,data$comas,data$dots,data$equal,data$urls,data$time,data$date), ncol=7)
cluster2<-kmeans(wmatrix,10)
result<-cbind(data,cluster2$cluster)
write.csv(result, file = outfile)
