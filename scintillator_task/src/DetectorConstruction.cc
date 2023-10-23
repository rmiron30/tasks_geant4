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

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

DetectorConstruction::DetectorConstruction()
:G4VUserDetectorConstruction()
{}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

DetectorConstruction::~DetectorConstruction()
{}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

G4VPhysicalVolume* DetectorConstruction::Construct()
{
  //
  // define a material from its elements.   case 1: chemical molecule
  // 
  G4double a, z;
  G4double density; 
  G4double concentrationOfTl; 
  G4int ncomponents, natoms;
 
  G4Element* C = new G4Element("Carbon"  ,"C" , z= 6., a= 12.01*g/mole);
  G4Element* F = new G4Element("Fluorine","F" , z= 9., a= 18.99*g/mole);
 
  G4Material* C6F6 = 
  new G4Material("FluorCarbonate", density= 1.61*g/cm3, ncomponents=2);
  C6F6->AddElement(C, natoms=6);
  C6F6->AddElement(F, natoms=6);
  
  // Definition of CsI(Tl) crystal
  
  // construct Cs and I
  
  G4Element *Cs = new G4Element("Cesium"  ,"Cs" , z=55. , a= 132.91*g/mole);
  G4Element *I = new G4Element("Iodine"  ,"I" , z=53. , a= 126.90*g/mole);
  
  // construct CsI material
  G4Material *CsI = new G4Material("CsI", density= 4.51*g/cm3, ncomponents=2);
  CsI->AddElement(Cs, 1);
  CsI->AddElement(I, 1);
  
  // dope with Thallium
  
  G4Element *Tl = new G4Element("Thallium"  ,"Tl" , z=81. , a= 204.38*g/mole);
  G4Material *doppedCsI = new G4Material("CsITl", density= 4.51*g/cm3, ncomponents=2);
  doppedCsI->AddElement(Tl, concentrationOfTl = 0.001*perCent);
  doppedCsI->AddMaterial(CsI, 100*perCent - concentrationOfTl);
  
  // we can also add the optical properties if needed
  
  G4cout << doppedCsI << G4endl;
  
  // construct BGO
  
  G4NistManager* manager = G4NistManager::Instance();
  
  G4Element *O = manager->FindOrBuildElement(8);
  G4Element *Bi = manager->FindOrBuildElement(83);
  G4Element* Ge = manager->FindOrBuildElement(32);
  
  G4Material *BGO = new G4Material("BGO", density= 7.10*g/cm3, ncomponents=3);
  BGO->AddElement(O , natoms=12);
  BGO->AddElement(Ge, natoms= 3);
  BGO->AddElement(Bi, natoms= 4); 
  
  // cosntruct LYSO
  
  G4Element *Lu = manager->FindOrBuildElement(71);
  G4Element *Si = manager->FindOrBuildElement(14);
  G4Element *Y = manager->FindOrBuildElement(39);
  
  G4Material *LYSO = new G4Material("LYSO", density= 7.4*g/cm3, ncomponents=4);
  LYSO->AddElement(Lu,71*perCent);
  LYSO->AddElement(Si,7*perCent);
  LYSO->AddElement(O, 18*perCent);
  LYSO->AddElement(Y, 4*perCent);
   
  //     
  // Container
  //  
  G4double Rmin=0., Rmax=5*cm, deltaZ= 5*cm, Phimin=0., deltaPhi=360*degree;

  G4Tubs*  
  solidWorld = new G4Tubs("C6F6",                        //its name
                   Rmin,Rmax,deltaZ,Phimin,deltaPhi);        //its size

  G4LogicalVolume*                         
  logicWorld = new G4LogicalVolume(solidWorld,                //its solid
                                   C6F6,                //its material
                                   "C6F6");                //its name
  G4VPhysicalVolume*                                   
  physiWorld = new G4PVPlacement(0,                        //no rotation
                                   G4ThreeVector(),        //at (0,0,0)
                                 logicWorld,                //its logical volume
                                 "C6F6",                //its name
                                 0,                        //its mother  volume
                                 false,                        //no boolean operation
                                 0, true);                        //copy number

  //
  // Scintillator pannel 4cm x 4cm x 2mm
  //
  
  G4double x1 = 4*cm, x2 = 4*cm, x3 = 0.2*cm;
  
  G4Box *scintilBox =  new G4Box("scintilBox", x1, x2, x3);
  
  G4LogicalVolume *logicBox = new G4LogicalVolume(scintilBox, BGO, "logicBox");
  
  G4VPhysicalVolume *physBox = new G4PVPlacement(0,                        //no rotation
                                   G4ThreeVector(),        //at (0,0,0)
                                 logicBox,                //its logical volume
                                 "physBox",                //its name
                                 0,
       //                          logicWorld,                        //its mother  volume
                                 false,                        //no boolean operation
                                 0, true);
  return physBox;
  //new G4PVPlacement(0, G4ThreeVector(1., 0., 0.), logicBox, "physBox", physiWorld, false, 0, true);

  //
  //always return the physical World
  //  
  
  
  
  
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
