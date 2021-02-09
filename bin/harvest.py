#!/usr/bin/env python3
import sys, getopt
import re
import os
import yaml

def harvest():
		plotDirectory = jobsDirectory +"/plots"
		os.system('cp ~/public_html/index.php '+plotDirectory)
		print('plotter --config='+year+'.yaml --input='+plotDirectory+'/Data.root --output='+plotDirectory+'/Data_eff.root')
		os.system('plotter --config='+year+'.yaml --input='+plotDirectory+'/Data.root --output='+plotDirectory+'/Data_eff.root')
		print('plotter --config='+year+'.yaml --input='+plotDirectory+'/MC.root --output='+plotDirectory+'/MC_eff.root')
		os.system('plotter --config='+year+'.yaml --input='+plotDirectory+'/MC.root --output='+plotDirectory+'/MC_eff.root')
def main():
    global jobsDirectory
    global outputDirectory
    global baseDir
    baseDir = os.getenv('CMAKE_BINARY_DIR')
    jobsDirectory = baseDir+"/outputs_"+suffix_name+"/"+year
    if not os.path.exists(jobsDirectory):
      os.makedirs(jobsDirectory)
    harvest()
	

if __name__ == '__main__':
	suffix_name = sys.argv[1]
	for aFile in ["2016.yaml","2017.yaml","2018.yaml"]:
		f = open(os.getenv('CMAKE_BINARY_DIR')+'/config/'+aFile)
		config = yaml.load(f)
		year =  str(config['year'])
		main()

