## Clicking in conversation: Short gaps between turns signal connection
## Emma Templeton

# Code to reproduce all analyses, in order that they are reported

install.packages(c('lme4','lmerTest','lsr'))

library(lme4)
library(lmerTest)
library(lsr)

setwd("/Users/Emma/Dropbox/Manuscripts/clicking_repo") # CHANGE PATH

#################### STUDY 1 ###########################

# ______________________________________________________
# ARE THE STRANGERS REALLY 'STRANGERS'?

data_qualtrics <- read.csv("./Analyses/post_convo_survey_with_factors_strangers.csv")

mean(data_qualtrics[['knew_before']])
sd(data_qualtrics[['knew_before']])

# ______________________________________________________
# GAP LENGTH --> ENJOYMENT, CONNECTION 
# (Across conversation analysis)

data_qualtrics <- read.csv("./Analyses/post_convo_survey_with_factors_strangers.csv")
data_connection <- read.csv("./Analyses/connection_strangers.csv") 
data_turn_taking <- read.csv("./Analyses/turn_taking_strangers.csv")
merged_DVs <- merge(data_qualtrics, data_connection, by=c("subID","partnerID"))
merged <- merge(merged_DVs, data_turn_taking, by=c("subID","partnerID"))

model_enjoyment <- lmer(scale(factor_1) ~ scale(mean_gap_convo) +  
                          (1 | subID), data=merged)
summary(model_enjoyment)

model_connection <- lmer(scale(avg_connection) ~ scale(mean_gap_convo) +  
                           (1 | subID), data=merged)
summary(model_connection)

# ______________________________________________________
# GAP LENGTH --> CONNECTION
# (Within conversation analysis: Strangers)

data_binned <- read.csv("./Analyses/binned_connection_and_gaps_strangers.csv")
data_subset <- data_binned[c("connection_20", "gap_length_mean_20", "bin_num", "subID", "dyad")]
data_subset_no_nans <- na.omit(data_subset)

model_binned <- lmer(scale(connection_20) ~ scale(gap_length_mean_20) + scale(bin_num) + (1 | subID) + (1 | dyad), data=data_subset_no_nans)
summary(model_binned)


#################### STUDY 2 ###########################

# ______________________________________________________
# GAP LENGTH --> CONNECTION
# (Within conversation analysis: Friends)

data_binned <- read.csv("./Analyses/binned_connection_and_gaps_friends.csv")
data_subset <- data_binned[c("connection_20", "gap_length_mean_20", "bin_num", "subID", "dyad")]
data_subset_no_nans <- na.omit(data_subset)

model_binned <- lmer(scale(connection_20) ~ scale(gap_length_mean_20) + scale(bin_num) + (1 | subID) + (1 | dyad), data=data_subset_no_nans)
summary(model_binned)

#################### STUDY 3 ###########################

# ______________________________________________________
# MANIPULATED GAPS --> PERCEIVED ENJOYMENT, CONNECTION

data <- read.csv("./Data/manipulated_gaps.csv")

model_enjoy <- lmer(enjoy ~ condition + (1 | subID) + (1 | convo), data=data)
#model_enjoy <- lmer(enjoy ~ condition + (1 | subID), data=data) # version that converges
summary(model_enjoy)
anova(model_enjoy)
pairwise.t.test(data$enjoy, data$condition, p.adj = "holm")

model_connect <- lmer(connected ~ condition + (1 | subID) + (1 | convo), data=data)
summary(model_connect)
anova(model_connect)
pairwise.t.test(data$connected, data$condition, p.adj = "holm")

# Get significance bars for visualization
# Using values centered within subject
data <- read.csv("./Analyses/manipulated_gaps_centered.csv")
A = data[data$convo == 'A',]
B = data[data$convo == 'B',]
C = data[data$convo == 'C',]
D = data[data$convo == 'D',]
E = data[data$convo == 'E',]
F = data[data$convo == 'F',]

pairwise.t.test(A$enjoy_centered, A$condition, p.adj = "holm")
pairwise.t.test(B$enjoy_centered, B$condition, p.adj = "holm")
pairwise.t.test(C$enjoy_centered, C$condition, p.adj = "holm")
pairwise.t.test(D$enjoy_centered, D$condition, p.adj = "holm")
pairwise.t.test(E$enjoy_centered, E$condition, p.adj = "holm")
pairwise.t.test(F$enjoy_centered, F$condition, p.adj = "holm")

pairwise.t.test(A$connected_centered, A$condition, p.adj = "holm")
pairwise.t.test(B$connected_centered, B$condition, p.adj = "holm")
pairwise.t.test(C$connected_centered, C$condition, p.adj = "holm")
pairwise.t.test(D$connected_centered, D$condition, p.adj = "holm")
pairwise.t.test(E$connected_centered, E$condition, p.adj = "holm")
pairwise.t.test(F$connected_centered, F$condition, p.adj = "holm")

