import yaml

config  ={}
config['year'] = 2016
config['tree_name'] = 'Vars'
config['lumi_text'] = '$35.7 fb^{-1}$' 
config['path'] = '/user/hanwen/trigger/hzz2l2nu2016/OUTPUTS/DileptonTrees/output' 
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
                       '(PFMET110_PFMHT110_IDTight && ptmiss > 1.1 * 110)',
                       '(PFMET120_PFMHT120_IDTight && ptmiss > 1.1 * 120)',
                       '(PFMET170_HBHECleaned && ptmiss > 1.1 * 170)',
                       '(PFHT300_PFMET100 && ptmiss > 1.1 * 100)',
                       '(PFMET300 && ptmiss > 1.1 * 300)',
                       '(PFMET400 && ptmiss > 1.1 * 400)',
                       '(PFMET600 && ptmiss > 1.1 * 600)',
                       'PFHT650_4JetPt50',
                       'PFHT750_4JetPt50',
                       '(MET300 && ptmiss > 1.1 * 300)',
                       '(PFMET100_PFMHT100_IDTight && ptmiss > 1.1 * 100)',
]
config['channels'] = {
    'ee':{
          'baseline':'lepton_cat == 0 && ll_mass > 76.',
          'testflag':[
                      'Ele25_eta2p1_WPTight_Gsf',
                      'Ele27_WPTight_Gsf',
                      '(Ele27_eta2p1_WPLoose_Gsf && ( run > 280919 || isMC))',
                      'Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
                      '(DoubleEle33_CaloIdL_GsfTrkIdVL && (run > 278873 || isMC))',
                      '(DoubleEle33_CaloIdL_MW && ( run < 278822 || isMC))',
                      'DoublePhoton60',
                      'Photon175',
                      ]
         },
    'mumu':{
            'baseline':'lepton_cat == 1 && ll_mass > 76.',
            'testflag':[
                        'IsoMu24',
                        'IsoTkMu24',
                        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',
                        '(Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL && (run > 280919 || isMC))',
                        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
                        'Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ',
                        '(TkMu50 && ( run <274442 || isMC))',
                        'Mu50',
                       ]
           },
    'emu':{
           'baseline':'lepton_cat == 2 && ll_mass > 76.',
           'testflag':[
                  'Ele25_eta2p1_WPTight_Gsf',
                  'Ele27_WPTight_Gsf',
                  'Ele27_eta2p1_WPLoose_Gsf',
                  'IsoMu24',
                  'IsoTkMu24',
                  '(TkMu50 && (run < 274442 || isMC))',
                  'Mu50',
                  '(Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL && ( run > 280919 || isMC))',
                  '(Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL && ( run > 280919 || isMC))',
                  '(Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ && (run < 278240 || isMC))',
                  '(Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ && (run < 278240 || isMC))',
                 ],
          }        
}                  
print(yaml.dump(config,sort_keys=False))
with open(str(config['year'])+'.yaml', 'w') as f:
  yaml.dump(config, f,sort_keys=False)
