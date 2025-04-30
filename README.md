# Agricultural Agentic AI

## Overview
Farmers across the globe have to navigate a dynamically changing climate, agricultural regulations, and crop markets that vary significantly depending on their location. Data AND has so much potential to help local farmers adjust or even pivot agricultural or irrigation strategies but because they are not as familiar with them, they have to rely on their intuitions. A user-friendly, agentic AI app for farmers to understand more about the dynamic changes in where they are farming. This will ultimately impact global food supplies, water sustainability. 

## Architecture Overview



## Data Source
Soil moisture data from National Aeronautics and Space Administration (NASA). 
ranges of 

It measures soil moisture level across the globe from the surface to 100 cm below the surface (depth of most crops' roots). 


NASA's soil moisture data from 1981 to the present day. 
The value ranges from 0 to 1. 0 indicates the soil is completely water-free and 1 indicates the soil is completely saturated. 


## Developer Guide

1. Fork this repository.
   <img width="143" alt="Screenshot 2025-04-30 at 11 45 18 AM" src="https://github.com/user-attachments/assets/77cba18e-1052-4355-948f-0adbb2a84ed9" />

3. Go to Streamlit Cloud and create an account or log-in: https://share.streamlit.io/
<img width="1482" alt="Screenshot 2025-04-30 at 11 12 28 AM" src="https://github.com/user-attachments/assets/c39dd924-372c-486a-a21b-1e0d0eccb03d" />

4. Click on "Create app" then "Deploy a public app from GitHub"
<img width="1522" alt="Screenshot 2025-04-30 at 11 42 14 AM" src="https://github.com/user-attachments/assets/615446ed-2694-4114-ade1-f994c449bf4a" />


<img width="1081" alt="Screenshot 2025-04-30 at 11 18 21 AM" src="https://github.com/user-attachments/assets/85243b1f-bfc4-46aa-83e1-dad5bbf2a3e0" />


4. Select appropriate parameters, including Python 3.12 and your OpenAI API key to Streamlit secret on "Advanced Settings", then deploy.
<img width="877" alt="Screenshot 2025-04-30 at 11 22 39 AM" src="https://github.com/user-attachments/assets/506cb0f5-7f81-478c-aeb6-6ca0d8146e97" />

<img width="856" alt="Screenshot 2025-04-30 at 11 27 52 AM" src="https://github.com/user-attachments/assets/2e8a16cb-eaf4-42bb-a1b5-13f121ce2a1c" />



 





## User Guide
1. Open Soil Agent App: https://soilagent.streamlit.app/

2. Select a location on a map. 
<img width="1213" alt="Screenshot 2025-04-29 at 9 19 48 PM" src="https://github.com/user-attachments/assets/20c3becc-a236-4799-b88c-aeacbc0c3847" />

3. Review response. 

4. Ask follow-up questions or provide feedback.
  
6. Repeat Step 3 and Step 4 until . 





clean the data 
and the history is deleted after use.
(If you select a location like in the ocean or somewhere you can't detect soil moisture, it will not work).

Farmers can select their location on a global map to access tailored analyses of their farmland including trajectories and seasonal variations of their land and next year's soil moisture predictions based on decades of MERRA-2 data. This supports efficient irrigation management and crop production which ultimately supports global water sustainability.

This tool allows farmers across the globe to zoom in on a Folium map to click on their location for analysis. Depending on the location, language may be adjusted to make it easier for the farmer to find their location.
This location data is sent to the NASA POWER API to retrieve the earliest to latest soil moisture data. This amount of historical data makes it possible for a forecasting model using the Prophet library to analyze long-term trends and seasonal cycles and predict soil moisture levels 365 days into the future. Prophet accounts for non-linear trends using a piecewise linear model and accounts for seasonal cycles using a Fourier series that decomposes the cycle into a series of sine and cosine terms. Nevertheless, it is a lightweight automated model in a lightweight Streamlit application. Thus, the analyses are provided to the farmers on-demand.
The first analysis is a line graph of the data from 1981 to the current date. The value ranges from 0 to 1 with 0 indicating the soil is completely water-free and 1 indicating the soil is completely saturated. The second analysis follows a similar format but consists of predicted values 365 days from the current date with confidence intervals. The third analysis decomposes the data to visualize the general trend without the fluctuations. The fourth analysis decomposes the data to visualize the impact of the seasonal cycle that occurs within each year on soil moisture levels. Each visualization is written in English with emojis, numbers and international units of measurement to make it easier to comprehend for everyone across the globe.
Farmers can also switch between 3 different depths of soil. This includes from the surface to 5cm below the surface which is the level most affected by precipitation, evapotranspiration, and other surface-level environmental factors. There is also from the surface to 100 cm below the surface which is the depth of most crops' roots. Finally, Profile Soil Moisture which is the soil moisture data from the surface to the bedrock. This indicates the soil's overall moisture level and is difficult for most farmers to figure out themselves.
These analyses help farmers understand their farm better and plan ahead. By adjusting seasonal irrigation strategies, switching to crops suited for the projected moisture levels, or deciding to purchase crop insurance.

An automated forecasting model using the Prophet library was applied to more than 40 years of MERRA-2 soil moisture data to identify long-term trends, predict 365 days into the future, and explore seasonal patterns.






## Conclusion


Contact
Daniel An: daniel.an.893@outlook.com

