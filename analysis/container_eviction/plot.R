library("ggplot2")
library("latex2exp")
library("flextable")

aspRatio = 0.75
w = 10

path = "."
folders = c("aws_nodejs_sleep_1", "aws_python_sleep_10", "aws_python_sleep_1", "aws_python_heavy_sleep_1")


for (folder in folders) {
  
  all_precip_files <- list.files(pattern = sprintf("results_%s_.*\\.csv", folder), full.names = TRUE)
  print(sprintf("results_%s_*.csv", folder))
  print(all_precip_files)
  
  #expfolder = sub(pattern = "/", replacement = "", folder)
  for (file in all_precip_files) {
    
    data = read.csv2(file, sep=",")
    data = data[(data$Invocations == 20) | (data$Invocations == 12) | (data$Invocations == 8),]
    data$Epoch = floor(data$DeltaT / 380)
    
    model = data.frame(Epoch=seq(0,3,length.out=40), Invocations=rep(c(8,12,20),40))
    model$WarmContainers = model$Invocations * 2^(-model$Epoch)
    
    
    expname = sub(pattern = "(.*)\\..*$", replacement = "\\1", basename(file))
  
    pdf_path <- paste(expname, ".pdf", sep="")
    write(pdf_path, stdout()) 
    #pdf(file=pdf_path, width = w, height = w*aspRatio)
    
    p <- ggplot(data=data, aes(x=as.factor(Epoch), y=WarmContainers, fill=as.factor(Invocations))) +
      geom_violin(position="identity") +
      geom_line(data=model, aes(x=Epoch+1, y=WarmContainers, linetype=as.factor(Invocations), color=as.factor(Invocations)), show.legend=F) +
      scale_x_discrete(TeX("Periods after start $p =\\frac{\\Delta T}{380s} $ (380s per period)"))+
      scale_fill_discrete(TeX("Initial invocations $D_{init}$")) +
      ylim(0,21) +
      scale_y_continuous(TeX("Number of warm containers $D_{warm}$")) +
      annotate("text", label=TeX("Model: $D_{warm} = D_{init} \\cdot 2^{-p}$", output="character"), parse=T, x=2.4, y=18, size = 10) +
      annotate("segment", x=1.8, y=16.6, xend=1.4, yend=15.4, arrow=arrow(length=unit(0.12, "inches"))) +
      annotate("segment", x=1.8, y=16.6, xend=1.4, yend=9.5, arrow=arrow(length=unit(0.12, "inches"))) +
      annotate("segment", x=1.8, y=16.6, xend=1.6, yend=5.5, arrow=arrow(length=unit(0.12, "inches"))) +
      theme_bw(20) +
      theme(legend.position = c(0.8, 0.5), axis.text=element_text(size=24), axis.title=element_text(size=28,face="bold"), legend.title = element_text(size=24), legend.text = element_text(size=28))

    ggsave(pdf_path, device = cairo_pdf, width = w, height = w*aspRatio)
    # print(p)
    #dev.off()
  }
}
