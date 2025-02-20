# KiCadActions
Helper scripts for KiCad CI actions

## Table of Contents
1. [About the Project](#about-the-project)
2. [Project Status](#project-status)
3. [Getting Started](#getting-started)

# About the Project
This project is designed to help with CI/CD workflows. Right now it only contains scripts, but eventually full github workflows will be added.

## Project Status
This project is just starting, if it were a puppy, it would still be stumbling around on unsteady legs, occasionally face planting.

# Getting Started
This is what you're really here for, right?

## Prerequisites 
These scripts use a global Field name `MFG Part Number` which can be added by going to preferences > preferences (or `ctrl + ,`) > schematic editor and adding a Field Name Template. 
![image](https://github.com/user-attachments/assets/1f861eda-364d-4402-8f14-788b41baaed0)


## GenerateBOM
This script searches the current directory that the script is located in for any `.kicad_sch` files and generates a BOM using the filename. Right now the script must be IN the same directory as the project, but there's no reason you can't modify the script
This will create a `.csv` file named `yourprojectname_BOM.csv` for each `.kicad_sch` in the directory

## BOMlookupdigikey
This requires digikey api access. You can sign up for it [here](https://developer.digikey.com/)

### Digikey API steps
You then need to create an [organization](https://developer.digikey.com/teams)
![image](https://github.com/user-attachments/assets/97c6157a-ff88-49b7-91fe-2634446de626)

And a production app 
![image](https://github.com/user-attachments/assets/27ffa148-9a8b-49c7-9afe-2b37df4ac5f9)
![image](https://github.com/user-attachments/assets/e0035f08-a4ca-4f2f-8953-25c26b460e99)
(*note, this needs to be a secure domain, https is required*)

Click on your new app
![image](https://github.com/user-attachments/assets/fba7234d-05ac-4684-86d7-6527844ece74)

Then you can find your Client ID and Client Secret
![image](https://github.com/user-attachments/assets/2d0f13f7-7613-4039-bb39-a4e7b599472a)

Copy and paste these into the BOMlookupdigikey script file

## Running the BOM Lookup Script
This script will look for any CSV's in the current directory with BOM in the name and query the API for the mfg part numbers


# Next Steps
The next thing I'll probably try to implement is checking for direct replacement alternates if a part number is not available.

##### Acknowledgements
Thanks to Phillip Johnston at [Embedded Artistry](https://embeddedartistry.com/) for making a super easy readme template.



