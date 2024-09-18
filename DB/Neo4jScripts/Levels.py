import os

import pandas as pd

from PermedcoeN1 import agentsList, datasetsDir

# constants
LABEL = "label"


# load agents of level 1 and 2
Agents_PerMedCoE_str = "Agents_PerMedCoE"
agentsN1 = pd.read_csv(datasetsDir + Agents_PerMedCoE_str + ".csv", sep=",", low_memory=False)
agentsN2 = pd.read_csv(datasetsDir + Agents_PerMedCoE_str + "n2.csv", sep=",", low_memory=False)

# add N1 and O (original) levels
agentsN1_N1 = agentsN1[agentsN1[LABEL].isin(agentsList)]
agentsN1_O = agentsN1[~agentsN1[LABEL].isin(agentsList)]
agentsN1.loc[agentsN1[LABEL].isin(agentsN1_O[LABEL]), "level"] = "N1"
agentsN1.loc[agentsN1[LABEL].isin(agentsN1_N1[LABEL]), "level"] = "O"

agentsN1.to_csv(datasetsDir + Agents_PerMedCoE_str + "n1.csv", sep=",", index=False)

# add N2 levels
agents_list_N1 = list(agentsN1[LABEL])    # N1 i O

agentsN1_N1 = agentsN2[agentsN2[LABEL].isin(agents_list_N1)]
agentsN1_N2 = agentsN2[~agentsN2[LABEL].isin(agents_list_N1)]
agentsN1_N2["level"] = "N2"
agentsN1_N2_final = pd.concat([agentsN1, agentsN1_N2])

agentsN1_N2_final.to_csv(datasetsDir + Agents_PerMedCoE_str + "n2.csv", sep=",", index=False)

# load MetaCitations Reduction (all and level 1)
MetaCitationsReduction_str = "MetaCitationsReduction_PerMedCoE"
metAll = pd.read_csv(datasetsDir + MetaCitationsReduction_str + "n2.csv", sep=",", low_memory=False)
metN1 = pd.read_csv(datasetsDir + MetaCitationsReduction_str + ".csv", sep=",", low_memory=False)

# rename MetaCitations Reduction files (all and level 1)
fileO = datasetsDir + MetaCitationsReduction_str + ".csv"
fileN2 = datasetsDir + MetaCitationsReduction_str + "n2.csv"
if os.path.exists(fileO) and os.path.exists(fileN2):
    os.rename(fileN2, datasetsDir + MetaCitationsReduction_str + "all.csv")
    os.rename(fileO, datasetsDir + MetaCitationsReduction_str + "n1.csv")

# add MetaCitations Reduction of level 2
metN2 = pd.concat([metAll, metN1]).drop_duplicates(keep=False)
metN2.to_csv(datasetsDir + MetaCitationsReduction_str + "n2.csv", sep=",", index=False)
