import yaml

config  ={}
config['year'] = 2017
config['tree_name'] = 'Vars'
config['file_name'] = '2017/data.root'
config['observable'] = ['leading_pt']#['ll_deltaR','jet_cat','ptmiss','ll_pt','leading_pt','trailing_pt','leading_abseta','trailing_abseta','nJet','nJetBuilder','PV_npvs','PV_npvsGood']
config['observable2D'] = {'leading_abseta':'trailing_abseta'}#,'ll_pt':'ll_deltaR',}
config['binning'] = {'ll_mass':[25, 75, 105, 200],
	             'run':[297046, 299329,302030, 303434, 305040, 306462 ],
	             'll_deltaR':[i * 0.2 for i in range(20)],
                     'jet_cat':[0,1,2,3],
                     'ptmiss':[0,20,30,50,80,120,150,200,300],
		     'll_pt':[0,25,55,70,90,110,130,150,200,300],
                     'trailing_pt':[25, 50, 75, 100, 150, 200],                  
                     'leading_pt':[25, 50, 75, 100, 150, 200],
                     'nJet':[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                     'nJetBuilder':[0,1,2,3,4,5,6,7,8,9,10,15],
                     'PV_npvs':[0,1000],
		     'PV_npvsGood':[0,10,12,14,16,18,20,22,24,26,28,30,40], 
                     'leading_abseta':[0.0,1.2,2.4],
		     'trailing_abseta':[0.0,1.2,2.4],
                     'leading_abseta_ee':[0.0,1.5,2.4],
		     'trailing_abseta_ee':[0.0,1.5,2.4],
                     'leading_abseta_mumu':[0.0,1.2,2.4],
		     'trailing_abseta_mumu':[0.0,1.2,2.4],
                     'leading_abseta_emu':[0.0,1.5,2.4],
		     'trailing_abseta_emu':[0.0,1.2,2.4],
                    }
config['MET-selections'] = [	
    '(PFHT500_PFMET100_PFMHT100_IDTight && ptmiss > 110. *1.1)',
    '(PFHT500_PFMET110_PFMHT110_IDTight && ptmiss > 110. *1.1)', 
    '(PFHT700_PFMET95_PFMHT95_IDTight && ptmiss > 95 * 1.1)', 
    '(PFHT800_PFMET85_PFMHT85_IDTight && ptmiss > 85 * 1.1)', 
    '(PFMET120_PFMHT120_IDTight && ptmiss > 120 *1.1)', 
    '(PFMET130_PFMHT130_IDTight && ptmiss > 130 *1.1)', 
    '(PFMET140_PFMHT140_IDTight && ptmiss > 1.1 * 140)', 
    '(PFMET120_PFMHT120_IDTight_PFHT60 && ptmiss > 1.1 * 120)', 
    '(TripleJet110_35_35_Mjj650_PFMET130 && ptmiss > 1.1 * 130)', 
    '(CaloMET250_HBHECleaned && ptmiss > 1.1 *250)', 
    '(CaloMET300_HBHECleaned && ptmiss > 1.1 * 300)', 
    '(CaloMET350_HBHECleaned && ptmiss > 1.1 * 350)', 
    '(PFMET200_HBHECleaned && ptmiss > 1.1 * 200)', 
    '(PFMET250_HBHECleaned && ptmiss > 1.1 * 250)', 
    '(PFMET300_HBHECleaned && ptmiss > 1.1 * 300)', 
    '(DiJet110_35_Mjj650_PFMET130 && ptmiss > 1.1 * 130)', 
]
config['channels'] = {
    'ee':{
          'baseline':'lepton_cat == 0 && ll_mass > 76.',
          'testflag':['Ele23_Ele12_CaloIdL_TrackIdL_IsoVL', 
                      'DoubleEle33_CaloIdL_MW', 
                      'DoublePhoton70', 
                      'Ele35_WPTight_Gsf', 
                      'Photon200',]
         },
    'mumu':{
            'baseline':'lepton_cat == 1 && ll_mass > 76.',
            'testflag':['Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8',
                     'IsoMu27', 
                     'Mu50', 
                     '(TkMu100 && ( run > 299368 || isMC ))',
                     '(OldMu100 && ( run > 299368 || isMC))']
           },
    'emu':{
           'baseline':'lepton_cat == 2 && ll_mass > 76.',
           'testflag':[
                      'IsoMu27', 
                      'Mu50', 
                      '(TkMu100 && ( run > 299368 || isMC ))',
                      '(OldMu100 && ( run > 299368 || isMC ))',
                      'Ele35_WPTight_Gsf', 
                      'Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
                      'Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ',]
          }
}
print(yaml.dump(config,sort_keys=False))
with open(str(config['year'])+'.yaml', 'w') as f:
	yaml.dump(config, f,sort_keys=False)