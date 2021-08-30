## Response time in conversation signals social connection
## Emma Templeton

# Code to reproduce all analyses, in order that they are reported
# 'gap length' = 'response time'

install.packages(c('lme4','lmerTest','lsr'))

library(lme4)
library(lmerTest)
library(lsr)

setwd("/Users/Emma/Dropbox/Manuscripts/clicking_repo")

#################### STUDY 1 ###########################

# ______________________________________________________
# ARE THE STRANGERS REALLY 'STRANGERS'?

data_qualtrics <- read.csv("./Analyses/post_convo_survey_with_factors_strangers.csv")

mean(data_qualtrics[['knew_before']])
sd(data_qualtrics[['knew_before']])

# ______________________________________________________
# ACROSS CONVERSATION ANALYSIS
# gap length --> enjoyment, connection 

data_qualtrics <- read.csv("./Analyses/post_convo_survey_with_factors_strangers.csv")
data_connection <- read.csv("./Analyses/connection_strangers.csv") 
data_turn_taking <- read.csv("./Analyses/turn_taking_strangers.csv")
merged_DVs <- merge(data_qualtrics, data_connection, by=c("subID","partnerID"))
merged <- merge(merged_DVs, data_turn_taking, by=c("subID","partnerID"))

#merged <- merged[ which(merged$knew_before < 50), ] # to limit analyses to true strangers

model_enjoyment <- lmer(scale(factor_1) ~ scale(mean_gap_convo) +  
                          (1 + scale(mean_gap_convo) | subID), data=merged)
summary(model_enjoyment)

model_connection <- lmer(scale(avg_connection) ~ scale(mean_gap_convo) +  
                           (1 + scale(mean_gap_convo) | subID), data=merged)
summary(model_connection)


# ______________________________________________________
# WITHIN CONVERSATION ANALYSIS
# gap length --> connection

data_binned <- read.csv("./Analyses/binned_connection_and_gaps_strangers.csv")
data_binned <- read.csv("./Analyses/binned_connection_and_gaps_by_speaker_strangers.csv")
data_subset <- data_binned[c("connection_20", "gap_length_mean_20", "bin_num", "subID", "dyad")]
data_subset_no_nans<-data_subset[!data_subset$bin_num>19,]
data_subset_no_nans$subID <- as.factor(data_subset_no_nans$subID)

model_binned <- lmer(scale(connection_20) ~ scale(gap_length_mean_20) + scale(bin_num) + (1 + scale(gap_length_mean_20) | subID) + (1 + scale(bin_num) | dyad), data=data_subset_no_nans)
summary(model_binned)

# ______________________________________________________
# INDIVIDUAL DIFFERENCES

data <- read.csv("./Analyses/individual_differences.csv")

model <- lm(scale(factor_1_partner_mean) ~ scale(mean_gap_speaker_self_mean), data=data)
summary(model)

model <- lm(scale(avg_connection_partner_mean) ~ scale(mean_gap_speaker_self_mean), data=data)
summary(model)

#################### STUDY 2 ###########################

# ______________________________________________________
# WITHIN CONVERSATION ANALYSIS
# gap length --> connection

data_binned <- read.csv("./Analyses/binned_connection_and_gaps_friends.csv")
data_subset <- data_binned[c("connection_20", "gap_length_mean_20", "bin_num", "subID", "dyad")]
data_subset_no_nans<-data_subset[!data_subset$bin_num>19,]
data_subset_no_nans$subID <- as.factor(data_subset_no_nans$subID)

model_binned <- lmer(scale(connection_20) ~ scale(gap_length_mean_20) + scale(bin_num) + (1 + scale(gap_length_mean_20) | subID) + (1 + scale(bin_num) | dyad), data=data_subset_no_nans)
summary(model_binned)

############### SELF / PARTNER EFFECTS #################

# ______________________________________________________
# Stranger Dataset  
# (Across conversation analysis)

data_qualtrics <- read.csv("./Analyses/post_convo_survey_with_factors_strangers.csv")
data_connection <- read.csv("./Analyses/connection_strangers.csv") 
data_turn_taking <- read.csv("./Analyses/turn_taking_strangers.csv")
merged_DVs <- merge(data_qualtrics, data_connection, by=c("subID","partnerID"))
merged <- merge(merged_DVs, data_turn_taking, by=c("subID","partnerID"))

