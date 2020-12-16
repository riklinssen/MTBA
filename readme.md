# MTBA-endline analyses reflection workshops

Code to reproduce analyses and visuals for MTBA- published here <add link> --> add link to report here. Visuals [here](https://oxfam.box.com/s/u1gbv1prb8w0ia855mx5t4493fu762h2), overview of variables/KPI's remarks [here](https://oxfam.box.com/s/mfs6vpucwp8ucaw45a617clu2qjzfz9g) -oxfam only access-

# Technologies
Project is created with: 
- STATA 13.1
- Python 3.8.0 

# Data
Source data for this project not public (as of Dec 2020) available on request.

# Structure
```
├───docs                    <- data documentation, questionnaire other relevant docs
│   
│          
│   
│      
│      
│      
│   
├───src                     <-.do (cleaning .py (visualisations) 
│   ├───data                 
│   │   ├───clean           <-Final datasets used for report generation  
│   │   ├───interim         <-intermediate data that has been transformed 
│   │   └───raw             <-original data dump         
│   ├───graphs              <-visualisations in report (not on github)
│   ├───descr_stats.py      <-script to generate descriptive statistics for presentations
│   ├───KPI_scales.py       <-script for visuals KPI's for scales (loaded in CSV instead of dta)
│   └───KPIs.py              <-script to generate visuals for KPI's 
│
└───requirements.txt   <- file that lists python packages used. Use pip install -r requirements.txt
```






