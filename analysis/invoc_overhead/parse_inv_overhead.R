library("ggplot2")
library("latex2exp")
library("flextable")

aspRatio = 0.5
w = 5

path = "../../data/invocation_overhead"
systems = c("aws", "azure", "gcp")
folders = c("cold_payload", "warm_payload")

rm(complete_data)

for (system in systems) {
  if (system == "aws") {
    system_name <- "AWS"
  }
  else if(system == "gcp") {
    system_name <- "GCP"
  }
  else {
    system_name <- "Azure"
  }
  for (folder in folders) {
    
    datafile = paste(path,system, folder, "result-processed.csv", sep = "/")
      
    if (file.exists(datafile)) {
      datatmp = read.csv2(datafile, sep=",", stringsAsFactors=FALSE)
      datatmp$payload_size = round(as.numeric(as.character(datatmp$payload_size)))/10^6
      datatmp$invocation_time = (as.numeric(as.character(datatmp$invocation_time)))
      datatmp = datatmp[c("payload_size", "invocation_time")]
      if (folder == "cold_payload") {
        datatmp$experiment = paste(system_name, " cold start", sep = ",")
      }
      else if (folder == "cold_payload_second") {
        datatmp$experiment = paste(system_name, " cold start 2", sep = ",")
      }
      else {
        datatmp$experiment = paste(system_name, " warm start", sep = ",")
      }
      
      if (exists('complete_data') && is.data.frame(get('complete_data'))) {
        complete_data <- rbind(complete_data, datatmp)
      }
      else {
        complete_data <- datatmp
      }
    }
    
  }
}

pdf(file = "inv_overhead.pdf", width = w, height = w * aspRatio)
  
p <- ggplot(data = complete_data, aes(x=payload_size, y=invocation_time, color=experiment, shape=experiment)) + 
  geom_point()+
  geom_smooth(method=lm) +
   theme_bw(20) +
  theme_minimal() +
  ylab("Invocation Time [s]") +
  xlab("Payload Size [MB]") +
  ylim(0,22) +
  guides(col=guide_legend(ncol=2)) +
  theme(legend.position = c(0.29, 0.87), legend.title = element_blank()) 
  
  print(p)
  dev.off()