model_enjoyment_t_p <- lmer(scale(factor_1) ~ scale(mean_gap_speaker) + scale(mean_gap_partner) +
                              (1 + scale(mean_gap_speaker) + scale(mean_gap_partner) | subID), data=merged)
summary(model_enjoyment_t_p)

model_connection_t_p <- lmer(scale(avg_connection) ~ scale(mean_gap_speaker) + scale(mean_gap_partner) +
                               (1 + scale(mean_gap_speaker) + scale(mean_gap_partner) | subID), data=merged)
summary(model_connection_t_p)

# contrast tests
df <- data.frame(matrix(unlist(coef(model_enjoyment_t_p)), nrow=66, byrow=FALSE))
names(df)[names(df) == 'X1'] <- 'intercept'
names(df)[names(df) == 'X2'] <- 'betas_speaker'
names(df)[names(df) == 'X3'] <- 'betas_partner'
df$partner_minus_speaker <- df$betas_partner - df$betas_speaker

t.test(df$partner_minus_speaker)

df <- data.frame(matrix(unlist(coef(model_connection_t_p)), nrow=66, byrow=FALSE))
names(df)[names(df) == 'X1'] <- 'intercept'
names(df)[names(df) == 'X2'] <- 'betas_speaker'
names(df)[names(df) == 'X3'] <- 'betas_partner'
df$partner_minus_speaker <- df$betas_partner - df$betas_speaker

t.test(df$partner_minus_speaker)

# ______________________________________________________
# Stranger Dataset  
# (Within conversation analysis)

data_binned <- read.csv("./Analyses/binned_connection_and_gaps_by_speaker_strangers.csv")
data_subset <- data_binned[c("connection_20",
                             "gap_length_mean_speaker_20",
                             "gap_length_mean_partner_20",
                             "bin_num", "subID", "dyad")]
data_subset_no_nans<-data_subset[!data_subset$bin_num>19,]
data_subset_no_nans$subID <- as.factor(data_subset_no_nans$subID)

model_binned <- lmer(scale(connection_20) ~ scale(gap_length_mean_speaker_20) + scale(gap_length_mean_partner_20) + scale(bin_num) + 
                       (1 + scale(gap_length_mean_speaker_20) + scale(gap_length_mean_partner_20) | subID) + 
                       (1 + scale(bin_num) | dyad), 
                     data=data_subset_no_nans)
summary(model_binned)

model_binned_converge <- update(model_binned, control=lmerControl(optimizer="bobyqa"))
summary(model_binned_converge)

# contrast test
df <- data.frame(matrix(unlist(coef(model_binned_converge)$subID), nrow=66, byrow=FALSE))
names(df)[names(df) == 'X1'] <- 'intercept'
names(df)[names(df) == 'X2'] <- 'betas_speaker'
names(df)[names(df) == 'X3'] <- 'betas_partner'
names(df)[names(df) == 'X4'] <- 'bin_num'
df$partner_minus_speaker <- df$betas_partner - df$betas_speaker

t.test(df$partner_minus_speaker)

# ______________________________________________________
# Friend Dataset  
# (Across conversation analysis)

data_binned <- read.csv("./Analyses/binned_connection_and_gaps_by_speaker_friends.csv")
data_subset <- data_binned[c("connection_20",
                             "gap_length_mean_speaker_20",
                             "gap_length_mean_partner_20",
                             "bin_num", "subID", "dyad")]
data_subset_no_nans<-data_subset[!data_subset$bin_num>19,]
data_subset_no_nans$subID <- as.factor(data_subset_no_nans$subID)

model_binned <- lmer(scale(connection_20) ~ scale(gap_length_mean_speaker_20) + scale(gap_length_mean_partner_20) + scale(bin_num) + 
                       (1 + scale(gap_length_mean_speaker_20) + scale(gap_length_mean_partner_20) | subID) + 
                       (1 + scale(bin_num) | dyad), 
                     data=data_subset_no_nans)
summary(model_binned)

# contrast test
df <- data.frame(matrix(unlist(coef(model_binned)$subID), nrow=87, byrow=FALSE))
names(df)[names(df) == 'X1'] <- 'intercept'
names(df)[names(df) == 'X2'] <- 'betas_speaker'
names(df)[names(df) == 'X3'] <- 'betas_partner'
names(df)[names(df) == 'X4'] <- 'bin_num'
df$partner_minus_speaker <- df$betas_partner - df$betas_speaker

t.test(df$partner_minus_speaker)

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
