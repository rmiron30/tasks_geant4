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
/// \file electromagnetic/TestEm4/TestEm4.cc
/// \brief Main program of the electromagnetic/TestEm4 example
//
//
//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#include "G4Types.hh"

#include "G4RunManagerFactory.hh"
#include "G4UImanager.hh"
#include "G4SteppingVerbose.hh"
#include "Randomize.hh"

#include "DetectorConstruction.hh"
#include "PhysicsList.hh"
#include "ActionInitialization.hh"

#include "G4UIExecutive.hh"
#include "G4VisExecutive.hh"

#include "json/json.hpp"

#include <filesystem>

using namespace std;
using json = nlohmann::json;

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

json readfile(string name)
{
  ifstream file(name);
  json j;
  file >> j;

  return j;
}

int main(int argc, char **argv)
{

  // detect interactive mode (if no arguments) and define UI session
  G4UIExecutive *ui = nullptr;
  if (argc == 1)
    ui = new G4UIExecutive(argc, argv);

  const auto path = std::filesystem::path(std::filesystem::current_path());
  // read json file
  //auto configFile = readfile("/home/raluca/geant4/tasks_geant4/scintillator_task/config.json");
  // auto configFile = readfile("/home/rmiron/geant4/tasks_geant4/scintillator_task/config.json");
  // auto configFile = readfile("/home/diagpc/Miron/Geant4/tasks_geant4/scintillator_task/config.json");
  // auto configFile = readfile("/home/raluca/tasks_geant4/scintillator_task/config.json");
  auto configFile = readfile(path.string() + "/../config.json");

  cout << configFile["thickness"] << endl;
  G4double thickness = configFile["thickness"]; // width of the scintillator, mm
  G4cout << configFile["thickness"] << " config thickness " << typeid(thickness).name() << G4endl;
  G4String material = configFile["material"]; // type of material, string

  // choose the Random engine
  G4Random::setTheEngine(new CLHEP::RanecuEngine);

  // Use SteppingVerbose with Unit
  G4int precision = 4;
  G4SteppingVerbose::UseBestUnit(precision);

  // construct the run manager
  auto runManager = G4RunManagerFactory::CreateRunManager();
  if (argc == 3)
  {
    G4int nThreads = G4UIcommand::ConvertToInt(argv[2]);
    runManager->SetNumberOfThreads(nThreads);
  }
  // set mandatory initialization classes

  DetectorConstruction *detector = new DetectorConstruction();
  detector->setJsonConfig(configFile);
  detector->SetScintillatorThickness(thickness);
  runManager->SetUserInitialization(detector);

  detector->SetScintillatorThickness(thickness);
  // G4cout << detector->GetScintillatorThickness() << "%%%%%" << G4endl;
  // detector->SetScintillatorType(material);
  runManager->SetUserInitialization(new PhysicsList);

  // set user action classes

  auto action = new ActionInitialization();
  action->setJsonConfig(configFile);
  runManager->SetUserInitialization(action);

  // Initialize G4 kernel
  runManager->Initialize();

  // initialize visualization
  G4VisManager *visManager = nullptr;

  // get the pointer to the User Interface manager
  G4UImanager *UImanager = G4UImanager::GetUIpointer();

  if (ui)
  {
    // interactive mode
    visManager = new G4VisExecutive;
    visManager->Initialize();
    ui->SessionStart();
    delete ui;
  }
  else
  {
    // batch mode
    G4String command = "/control/execute ";
    G4String fileName = argv[1];
    UImanager->ApplyCommand(command + fileName);
  }

  // job termination
  delete visManager;
  delete runManager;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
