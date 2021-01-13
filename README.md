# Meraki SDWAN Extended Automation
This project builds on top of previous developments made by Shiyue Chen. The original web app can be found at https://github.com/shiyuechengineer/meraki-api-demo/tree/master/web_ui. In general terms, this new version includes a new look, as well as the addition of two new functionalities: DC Switchover and Map Monitoring.

## Internal Structure and File Organization
The development of the web app combines different documents, which are organized as follows:
  * **Static:** Contains static files like the CSS, JavaScript, images, fonts and logos.
  * **Templates:** Contains the HTML files for every page of the app.
  * **.env:** Stores the API keys for Meraki Dashboard and HERE Maps. This file also defines the organization number.
  * **flaskapp.py:** The main python function of the program.
  * **flaskapp.wgsi:** Used for deployment on production server. 
  * **merakiapi.py:** Python methods used to get and set data into the Meraki Dashboard. Methods in this file use the Meraki API v0.
  * **merakiapiV1.py:** Python methods used to get and set data into the Meraki Dashboard. Methods in this file use the Meraki API v1.
###### A note on HTML Files
For simplicity, HTML files use inheritance. The base template defines the sidebar and other items that remain the same accross all pages. The other HTML files within the templates folder extend the base file, and therefore redefine the body of the HTML.

## Personalization
This app can be deployed for different companies. To adapt the app for different companies the following components must be modified in the App Settings tab:
* Loss tolerance
* Latency tolerance
* Company name
* Company logo

After wirting the information required and uploading the company logo, it is necessary to submit the changes for the web app to change its template with the personalized information. 


## How to run:
The following list ilustrates how to run the code locally.

1. Clone git repository https://github.com/jperezsan/meraki-sdwan-extended-automation (Collaborator permissions might be needed)
2. Create a virtual environment and activate it
    * Create virtual environment with venv
      ```sh
      python -m venv venv
      ```
      
    Activate using Powershell
      * Open Powershell as an Administrator and run the following command:
        ```powershell
        Set-ExecutionPolicy Unrestricted –Force
        ```
        
      * In the project folder, ensure the venv directory was created
      * Activate the virtual environment using       
        ```powershell
        . .\venv\Scripts\Activate.ps1
        ```        
    Activate using Linux
      * In a terminal window, cd to the project directory and run:        
        ```bsh
        . venv/bin/activate
        ```

3. Upgrade pip and install project's requirenments
   ```sh
    pip install --upgrade pip
    pip install -r requirenments.txt 
    ```
4. Create the following environment variables:
  * It is important not to hardcode the api keys directly in flaskapp.py

    Name | Description
    ----------------|----------------------------
    MERAKI_API_KEY | API key used to access the Dashboard 
    MERAKI_ORG_ID | Organization ID  
    HERE_MAPS_API_KEY | API key issued from the HERE MAPS developer account 

    Using powershell
    ```powershell
    $env:MERAKI_API_KEY=”xxxxxxxxxxxxxxxxx”
    ```  

    Linux
    ```bash
    export MERAKI_API_KEY=”xxxxxxxxxxxxxxxxx”
    ```

  * It is better to create a .env file which contains all the environment variables in order to keep the API_KEY information and the organization ID secure.
    We are using dotenv to read environment variables from a .env file, which is a local file that does not goes up into the github cloud in orden to keep them safe.
    We also store here the information about the API Key needed for Here Maps, the application that shows the map on the map monitoring module.
    The file must be written in the next format:
    
    .env contents:
    ```sh
    MERAKI_API_KEY=”xxxxxxxxxxxxxxxxxxxxxxxxxxxx”
    MERAKI_ORG_ID=”xxxxxxx”
    HERE_MAPS_API_KEY=”xxxxxxxxxxxxxxxxxxxxxxxxxx”
    ```
  
  5. Create FLASK_APP environment variable
  * To run the application with localhost, create another environment variable called FLASK_APP and assign the main    Python application, which is flaskapp.py

      Powershell:
      ```powershell
      $env:FLASK_APP=”flaskapp.py”    
      ```
      Linux:
      ```bash
      export FLASK_APP=”flaskapp.py”
      ```

  6. Run de application on localhost (Only for development)
      ```sh
      flask run
      ```

      The application will run most likely on http://localhost:5000



## DC Switchover Module
The switchover function modifies the configuration of VPN connections. This module only modifies spokes configuration. Hub or data center (DC) configuration still must be done directly on the Meraki Dashboard.

The main function of this module swaps the active and backup hubs for the selected spokes. This happens by clicking on the “SWAP HUBS” button. Whenever the swap action is triggered, a tag is added to the network. This tag states whether the VPN is connected at the primary hub or at the secondary hub. Existing tags in each network are preserved.
The DC switchover module is also capable of replacing the primary, secondary or tertiary VPN hub by manually selecting a specific hub from the dropdown list. After selecting a hub, chose if the hub will be set as primary, secondary, or tertiary. Then, check or uncheck the full tunnel box to enable this VPN link as full tunnel or not. Finally, click on the change hub, and configuration changes will be triggered.

It is possible to change several networks at the same time. Simply check all the networks where changes must be made, and then click the swap hubs or change hubs according to the requested feature.

##### Relevant information:
As of now, there’s no confirmation page saying that changes were made successfully. Additionally, the network list that appears when accessing the DC switchover module gets loaded when the app is launched. Therefore, for updating the network list a reload is required.



## Map Monitoring Module
The Map Monitoring module is perhaps the most relevant module in the app right now. It provides a quick overview of the health of all MX devices within an organization. The map shown on this module color codes all the MX devices. There are five different colors, which represent the following:
 * Green: Everything OK
 * Blue: Only one WAN uplink operational
 * Yellow: Latency above specified tolerance
 * Orange: Loss below specified tolerance
 * Red: No WAN Connectivity

For simplicity, in the map view, close MX devices are grouped together. If at least one MX device within a cluster has a condition different than green, the cluster will be color coded as yellow. When zooming in, clusters break down into smaller cluster if devices are still close the one from each other. If devices are not relatively close, the cluster no longer appears, and instead a rectangle displaying the MX status is shown.

When working with clusters, a table listing all the MX devices within the cluster is shown. This table shows the status of the devices, as well as a button that redirects to that device on the original Meraki dashboard.



