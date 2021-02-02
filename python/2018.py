import yaml

config  ={}
config['year'] = 2018
config['tree_name'] = 'Vars'
config['lumi_text'] = '$59.7 fb^{-1}$' 
config['path'] = '/user/hanwen/trigger/hzz2l2nu2018/OUTPUTS/DileptonTrees/output' 
config['observable'] = ['ll_deltaR','run','jet_cat','ptmiss','ll_pt','leading_pt','trailing_pt','nJet','nJetBuilder','PV_npvs','PV_npvsGood']
config['observable2D'] = {'leading_abseta':'trailing_abseta','ll_pt':'ll_deltaR',}
config['binning'] = {#'ll_mass':[25, 75, 105, 200],
                     #'run':[272006 + i for i in range(284045 - 272006)],
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
config['pre-selections'] ={ 
'(PFHT500_PFMET100_PFMHT100_IDTight && ptmiss > 1.1 * 100)',
'(PFHT500_PFMET110_PFMHT110_IDTight && ptmiss > 1.1 * 110)',
'(PFHT700_PFMET95_PFMHT95_IDTight && ptmiss > 1.1 * 95)',
'(PFHT800_PFMET85_PFMHT85_IDTight && ptmiss > 1.1 * 85)',
'(PFMET120_PFMHT120_IDTight && ptmiss > 1.1 *120)',
'(PFMET130_PFMHT130_IDTight && ptmiss > 1.1 *130)',
'(PFMET140_PFMHT140_IDTight && ptmiss > 1.1 *140)',
'(PFMET120_PFMHT120_IDTight_PFHT60 && ptmiss > 1.1 *120)',
'(PFMET200_HBHECleaned && ptmiss > 1.1 *200)',
'(PFMET250_HBHECleaned && ptmiss > 1.1 *250)',
'(PFMET300_HBHECleaned && ptmiss > 1.1 *300)',
'(CaloMET250_HBHECleaned && ptmiss > 1.1 *250)',
'(CaloMET300_HBHECleaned && ptmiss > 1.1 *300)',
'(CaloMET350_HBHECleaned && ptmiss > 1.1 *350)',
'PFHT330PT30_QuadPFJet_75_60_45_40',
'PFHT450_SixPFJet36',
}
config['channels'] = {
    'ee':{
          'baseline':'lepton_cat == 0 && ll_mass > 76.',
          'testflag':['Ele23_Ele12_CaloIdL_TrackIdL_IsoVL', 
                      'DoubleEle33_CaloIdL_MW', 
                      'DoublePhoton70', 
                      'Ele32_WPTight_Gsf',
                      'Photon200',]
         },
    'mumu':{
            'baseline':'lepton_cat == 1 && ll_mass > 76.',
            'testflag':[
                        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8',
                        'IsoMu24',
                        'Mu50',
                        'TkMu100',
                        'OldMu100',
                       ]
           },
    'emu':{
           'baseline':'lepton_cat == 2 && ll_mass > 76.',
           'testflag':[
                      'IsoMu24',
                      'Mu50', 
                      'TkMu100',
                      'OldMu100',
                      'Ele32_WPTight_Gsf',
                      'Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
                      'Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ',
                      ]
          }
}
print(yaml.dump(config,sort_keys=False))
with open(str(config['year'])+'.yaml', 'w') as f:
  yaml.dump(config, f,sort_keys=False)
