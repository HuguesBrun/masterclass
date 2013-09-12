from ROOT import gSystem
from ROOT import TChain
from ROOT import TFile
from ROOT import TH1F
from ROOT import TLorentzVector
import sys

# load library with MyClass dictionary
gSystem.Load( 'MyMuon_C' )
gSystem.Load( 'MyJet_C' )

# get MyClass from ROOT
from ROOT import MyMuon
from ROOT import MyJet

args = sys.argv[1:]
nameSample = str(args[0])

chain = TChain("data")


outFile = TFile("histos_"+nameSample+".root","RECREATE")

invMass = TH1F("invMass","",40,60,120)




def FillTheObjectCollections():
    for j in xrange(chain.NMuon):
        muon = MyMuon(chain.Muon_Px[j],chain.Muon_Py[j],chain.Muon_Py[j],chain.Muon_E[j])
        muon.SetIsolation(chain.Muon_Iso[j])
        muon.SetCharge(chain.Muon_Charge[j]);
        AllMuons.append(muon)



chain.Add(nameSample+".root")
nbEntries = chain.GetEntries()
for i in xrange(nbEntries):
    AllMuons = []
    chain.GetEntry(i)
    FillTheObjectCollections()

#######################################
    if (len(AllMuons)<2): continue
    sumMuon = AllMuons[0] + AllMuons[1]
    invMass.Fill(sumMuon.M())

#######################################
outFile.Write()
outFile.Close()




