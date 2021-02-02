#include <iostream>
#include <filesystem>
#include <map>
#include <memory>
#include <string>
#include <vector>

#include <yaml-cpp/yaml.h>
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/join.hpp>
#include <boost/program_options.hpp>
#include <TCanvas.h>
#include <TFile.h>
#include <TEfficiency.h>
#include <TH1.h>
#include <TH2.h>


#include <FileInPath.h>
#include <Options.h>

using namespace ROOT;

namespace po = boost::program_options;
int main(int argc, char **argv){

  Options options(argc, argv);

  YAML::Node const config = options.GetConfig();
  std::string filename;
  if  (options.Exists("input")) filename = options.GetAs<std::string>("input");
  else filename = Options::NodeAs<std::string>(config, {"file_name"});
  std::cout<<filename;
  std::string pathAndName = FileInPath::Resolve(filename);//pathToFile + std::string("/") + filename ;//boost::algorithm::join(pathToFile, filename, "/");
  
  TFile *inputFile = new TFile(pathAndName.c_str());
  TFile *outputFile = new TFile(options.GetAs<std::string>("output").c_str(),"recreate");
  std::vector<std::string> channels = {"ee","mumu","emu"};
  std::vector<std::string> obs = Options::GetStrings(config, {"observable"});
  std::map<std::string, std::string> obs2D = Options::NodeAs<std::map<std::string, std::string>>(config, {"observable2D"});
  
  for(auto ch = channels.begin(); ch != channels.end() ;ch++){
  
  //Filling 1D histogram and Efficiency  
    for(auto ob = obs.begin(); ob != obs.end(); ob++){
      std::string ob_key = *ob;
      if  (options.Exists("rebin") && boost::contains(*ob, "eta")) ob_key = ob_key+"_"+*ch;
      std::vector<double> bin_vec = Options::GetBinning(config, {"binning",ob_key});
      Double_t binning [bin_vec.size()];
      memcpy(binning, &bin_vec[0], bin_vec.size() * sizeof(bin_vec[0]));
      TH1D* h_nominal = new TH1D("","", bin_vec.size()-1, binning);
      TH1D* h_upper = new TH1D("","", bin_vec.size()-1, binning);
      TH1D* h_lower = new TH1D("","", bin_vec.size()-1, binning);
      TH1D* h_pass = (TH1D*) inputFile->Get(TString(*ob+"_"+*ch+"_pass"));
      TH1D* h_all = (TH1D*) inputFile->Get(TString(*ob+"_"+*ch+"_all"));
      for( int i = 0 ; i < h_nominal->GetNbinsX() + 1; i++){
        double pass = h_pass->GetBinContent(i);
        double all  = h_all ->GetBinContent(i);
        h_nominal->SetBinContent(i, pass/all);
        h_upper  ->SetBinContent(i,TEfficiency::ClopperPearson(all, pass, 0.95, true ));
        h_lower  ->SetBinContent(i,TEfficiency::ClopperPearson(all, pass, 0.95, false ));
      }

      h_nominal->SetName(TString(*ob+"_"+*ch)+"_nominal");
      h_upper->SetName(TString(*ob+"_"+*ch)+"_upper");
      h_lower->SetName(TString(*ob+"_"+*ch)+"_lower");
      h_nominal->Write();
      h_upper->Write();
      h_lower->Write();
      delete h_nominal;
      delete h_upper;
      delete h_lower;
    }
  
  //Filling 2D histogram and Efficiency
    for (auto ob = obs2D.begin(); ob!= obs2D.end();ob++){
      std::string ob_key1 = (*ob).first;
      std::string ob_key2 = (*ob).second;
      if  (options.Exists("rebin") && boost::contains((*ob).first, "eta"))
        ob_key1 = ob_key1+"_"+*ch;
      if  (options.Exists("rebin") && boost::contains((*ob).second, "eta"))
        ob_key2 = ob_key2+"_"+*ch;
      std::vector<double> bin1_vec = Options::GetBinning(config, {"binning",ob_key1});
      std::vector<double> bin2_vec = Options::GetBinning(config, {"binning",ob_key2});
      Double_t binning1 [bin1_vec.size()];
      Double_t binning2 [bin2_vec.size()];
      memcpy(binning1, &bin1_vec[0], bin1_vec.size() * sizeof(bin1_vec[0]));
      memcpy(binning2, &bin2_vec[0], bin2_vec.size() * sizeof(bin2_vec[0]));
      
      TH2D* h_nominal = new TH2D("","",bin1_vec.size()-1, binning1, bin2_vec.size()-1, binning2);
      TH2D* h_upper = new TH2D("","",bin1_vec.size()-1, binning1, bin2_vec.size()-1, binning2);
      TH2D* h_lower = new TH2D("","",bin1_vec.size()-1, binning1, bin2_vec.size()-1, binning2);
      TH2D* h_pass = (TH2D*) inputFile->Get(TString((*ob).first+"_"+(*ob).second+"_"+*ch+"_pass"));
      TH2D* h_all = (TH2D*) inputFile->Get(TString((*ob).first+"_"+(*ob).second+"_"+*ch+"_all"));
      for( int x = 0 ; x < h_nominal->GetNbinsX()  + 1 ; x++){
        for( int y = 0 ; y <  h_nominal->GetNbinsY() + 1 ;y++){
          double pass = h_pass->GetBinContent(x, y);
          double all  = h_all ->GetBinContent(x, y);
          h_nominal->SetBinContent(x, y, pass/all);
          h_upper  ->SetBinContent(x, y, TEfficiency::ClopperPearson(all, pass, 0.95, true ));
          h_lower  ->SetBinContent(x, y, TEfficiency::ClopperPearson(all, pass, 0.95, false ));
        }

      }
      
      h_nominal->SetName(TString((*ob).first+"_"+(*ob).second+"_"+*ch)+"_nominal");
      h_upper->SetName(TString((*ob).first+"_"+(*ob).second+"_"+*ch)+"_upper");
      h_lower->SetName(TString((*ob).first+"_"+(*ob).second+"_"+*ch)+"_lower");
      h_nominal->Write();
      h_upper->Write();
      h_lower->Write();
      delete h_nominal;
      delete h_upper;
      delete h_lower;
    }
  }
  
  
  
  outputFile->Close();
  delete outputFile;
  return 0;
}
