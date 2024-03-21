require(quanteda)
require(quanteda.textmodels)
require(quanteda.textstats)
require(quanteda.textplots)
require(ggplot2)
require(readr)

## TTR #########

### L1 ########

# load texts from L1 writer
L1_texts <- read_delim("~/Dev/ALiG/Data/L1/results/general/L1_texts.csv", delim = "\t", escape_double = FALSE, trim_ws = TRUE)

# Analysing TTR for all files (Attention: Tokenized by the TTR tool and not manually)
L1_corpus <- corpus(L1_texts)
docnames(L1_corpus) <- paste(L1_corpus$file, L1_corpus$L1_1, sep = "-")
toks_L1 <- tokens(L1_corpus, remove_punct = TRUE, remove_numbers = TRUE) %>% 
  tokens_remove(pattern = stopwords("de", source = "marimo")) %>% 
  tokens_keep(pattern = "^[\\p{script=Latn}]+$", valuetype = "regex")

# Calculate all values of lexical diversity
dfm_L1 <- dfm(toks_L1)
tstat_lexdiv <- textstat_lexdiv(dfm_L1, "all")

# Plot TTR?
plot(tstat_lexdiv$TTR, type = "l", xaxt = "n", xlab = NULL, ylab = "TTR")
grid()
axis(1, at = seq_len(nrow(tstat_lexdiv)), labels = dfm_L1$L1_1)

### L2 ########

# load texts from L2 writers
L2_texts <- read_delim("~/Dev/ALiG/Data/L2/results/general/L2_texts.csv", delim = "\t", escape_double = FALSE, trim_ws = TRUE)

# Analysing TTR for all files (Attention: Tokenized by the TTR tool and not manually)
L2_corpus <- corpus(L2_texts)
summary(L2_corpus)
docnames(L2_corpus) <- paste(L2_corpus$L1_1, L2_corpus$file, sep = "-")
toks_L2 <- tokens(L2_corpus, remove_punct = TRUE, remove_numbers = TRUE) %>% 
  tokens_remove(pattern = stopwords("de", source = "marimo")) %>% 
  tokens_keep(pattern = "^[\\p{script=Latn}]+$", valuetype = "regex")

# Calculate all values of lexical diversity
dfm_L2 <- dfm(toks_L2)
tstat_lexdiv2 <- textstat_lexdiv(dfm_L2, "all")

# Sort it and try to plot it
t <- data.frame(tstat_lexdiv2)
t$L1 <- L2_corpus$L1_1
test <- t[order(t$L1, decreasing = TRUE),]
t$L1 <- as.factor((t$L1))
summary(t)

new <- t %>%
  group_by(L1) %>%
  summarise_at(vars(TTR), list(name = mean))


## Manually Tokenised #########

## Sort by sum of tokens (manually tokenised)
library(dplyr)

### L2 ###########

# load texts from L2 writer
L2_tok <- read_delim("~/Dev/ALiG/Data/L2/results/general/token_sum.csv", delim = "\t", escape_double = FALSE, trim_ws = TRUE)

# Calculate mean per language pair (for token sum)
L2_L_mean<- L2_tok %>%
  group_by(L1_1, L1_2) %>%
  summarise_at(vars(sum), list(name = mean))

# Calculate IQR per language pair (for token sum)
L2_L_iqr<- L2_tok %>%
  group_by(L1_1, L1_2) %>%
  summarise_at(vars(sum), list(name = IQR))

# Calculate amount of speakers per language pair (for token sum)
L2_amount <- L2_tok %>% count(L1_1, L1_2)

# Fuse data frames
L2_L <- L2_L_mean
L2_L$IQR <- L2_L_iqr$name
L2_L$amount <- L2_amount$n

# write in file
write.csv(L2_L , "token_per_language_L2.csv", row.names=FALSE)


### L1 ###########

# load texts from L1 writer
L1_tok <- read_delim("~/Dev/ALiG/Data/L1/results/general/token_sum.csv", delim = "\t", escape_double = FALSE, trim_ws = TRUE)

# Calculate mean per language pair (for token sum)
L1_L_mean<- L1_tok %>%
  group_by(L1_1, L1_2, L1_3) %>%
  summarise_at(vars(sum), list(name = mean))

# Calculate IQR per language pair (for token sum)
L1_L_iqr<- L1_tok %>%
  group_by(L1_1, L1_2, L1_3) %>%
  summarise_at(vars(sum), list(name = IQR))

# Calculate amount of speakers per language pair (for token sum)
L1_amount <- L1_tok %>% count(L1_1, L1_2, L1_3)

# Fuse data frames
L1_L <- L1_L_mean
L1_L$IQR <- L1_L_iqr$name
L1_L$amount <- L1_amount$n

# write in file
write.csv(L1_L , "token_per_language_L1.csv", row.names=FALSE)

# Testing to visualize
L2_tok
plot(L2_tok$sum, data = L2_tok)
with(L2_tok,text(L2_tok$sum, labels=L2_tok$L1_1, pos=4))

ggplot(L2_tok, aes(x=L1_1, y=sum, color=L1_1)) + 
  geom_point(size=6)

