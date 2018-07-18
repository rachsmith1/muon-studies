
# coding: utf-8

# In[1]:

from muon_h import *
from muon_plot import *


# In[2]:

filepath = '/gpfs/slac/atlas/fs1/d/rafaeltl/public/RNNIP/FTAG_ntups/user.rateixei.mc16_13TeV.410470.PhPy8EG_A14_ttbar_hdamp258p75_nonallhad.AOD..dijetSamplesNominal20180629_Akt4EMTo/user.rateixei.14594351.Akt4EMTo._002365.root'


# In[3]:

data = root2array(filepath)


# ## 20 GeV <= Jet pT < 50 GeV and 0 <= Jet |eta| < 1

# In[ ]:

makeMuonPlots(data,"20_50","0_1")


# ## 20 GeV <= Jet pT < 50 GeV and 1 <= Jet |eta| < 2.5

# In[ ]:

makeMuonPlots(data,"20_50","1_2.5")


# ## 50 GeV <= Jet pT < 100 GeV and 0 <= Jet |eta| < 1

# In[ ]:

makeMuonPlots(data,"50_100","0_1")


# ## 50 GeV <= Jet pT < 100 GeV and 1 <= Jet |eta| < 2.5

# In[ ]:

makeMuonPlots(data,"50_100","1_2.5")


# ## 100 GeV <= Jet pT < 200 GeV and 0 <= Jet |eta| < 1

# In[ ]:

makeMuonPlots(data,"100_200","0_1")


# ## 100 GeV <= Jet pT < 200 GeV and 1 <= Jet |eta| < 2.5

# In[ ]:

makeMuonPlots(data,"100_200","1_2.5")


# ## 200 GeV <= Jet pT < 500 GeV and 0 <= Jet |eta| < 1

# In[ ]:

makeMuonPlots(data,"200_500","0_1")


# ## 200 GeV <= Jet pT < 500 GeV and 1 <= Jet|eta| < 2.5

# In[ ]:

makeMuonPlots(data,"200_500","1_2.5")