#################### STUDY 4 ###########################

# ______________________________________________________
# FRIENDS VS STRANGERS (independent)

data_friends <- read.csv("./Analyses/turn_taking_friends.csv")
data_strangers <- read.csv("./Analyses/turn_taking_strangers.csv")

t.test(data_friends$mean_gap_convo, data_strangers$mean_gap_convo, var.equal = FALSE)
cohensD(data_friends$mean_gap_convo, data_strangers$mean_gap_convo, method = 'unequal')

t.test(data_friends$median_gap_convo, data_strangers$median_gap_convo, var.equal = FALSE)
cohensD(data_friends$median_gap_convo, data_strangers$median_gap_convo, method = 'unequal')

# chi-square test is in the notebook "chi-square test (do friends use more "long gaps"?)"
# in the project's Github repo

# ______________________________________________________
# FRIENDS VS STRANGERS (paired)

# This version has one value for Friend and one value for Stranger for each of the
# 22 participants who had both friend and stranger conversations
# (not reported in the main text)
data_friends_and_strangers <- read.csv("./Analyses/friends_vs_strangers.csv")

t.test(data_friends_and_strangers$mean_gap_friends, data_friends_and_strangers$mean_gap_strangers, paired=TRUE)
cohensD(data_friends_and_strangers$mean_gap_friends, data_friends_and_strangers$mean_gap_strangers, method='paired')

t.test(data_friends_and_strangers$median_gap_friends, data_friends_and_strangers$median_gap_strangers, paired=TRUE)
cohensD(data_friends_and_strangers$median_gap_friends, data_friends_and_strangers$median_gap_strangers, method='paired')

# ______________________________________________________
# LONG GAP RATING TASK

data_rating <- read.csv("./Analyses/long_gap_ratings_long_format.csv")
data_info <- read.csv("./Data/long_gap_stimuli_info.csv")
merged <- merge(data_rating, data_info, by=c("video_num"))

merged$video_num <- as.factor(merged$video_num)
merged$rater <- as.factor(merged$rater)
merged$laughter_present <- as.factor(merged$laughter_present)
merged$laughter_who <- as.factor(merged$laughter_who)
merged$gestures_present <- as.factor(merged$gestures_present)
merged$rater_know_person <- as.factor(merged$rater_know_person)

# Difference by condition (friend / stranger)
# (for continous variables)

model_awkward <- lmer(scale(awkward) ~ condition +  
                        (1 | rater), data=merged)
summary(model_awkward)

model_connected <- lmer(scale(connected) ~ condition +  
                          (1 | rater), data=merged)
summary(model_connected)

model_topics <- lmer(scale(topics) ~ condition +  
                       (1 | rater), data=merged)
summary(model_topics)

model_genuine_laugh <- lmer(scale(laughter_genuine) ~ condition +  
                              (1 | rater), data=merged)
summary(model_genuine_laugh)

# Explore Condition x Interval interaction
# (for continuous variables)
model_awkward <- lmer(scale(awkward) ~ condition * scale(interval) +  
                        (1 | rater), data=merged)
summary(model_awkward)

model_connected <- lmer(scale(connected) ~ condition * scale(interval) +  
                          (1 | rater), data=merged)
summary(model_connected)

model_topics <- lmer(scale(topics) ~ condition * scale(interval) +  
                       (1 | rater), data=merged)
summary(model_topics)

model_genuine_laugh <- lmer(scale(laughter_genuine) ~ condition * scale(interval) +  
                              (1 | rater), data=merged)
summary(model_genuine_laugh)

# Differences in counts by condition (friend / stranger)
# (for categorical variables)

data_wide <- read.csv("./Analyses/long_gap_ratings_wide_format.csv")
data_info <- read.csv("./Data/long_gap_stimuli_info.csv")
merged <- merge(data_wide, data_info, by=c("video_num"))

merged$video_num <- as.factor(merged$video_num)
merged$laughter_consensus <- as.factor(merged$laughter_consensus)
merged$laughter_who_consensus <- as.factor(merged$laughter_who_consensus)
merged$laughter_who_consensus_binary <- as.factor(merged$laughter_who_consensus_binary)
merged$gestures_consensus <- as.factor(merged$gestures_consensus)

table(merged$condition, merged$laughter_consensus)
chisq.test(table(merged$condition, merged$laughter_consensus))

table(merged$condition, merged$gestures_consensus)
chisq.test(table(merged$condition, merged$gestures_consensus))

table(merged$condition, merged$laughter_who_consensus_binary)
chisq.test(table(merged$condition, merged$laughter_who_consensus_binary))
chisq.test(table(merged$condition, merged$laughter_who_consensus_binary), simulate.p.value = TRUE)
