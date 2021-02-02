#include <iostream>
#include <array>
#include <map>
#include <memory>
#include <string>
#include <tuple>
#include <vector>

#include <ROOT/RDataFrame.hxx>
#include <yaml-cpp/yaml.h>
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/join.hpp>
#include <boost/program_options.hpp>
#include <TCanvas.h>
#include <TEfficiency.h>

#include <FileInPath.h>
#include <Options.h>

using namespace ROOT;

namespace po = boost::program_options;
int main(int argc, char **argv){

  Options options(argc, argv);
  YAML::Node const config = options.GetConfig();
  std::string tree = Options::NodeAs<std::string>(config, {"tree_name"});
  std::string filename;
  if  (options.Exists("input")) filename = options.GetAs<std::string>("input");
  else filename = Options::NodeAs<std::string>(config, {"file_name"});
  std::string pathAndName = FileInPath::Resolve(filename);//pathToFile + std::string("/") + filename ;//boost::algorithm::join(pathToFile, filename, "/");
  
  std::string outputName = "output.root";
  if  (options.Exists("output")) outputName = options.GetAs<std::string>("output");
  TFile *inputFile = new TFile(TString(pathAndName));
  TTree *ttr = (TTree *)inputFile->Get("Vars");
  auto *list = ttr->GetListOfBranches();
  TBranch *branch = (TBranch*)list->Last();
  std::vector<TString> listOfBranches;

  for (auto it = list->begin(); it!= list->end() ;it.Next()) listOfBranches.push_back(((TBranch*)it())->GetName());
  inputFile->Close();
  delete inputFile;
  TFile *outputFile = new TFile(options.GetAs<std::string>("output").c_str(),"recreate");
  EnableImplicitMT();
  RDataFrame d(tree,pathAndName);
  std::vector<std::string> met_triggers = Options::GetStrings(config, {"MET-selections"});
  for (auto it = met_triggers.begin(); it != met_triggers.end(); ){
    unsigned int brNumber = 0;
    for (auto br = listOfBranches.begin();br != listOfBranches.end();br++){
      if (boost::contains(*it, (*br).View())) brNumber++;
      if (boost::contains(*it, "ptmiss")) brNumber--;
    } 
    if(brNumber ==0) met_triggers.erase(it);
    else ++it;
  }
  std::vector<std::string> channels = {"ee","mumu","emu"};
  std::vector<std::string> obs = Options::GetStrings(config, {"observable"});
  std::map<std::string, std::string> obs2D = Options::NodeAs<std::map<std::string, std::string>>(config, {"observable2D"});
  
  auto d_inter = options.Exists("isMC") ? d.Define("weights","weight") : d.Define("weights","1") ; 
  for(auto ch = channels.begin(); ch != channels.end() ;ch++){
  
    std::vector<std::string> ch_triggers = Options::GetStrings(config, {"channels",*ch,"testflag"});
    
    std::string ee_base = Options::NodeAs<std::string>(config, {"channels",*ch,"baseline"});
    auto d_new     = d_inter.Filter("("+boost::join(met_triggers, " || ")+") && "+ee_base+ "&& ("+boost::join(ch_triggers, " || ")+")");
    auto d_new_all = d_inter.Filter("("+boost::join(met_triggers, " || ")+") && "+ee_base);
  
  //Filling 1D histogram and Efficiency  
    for(auto ob = obs.begin(); ob != obs.end(); ob++){
      std::string ob_key = *ob;
      if  (options.Exists("rebin") && boost::contains(*ob, "eta")) ob_key = ob_key+"_"+*ch;
      std::vector<double> bin_vec = Options::GetBinning(config, {"binning",ob_key});
      Double_t binning [bin_vec.size()];
      memcpy(binning, &bin_vec[0], bin_vec.size() * sizeof(bin_vec[0]));
      
      auto hist_model = ROOT::RDF::TH1DModel("","",bin_vec.size()-1, binning);
      auto proxy = d_new.Histo1D(hist_model, *ob, "weights");
      auto proxy_all =d_new_all.Histo1D(hist_model, *ob, "weights");
      auto hist =     (TH1D *)proxy.GetValue().Clone();
      hist->SetName(TString(*ob+"_"+*ch)+"_pass");
      auto hist_all = (TH1D *)proxy_all.GetValue().Clone();
      hist_all->SetName(TString(*ob+"_"+*ch)+"_all");
      if (options.Exists("isMC")){
        double sf = hist->GetEffectiveEntries() / hist->Integral();
        double sf_all = hist_all->GetEffectiveEntries() / hist_all->Integral();
        hist->Scale(sf);
        hist_all->Scale(sf_all);
      }
      hist->Write();
      hist_all->Write();
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
      
      auto hist_model = ROOT::RDF::TH2DModel("","",bin1_vec.size()-1, binning1, bin2_vec.size()-1, binning2);
      auto proxy = d_new.Histo2D(hist_model, (*ob).first,(*ob).second, "weights");
      auto proxy_all =d_new_all.Histo2D(hist_model, (*ob).first,(*ob).second, "weights");
      auto hist =     (TH2D *)proxy.GetValue().Clone();
      hist->SetName(TString((*ob).first+"_"+(*ob).second+"_"+*ch)+"_pass");
      auto hist_all = (TH2D *)proxy_all.GetValue().Clone();
      hist_all->SetName(TString((*ob).first+"_"+(*ob).second+"_"+*ch)+"_all");
      if (options.Exists("isMC")){
        double sf = hist->GetEffectiveEntries() / hist->Integral();
        double sf_all = hist_all->GetEffectiveEntries() / hist_all->Integral();
        hist->Scale(sf);
        hist_all->Scale(sf_all);
      }
      hist->Write();
      hist_all->Write();
    }
  }
  
  
  
  outputFile->Close();
  delete outputFile;
  return 0;
}
