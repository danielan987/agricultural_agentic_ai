# Agricultural Agentic AI

## Background
Farmers across the globe have to navigate a dynamically changing climate, agricultural regulations, and crop markets that vary significantly depending on their location. This requires adjusting or even pivoting agricultural and irrigation strategies. This user-friendly, agentic AI app for farmers searches the Internet and leverages data to assist them in making these decisions.    

## Architecture 
<img width="945" alt="Screenshot 2025-05-01 at 12 41 33 AM" src="https://github.com/user-attachments/assets/a2f9d779-44ee-4166-aa61-e21408f3c74c" />

On Streamlit, a user selects a location on OpenStreetMap. This gets sent 


back to Streamlit, 



This information is used to first pull 40 years of soil moisture data from the NASA POWER API. This is fed to the Prophet model which will automatically develop forecasts of the soil moisture levels of that location. These native plug-ins gets added to the history 


Semantic kernel because it has multiple native plug-ins
Classic search pre-fetched data retrieval 

In the context of getting data 


After the response from the location identifier, the data analyst agent receives the responses from the local identifier agent as well as from 



The latitude and longitude is sent to the Semantic Kernel where it is received by two native plugins. First/ 

add these plugins to the kernel. 

Within a 
gpt-4o-mini

An automated forecasting model using the Prophet library was applied to more than 40 years of MERRA-2 soil moisture data to identify long-term trends, predict 365 days into the future, and explore seasonal patterns.


## Data Source
The National Aeronautics and Space Administration (NASA) has developed Modern-Era Retrospective analysis for Research and Applications, Version 2 (MERRA-2), which consists of a variety of Earth's climate data since 1981. The data that was used for this project has a parameter name "GWETROOT" and this consists of soil moisture levels across the globe from the surface to 100 cm below the surface (depth of most crops' roots). The value ranges from 0 to 1, with 0 indicating there is no water in the soil and 1 indicating the soil is saturated. There are limitations to this data as it involves modeling and assimilation. Some locations do not have soil moisture data for a variety of reasons, including if the location is in the ocean, and they may have a value of "-999", which gets cleaned before forecasting. 

## Developer Guide

1. Fork this repository.
<img width="143" alt="Screenshot 2025-04-30 at 11 45 18 AM" src="https://github.com/user-attachments/assets/77cba18e-1052-4355-948f-0adbb2a84ed9" />

2. Go to Streamlit Cloud and create an account or log-in: https://share.streamlit.io/
<img width="1482" alt="Screenshot 2025-04-30 at 11 12 28 AM" src="https://github.com/user-attachments/assets/ff1779ad-8490-4fe6-abaf-02a2adea8a6c" />

3. Click on "Create app" then "Deploy a public app from GitHub"
<img width="1522" alt="Screenshot 2025-04-30 at 11 42 14 AM" src="https://github.com/user-attachments/assets/615446ed-2694-4114-ade1-f994c449bf4a" />

<img width="1081" alt="Screenshot 2025-04-30 at 11 18 21 AM" src="https://github.com/user-attachments/assets/30b56274-92eb-4dcd-b5c4-332f0c3995fc" />

4. Select appropriate parameters, including Python 3.12 and your OpenAI API key, to Streamlit secret on "Advanced Settings", then deploy.
<img width="877" alt="Screenshot 2025-04-30 at 11 22 39 AM" src="https://github.com/user-attachments/assets/b323992b-c22d-4854-b0de-30df01aefb63" />
  <img width="856" alt="Screenshot 2025-04-30 at 11 27 52 AM" src="https://github.com/user-attachments/assets/c88db9b6-4ad2-4aad-bd11-4031284468e3" />

## User Guide
1. Open Agricultural Agentic AI App: [https://soilagent.streamlit.app/](https://agricultural-agentic-ai.streamlit.app/)

2. Zoom in and select a location on a map. 
<img width="1213" alt="Screenshot 2025-04-29 at 9 19 48 PM" src="https://github.com/user-attachments/assets/5b106ef8-2626-4e37-b7d8-f4b8908ba868" />
<img width="740" alt="Screenshot 2025-04-30 at 11 54 03 AM" src="https://github.com/user-attachments/assets/d68e738d-c765-4495-b03c-2316c19a0164" />

3. Review responses from agents. 
<img width="1573" alt="Screenshot 2025-05-01 at 12 50 37 AM" src="https://github.com/user-attachments/assets/7b523263-76b2-4a41-b341-42e6ac81ba69" />
<img width="1565" alt="Screenshot 2025-05-01 at 12 51 32 AM" src="https://github.com/user-attachments/assets/a7b97720-3044-403a-90e8-bcc816dd506d" />

4. Ask follow-up questions.
<img width="1599" alt="Screenshot 2025-05-01 at 12 56 52 AM" src="https://github.com/user-attachments/assets/15674285-8d25-447c-a57b-a8cab88405bc" />

5. Repeat Step 3 and Step 4 until satisfied. 

## Contact
Daniel An: daniel.an.893@outlook.com
