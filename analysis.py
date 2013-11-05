from ROOT import gSystem, gPad, gROOT
from ROOT import TChain
from ROOT import TFile
from ROOT import TH1F
from ROOT import THStack
from ROOT import TCanvas
from ROOT import TLorentzVector
import sys
gROOT.SetBatch()

from math import ceil

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
        muon.SetCharge(chain.Muon_Charge[j])
        AllMuons.append(muon)
    for j in xrange(chain.NElectron):
        electron = MyElectron(chain.Electron_Px[j],chain.Electron_Py[j],chain.Electron_Pz[j],chain.Electron_E[j])
        electron.SetIsolation(chain.Electron_Iso[j])
        electron.SetCharge(chain.Electron_Charge[j])
        AllElectrons.append(electron)
    for j in xrange(chain.NPhoton):
        photon = MyPhoton(chain.Photon_Px[j],chain.Photon_Py[j],chain.Photon_Pz[j],chain.Photon_E[j])
        photon.SetIsolation(chain.Photon_Iso[j])
        AllPhotons.append(photon)
    for j in xrange(chain.NJet):
        jet = MyJet(chain.Jet_Px[j],chain.Jet_Py[j],chain.Jet_Pz[j],chain.Jet_E[j])
        jet.SetBTagDiscriminator(chain.Jet_btag[j])
        AllJets.append(jet)
    hadB = TLorentzVector(); hadB.SetXYZM(chain.MChadronicBottom_px, chain.MChadronicBottom_py, chain.MChadronicBottom_pz, 4.8);
    lepB = TLorentzVector(); lepB.SetXYZM(chain.MCleptonicBottom_px, chain.MCleptonicBottom_py, chain.MCleptonicBottom_pz, 4.8);
    hadWq = TLorentzVector(); hadWq.SetXYZM(chain.MChadronicWDecayQuark_px, chain.MChadronicWDecayQuark_py, chain.MChadronicWDecayQuark_pz, 0.0);
    hadWqb = TLorentzVector(); hadWqb.SetXYZM(chain.MChadronicWDecayQuarkBar_px, chain.MChadronicWDecayQuarkBar_py, chain.MChadronicWDecayQuarkBar_pz, 0.0);
    lepWl = TLorentzVector(); lepWl.SetXYZM(chain.MClepton_px, chain.MClepton_py, chain.MClepton_pz, 0.0);
    lepWn= TLorentzVector(); lepWn.SetXYZM(chain.MCneutrino_px, chain.MCneutrino_py, chain.MCneutrino_pz, 0.0);
    met = TLorentzVector(); met.SetXYZM(chain.MET_px, chain.MET_py, 0., 0.)

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
        if(i % (nbEntries/10) == 0): print "\tProcessing entry {0} / {1} ({2}% done)".format(i, nbEntries, ceil(float(i)/float(nbEntries)*100.))
        AllMuons = []
        AllElectrons = []
        AllPhotons = []
        AllJets = []
        chain.GetEntry(i)
        FillTheObjectCollections()

#######################################
        NMuons[countFile].Fill(chain.NMuon)

        if(not chain.triggerIsoMu24): continue
        if(chain.NMuon < 2): continue
        opcharge = AllMuons[0].GetCharge() * AllMuons[1].GetCharge()
        if(opcharge != -1): continue
        if(AllMuons[0].Pt() < 24.): continue
        if(not (AllMuons[0].IsIsolated() and AllMuons[1].IsIsolated())): continue
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

print ' creating canevas'
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



