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
/// \file electromagnetic/TestEm4/src/DetectorConstruction.cc
/// \brief Implementation of the DetectorConstruction class
//
//
//

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#include "DetectorConstruction.hh"

#include "G4Material.hh"
#include "G4Tubs.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4NistManager.hh"

#include "json/json.hpp"

using namespace std;
using json = nlohmann::json;

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

// json readfile(string name)
// {
//     ifstream file(name);
//     json j;
//     file >> j;

//     return j;
// }

DetectorConstruction::DetectorConstruction()
    : G4VUserDetectorConstruction()
{
  // auto configFile = readfile("/home/raluca/geant4/tasks_geant4/scintillator_task/config.json");
  // fThickness = configFile["thickness"];
  // // fMat = configFile["material"];
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

DetectorConstruction::~DetectorConstruction()
{
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

G4VPhysicalVolume *DetectorConstruction::Construct()
{
  //
  // define a material from its elements
  //
  G4double a, z;
  G4double density;
  G4double concentrationOfTl;
  G4int ncomponents, natoms;

  // Definition of CsI(Tl) crystal

  // construct Cs and I

  G4Element *Cs = new G4Element("Cesium", "Cs", z = 55., a = 132.91 * g / mole);
  G4Element *I = new G4Element("Iodine", "I", z = 53., a = 126.90 * g / mole);

  // construct CsI material
  G4Material *CsI = new G4Material("CsI", density = 4.51 * g / cm3, ncomponents = 2);
  CsI->AddElement(Cs, 1);
  CsI->AddElement(I, 1);

  // dope with Thallium

  G4Element *Tl = new G4Element("Thallium", "Tl", z = 81., a = 204.38 * g / mole);
  // G4Material *doppedCsI = new G4Material("CsITl", density = 4.51 * g / cm3, ncomponents = 2);
  // doppedCsI->AddElement(Tl, concentrationOfTl = 0.001 * perCent);
  // doppedCsI->AddMaterial(CsI, 100 * perCent - concentrationOfTl);

  // we can also add the optical properties if needed

  // construct BGO

  G4NistManager *manager = G4NistManager::Instance();

  G4Element *O = manager->FindOrBuildElement(8);
  G4Element *Bi = manager->FindOrBuildElement(83);
  G4Element *Ge = manager->FindOrBuildElement(32);

  // G4Material *BGO = new G4Material("BGO", density = 7.10 * g / cm3, ncomponents = 3);
  // BGO->AddElement(O, natoms = 12);
  // BGO->AddElement(Ge, natoms = 3);
  // BGO->AddElement(Bi, natoms = 4);

  // cosntruct LYSO

  G4Element *Lu = manager->FindOrBuildElement(71);
  G4Element *Si = manager->FindOrBuildElement(14);
  G4Element *Y = manager->FindOrBuildElement(39);

  // G4Material *LYSO = new G4Material("LYSO", density = 7.4 * g / cm3, ncomponents = 4);
  // LYSO->AddElement(Lu, 71 * perCent);
  // LYSO->AddElement(Si, 7 * perCent);
  // LYSO->AddElement(O, 18 * perCent);
  // LYSO->AddElement(Y, 4 * perCent);

  // CONTAINERUL PENTRU SCINTILATOR - CONTINE AER SAU VID
  G4double Xw = 15 * cm, Yw = 15 * cm, Zw = 15 * cm;

  G4Box *BBox = new G4Box("BBox", Xw, Yw, Zw);
  G4Material *galactic = manager->FindOrBuildMaterial("G4_AIR");
  G4LogicalVolume *BBoxLV = new G4LogicalVolume(BBox, galactic, "BBoxLV");
  G4VPhysicalVolume *BBoxphys = new G4PVPlacement(0,               // no rotation
                                                  G4ThreeVector(), // at (0,0,0)
                                                  BBoxLV,          // its logical volume
                                                  "BBoxphys",      // its name
                                                  0,               // its mother  volume
                                                  false,           // no boolean operation
                                                  0, true);        // copy number

  //
  // Scintillator pannel 4cm x 4cm x 2mm
  //

  // G4cout << fThickness << " " << std::this_thread::get_id() << G4endl;

  G4double x1 = 1 * mm, x2 = 1 * mm, x3 = fThickness * mm;
  // G4cout << x3 << "x3" << G4endl;

  // G4cout << config["thickness"] << " x3 " << G4endl;

  G4Box *scintilBox = new G4Box("scintilBox", x1, x2, config["thickness"]);
  // G4Box *scintilBox = new G4Box("scintilBox", x1, x2, x3);
  G4Material *mat;

  if (config["material"] == "LYSO")
  {

    mat = new G4Material("LYSO", density = 7.4 * g / cm3, ncomponents = 4);
    mat->AddElement(Lu, 71 * perCent);
    mat->AddElement(Si, 7 * perCent);
    mat->AddElement(O, 18 * perCent);
    mat->AddElement(Y, 4 * perCent);
  }
  else if (config["material"] == "BGO")
  {
    mat = new G4Material("BGO", density = 7.10 * g / cm3, ncomponents = 3);
    mat->AddElement(O, natoms = 12);
    mat->AddElement(Ge, natoms = 3);
    mat->AddElement(Bi, natoms = 4);
  }
  else if (config["material"] == "CsI")
  {
    mat = new G4Material("CsITl", density = 4.51 * g / cm3, ncomponents = 2);
    mat->AddElement(Tl, concentrationOfTl = 0.001 * perCent);
    mat->AddMaterial(CsI, 100 * perCent - concentrationOfTl);
  }
  // else if(){}
  // } else {
  //   G4LogicalVolume *logicBox = new G4LogicalVolume(scintilBox, LYSO, "logicBox");
  // }

  G4LogicalVolume *logicBox = new G4LogicalVolume(scintilBox, mat, "logicBox");

  G4VPhysicalVolume *physBox = new G4PVPlacement(0,               // no rotation
                                                 G4ThreeVector(), // at (0,0,0)
                                                 logicBox,        // its logical volume
                                                 "physBox",       // its name
                                                 BBoxLV,          // its mother  volume
                                                 false,           // no boolean operation
                                                 0, true);

  return BBoxphys;
  // new G4PVPlacement(0, G4ThreeVector(1., 0., 0.), logicBox, "physBox", physiWorld, false, 0, true);

  //
  // always return the physical World
  //
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
