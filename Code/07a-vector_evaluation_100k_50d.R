## Author: Ryan McMahon
## File: "~/Track2Vec/Code/07a-vector_evaluation_100k_50d.R"
## Date Created: 03/07/2017
## Date Last Modified: 03/07/2017
##
## Purpose: Explore the vectors produced by a GloVe model with the most frequent 
#           100k (99,997) tracks on Spotify; embedding dimension is 50.
#
#
## NOTES:
#           
# 
#
## EDITS:
#         
#

## Program and Hardware Information:
# R 3.1.3 "Smooth Sidewalk"; 64-bit
# Windows 8.1; MSi GE60 2PL Apache Laptop

################################################################################


##############################
### 0) SET UP
##############################
rm(list=ls())
options(stringsAsFactors = F)
set.seed(11769)
setwd("C:/Users/rbm166/Dropbox/Track2Vec/Data/")


# 0a) Cosine Similarity Function:
cos_similarity <- function(x.vec, y.vec, data, new_colname){
  
  x.vec <- as.matrix(x.vec)
  y.vec <- as.matrix(y.vec)
  
  cos_sim <- y.vec %*% t(x.vec)
  data[,new_colname] <- cos_sim[,1]

  return(data)
  
}


# 0b) Analogy Function:
analogy <- function(q_vecs, y.vec, data, new_colname){
  
  # 'q_vecs' is an ordered list of the analogy vectors; 
  #   e.g., "q_vecs[[1]] is to q_vecs[[2]] as q_vecs[[3]] is to ______"
  
  if(length(q_vecs) != 3) {
    print("Need list of three vectors! In order!")
    break
  }
  
  x.vec <- as.matrix(q_vecs[[2]] - q_vecs[[1]] + q_vecs[[3]])
  d <- sqrt(sum(x.vec^2))
  x.norm <- t(t(x.vec)/d)
  
  y.vec <- as.matrix(y.vec)
  
  dist <- y.vec %*% t(x.norm)
  
  data[,new_colname] <- dist[,1]
  
  return(data)
  
}

##############################
### 1) DATA PROCESSING
##############################

# 1a) Read in the track info and vectors:
df <- read.csv(file = "01-vectors_lookup_combined100k_50d.csv")

# 1b) Rename the first column from 'X' to 'track_id':
colnames(df)[1] <- "track_id"

# 1c) Order the data frames by track frequency:
df <- df[order(df$freq, decreasing=T), ]

# 1d) Put the embeddings into a separate matrix:
X <- df[,grep(pattern = "X[0-9]{1,2}", x = colnames(df), ignore.case = T)]

# 1e) Create a training set for PCA:
train.samp <- sample(x = nrow(X), size = 5000, replace = T)
X.train <- X[train.samp,]


##############################
### 2) PRINCIPAL COMPONENTS
##############################

# 2a) Fit PCA model to the training data:
vec.pca <- prcomp(x = X.train, retx = T, center = F, scale. = F)

# 2b) Inspect the results:
summary(vec.pca)
plot(vec.pca)
biplot(vec.pca)

# 2c) Fit the model to all of the embeddings:
X.pca <- predict(object = vec.pca, newdata = X)

# 2d) Generate new data frame with rotated embeddings:
new.df <- as.data.frame(cbind(df[,1:14], X.pca))


##############################
### 3) ANALYSIS:
##############################


plot(new.df$PC1[1:250], new.df$PC2[1:250], type = "n")
text(x = new.df$PC1[1:250], y = new.df$PC2[1:250], labels = new.df$artist_names[1:250], cex = 0.5)


# 3a) Similarity 
similarity.df <- df[,1:14]

#   i) 'Me, Myself, and I' - G-Eazy & Bebe Rexha
id.temp <- '40YcuQysJ0KlGQTeGUosTC'
x.vec <- df[df$track_id==id.temp, 15:ncol(df)]
y.vec <- df[, 15:ncol(df)]
new_colname <- "me.my.i.cos"
similarity.df <- cos_similarity(x.vec = x.vec, y.vec = y.vec, 
                                new_colname = new_colname, data = similarity.df)

head(similarity.df[order(similarity.df$me.my.i.cos, decreasing=T),], 20)


#   ii) 'Killing in the Name' - Rage Against the Machine
id.temp <- "59WN2psjkt1tyaxjspN8fp"
x.vec <- df[df$track_id==id.temp, 15:ncol(df)]
new_colname <- "kill.in.name.cos"
similarity.df <- cos_similarity(x.vec = x.vec, y.vec = y.vec, 
                                new_colname = new_colname, data = similarity.df)

head(similarity.df[order(similarity.df$kill.in.name.cos, decreasing=T),], 20)


#   iii) 'Drunk' - Ed Sheeran
id.temp <- "4RnCPWlBsY7oUDdyruod7Y"
x.vec <- df[df$track_id==id.temp, 15:ncol(df)]
new_colname <- "drunk.sheeran.cos"
similarity.df <- cos_similarity(x.vec = x.vec, y.vec = y.vec, 
                                new_colname = new_colname, data = similarity.df)

head(similarity.df[order(similarity.df$drunk.sheeran.cos, decreasing=T),], 20)


#   iv) Average of all 50 Cent songs:
x.vec <- t(apply(df[grep(pattern = '50 Cent', x = df$artist_names), 15:ncol(df)],2,mean))
new_colname <- "fiftycent.avg.cos"
similarity.df <- cos_similarity(x.vec = x.vec, y.vec = y.vec, 
                                new_colname = new_colname, data = similarity.df)


head(similarity.df[order(similarity.df$fiftycent.avg.cos, decreasing=T),], 20)




# 3b) Analogies: 

analogy.df <- df[,1:14]

#   i) "Photograph" - Ed Sheeran is to "Thinking Out Loud" - Ed Sheeran as "Enter Sandman" - Metallica is to _________
#       - the Ed Sheeran songs are on the same album.

ids.temp <- c('1HNkqx9Ahdgi1Ixy2xkKkL', '34gCuhDGsG4bRPIf9bb02f', '1hKdDCpiI9mqz1jVHRKG0E')
q_vecs = list(df[df$track_id==ids.temp[1], 15:ncol(df)], 
              df[df$track_id==ids.temp[2], 15:ncol(df)], 
              df[df$track_id==ids.temp[3], 15:ncol(df)])
y.vec <- df[, 15:ncol(df)]
new_colname <- "ed_ed_metallica.analogy"
analogy.df <- analogy(q_vecs = q_vecs, y.vec = y.vec, 
                                new_colname = new_colname, data = analogy.df)

head(analogy.df[order(analogy.df$ed_ed_metallica.analogy, decreasing=T),], 20)
