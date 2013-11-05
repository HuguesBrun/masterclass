from ROOT import gSystem, gPad
from ROOT import TChain
from ROOT import TFile
from ROOT import TH1F
from ROOT import THStack
from ROOT import TCanvas
from ROOT import TLorentzVector
import sys

# load library with MyClass dictionary
gSystem.Load( 'MyMuon_C' )
gSystem.Load( 'MyElectron_C' )
gSystem.Load( 'MyPhoton_C' )
gSystem.Load( 'MyJet_C' )

# get MyClass from ROOT
from ROOT import MyMuon
from ROOT import MyElectron
from ROOT import MyPhoton
from ROOT import MyJet

def FillTheObjectCollections():
    for j in xrange(chain.NMuon):
        muon = MyMuon(chain.Muon_Px[j],chain.Muon_Py[j],chain.Muon_Pz[j],chain.Muon_E[j])
        muon.SetIsolation(chain.Muon_Iso[j])
        muon.SetCharge(chain.Muon_Charge[j]);
        AllMuons.append(muon)

#args = sys.argv[1:]
#nameSample = str(args[0])
AllSample = ["data","mc_ttbar","mc_wjets","mc_dy","mc_qcd"]
IntLumiWeight = [1.0, 0.5, 0.5, 0.5, 0.05]

countFile = 0
invMass = []
invMassSel = []
NMuons = []
NElectrons = []
NPhotons = []
NJets = []

outFile = TFile("histos_all.root","RECREATE")
hs = THStack('hs','invariant Mass')

for file in AllSample:
    nameSample = AllSample[countFile]
    print  " file ", nameSample

    chain = TChain("data")

#    invMass[countFile] = TH1F("invMass"+nameSample,"",40,60,140)
    invMass.append(TH1F('invMass_'+ nameSample, "invariant Mass", 40, 60, 140))
    invMassSel.append(TH1F('invMassSel_'+ nameSample,"invariant Mass",100,0,200))
    NMuons.append(TH1F('NMuons_'+ nameSample,'Muons nb',10,0,10))
    NElectrons.append(TH1F('NElectrons_'+ nameSample,'Electrons nb',10,0,10))
    NPhotons.append(TH1F('NPhotons_'+ nameSample,'Photons nb',10,0,10))
    NJets.append(TH1F('NJets_'+ nameSample,'Jets nb',10,0,10))

    chain.Add("files/"+nameSample+".root")
    nbEntries = chain.GetEntries()
#    nbEntries = 1000
    for i in xrange(nbEntries):
        AllMuons = []
        chain.GetEntry(i)
        FillTheObjectCollections()

#######################################
        NMuons[countFile].Fill(chain.NMuon)
        if(chain.NMuon > 1):
            opcharge = chain.Muon_Charge[0] * chain.Muon_Charge[1]
            if(opcharge == -1):
                if(chain.Muon_Iso[0] < 1):
                    if(chain.Muon_Iso[1] < 1):
                        sumMuon = AllMuons[0] + AllMuons[1]
                        weight = chain.EventWeight * chain.triggerIsoMu24 * IntLumiWeight[countFile]
                        invMassSel[countFile].Fill(sumMuon.M(), weight)

        NElectrons[countFile].Fill(chain.NElectron)
        NPhotons[countFile].Fill(chain.NPhoton)
        NJets[countFile].Fill(chain.NJet)

        if (len(AllMuons)<2): continue
        sumMuon = AllMuons[0] + AllMuons[1]
        invMass[countFile].Fill(sumMuon.M())

#######################################
    if(countFile > 0):
        invMassSel[countFile].SetFillColor(countFile)
        hs.Add(invMassSel[countFile])
    countFile = countFile + 1

print ' creating canavas'
c = TCanvas("c", "c", 800, 1000)
c.Divide(1,2)
c.cd(1)
hs.Draw('hist')
invMassSel[0].Draw('pesame')
invMassSel[0].SetMarkerStyle(20)
invMassSel[0].SetMarkerSize(0.5)
c.cd(2)
gPad.SetLogy(1)
hs.Draw('hist')
invMassSel[0].Draw('pesame')
c.Print("InvMass.gif")

outFile.Write()
outFile.Close()




