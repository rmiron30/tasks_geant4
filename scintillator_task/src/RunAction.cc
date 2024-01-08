//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
/// \file electromagnetic/TestEm4/src/RunAction.cc
/// \brief Implementation of the RunAction class
//
//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#include "RunAction.hh"

#include "G4Run.hh"
#include "G4RunManager.hh"

#include "G4SystemOfUnits.hh"
#include "Randomize.hh"

#include "G4AnalysisManager.hh"

#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <ctime>
// namespace fs = std::filesystem;
using namespace std;

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

RunAction::RunAction()
    : G4UserRunAction()
{
  G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();
  analysisManager->SetDefaultFileType("root");
  analysisManager->SetVerboseLevel(2);
  analysisManager->SetFirstHistoId(1);
  //analysisManager->SetSecondHistoId(2);

  // Creating histograms
  //
  analysisManager->CreateH1("Hist1D", "deposited energy (MeV)", 100000, 0., 11.);
  analysisManager->CreateH2("eDep2D", "Energy Deposition", 2000, -1 * mm, 1 * mm, 2000, -1 * mm, 1 * mm);
  analysisManager->CreateH1("enerBeam", "energy of the beam", 1000, 0., 11.);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

RunAction::~RunAction()
{
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void RunAction::BeginOfRunAction(const G4Run *)
{
  // show Rndm status
  if (isMaster)
    G4Random::showEngineStatus();

  // Get analysis manager
  G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();

  // Open an output file
  //
  G4String fileName = "testem4";
  analysisManager->OpenFile(fileName);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void RunAction::EndOfRunAction(const G4Run *)
{
  // show Rndm status

  G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();
  char timeDir [80];

  if (isMaster){
    G4Random::showEngineStatus();

    // the current time

    std::time_t t = std::time(nullptr);
    
    std::strftime(timeDir, 80, "%Y-%m-%d-%H-%M-%S", std::localtime(&t));

    // save histograms
  
    std::filesystem::create_directory(timeDir);
    

  }

  
  // std::ifstream file("testem4.root", std::ios::binary);
  // std::ofstream newFile(timeDir + std::string("/testem4.root"), std::ios::binary);
  // newFile << file.rdbuf();

  analysisManager->Write();
  analysisManager->CloseFile();

  if (isMaster){
    G4Random::showEngineStatus();
    //  const auto copyOptions = std::filesystem::copy_options::update_existing | std::filesystem::copy_options::recursive | std::filesystem::copy_options::directories_only;
    const auto copyOptions = std::filesystem::copy_options::overwrite_existing | std::filesystem::copy_options::recursive; 
    std::filesystem::copy("testem4.root", timeDir + std::string("/testem4.root"), copyOptions);
    std::filesystem::copy("../config.json", timeDir + std::string("/config.json"), copyOptions);

  }


}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
