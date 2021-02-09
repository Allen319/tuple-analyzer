#!/usr/bin/env python3
import sys, getopt
import re
import os
import yaml

def prepare_job_script():
		plotDirectory = jobsDirectory +"/plots"
		if not os.path.exists(plotDirectory):
			os.makedirs(plotDirectory)
		scriptsDirectory = outputDirectory +"/jobs"
		if not os.path.exists(scriptsDirectory):
			os.makedirs(scriptsDirectory)
		os.system("cp "+baseDir+"/env.sh " +scriptsDirectory) 
		os.system("cp "+baseDir+"/bin/* " +scriptsDirectory) 
		os.system("cp "+baseDir+"/config/* " +scriptsDirectory) 
		for fileName in samples:
			scriptFile = open(scriptsDirectory+'/'+'mkhis_'+year+fileName+"_"+'.sh','w')
			scriptLines = ''
			#scriptLines += 'export VO_CMS_SW_DIR=/nfs/soft/cms\n'
			#scriptLines += 'export SCRAM_ARCH=slc6_amd64_gcc530\n'
			#scriptLines += 'export BUILD_ARCH=slc6_amd64_gcc530\n'
			scriptLines += ('export INITDIR='+scriptsDirectory+'\n')
			scriptLines += ('cd $INITDIR\n')
			scriptLines += ('. ./env.sh\n')
			#scriptLines += 'eval `scramv1 runtime -sh`\n'
			scriptLines += 'hostname ;\n'
			scriptLines += ("date;\n")
			if "Data" in fileName:

				scriptLines += ("./tuple --rebin --input="+path+"/"+fileName+" --config="+aFile +" --output=" +plotDirectory+"/"+fileName+";\n")
			else:
				scriptLines += ("./tuple --rebin --isMC --input="+path+"/"+fileName+" --config="+aFile +" --output=" +plotDirectory+"/"+fileName+";\n")

			#scriptLines += ("./fit.py -i "+subDirectory+fileName+".root" +" -s "+fileName+" -y "+baseDir+"/config/"+aFile+" -f "+aModel+" -o "+subDirectory+fileName+"_eff.root;\n")
			scriptFile.write(scriptLines)
			scriptFile.close()
			jobsFiles = open(scriptsDirectory+"/sendJobs.cmd","a")
			jobsFiles.write("qsub  "+scriptsDirectory+'/'+'mkhis_'+year+fileName+"_"+'.sh\n')
			jobsFiles.close()

def main():
    global jobsDirectory
    global outputDirectory
    global baseDir
    baseDir = os.getenv('CMAKE_BINARY_DIR')
    outputDirectory = baseDir+"/outputs_"+suffix_name+"/"
    jobsDirectory = baseDir+"/outputs_"+suffix_name+"/"+year
    if not os.path.exists(jobsDirectory):
      os.makedirs(jobsDirectory)
    prepare_job_script()
	

if __name__ == '__main__':
	suffix_name = sys.argv[1]
	for aFile in ["2016.yaml", "2017.yaml", "2018.yaml"]:
		f = open(os.getenv('CMAKE_BINARY_DIR')+'/config/'+aFile)
		config = yaml.load(f)
		print(config)
		yaml.dump(config)
		year =  str(config['year'])
		path = str(config['path'])
		samples = os.listdir(path)
		main()

