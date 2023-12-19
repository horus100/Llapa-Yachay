# Llapa-Yachay
#### Quechua translation: All - Know
## Blockchain model for university degree registration and issuance
------------
It is a blockchain model focused on the registration and issuance of university degrees, which can consist of up to five participating nodes, with an additional node dedicated to interaction with the public.
### Version
The current project is version 1.0.0.

### State
The current project is a prototype that includes the basic and essential functionalities of a blockchain system, being an initial version, it is recognised that there are some improvements to be added, however, this first version aims to explore the application of this technology in university degrees.
### Prerequisites
This project has been developed and tested on Linux only, and the environment must meet the following requirements
- Ubuntu 20.04 or 22.04 operating system
- Docker Engine 20.10
- Python >= 3.10.0

### Install

Note: Before proceeding, check that the above requirements are met.

1. Download or clone the repository, and go into the Llapayachay folder, and then into the src subfolder:

        cd Llapa-Yachay
        cd src

2. In this folder you will find 2 other folders called participants and public, first go to the participants folder:

        cd participant

3. Run the script image.sh and then the script start.sh

        sh image.sh
        sh start.sh
4. Return to the previous directory and change to the public folder:

        cd ..
        cd public

5. Run the image.sh script and then the start.sh script

        bash image.sh
        bash start.sh
