rd /s /q .\Local_Windows\Customer\
mkdir .\Local_Windows\Customer\
mkdir .\Local_Windows\Customer\data\

COPY .\RLMS-Bot\credentials.yml .\Local_Windows\Customer\
COPY .\RLMS-Bot\config.yml .\Local_Windows\Customer\
COPY .\RLMS-Bot\docker\endpoints.yml .\Local_Windows\Customer\
COPY .\RLMS-Bot\nlu_refresh.py .\Local_Windows\Customer\
XCOPY .\RLMS-Bot\extra .\Local_Windows\Customer\extra /i

COPY .\RLMS-Bot\docker\customer\stories.md .\Local_Windows\Customer\data\
COPY .\RLMS-Bot\docker\customer\base.md .\Local_Windows\Customer\extra\
COPY .\RLMS-Bot\docker\customer\domain.yml .\Local_Windows\Customer\
cd .\Local_Windows\Customer\

pause
python nlu_refresh.py
pause
rasa train
pause
rasa run -p 5082 --debug --cors "*"