rd /s /q .\Local_Windows\Admin\
pause

mkdir .\Local_Windows\Admin\
mkdir .\Local_Windows\Admin\data\

COPY .\RLMS-Bot\credentials.yml .\Local_Windows\Admin\
COPY .\RLMS-Bot\config.yml .\Local_Windows\Admin\
COPY .\RLMS-Bot\docker\endpoints.yml .\Local_Windows\Admin\
COPY .\RLMS-Bot\nlu_refresh.py .\Local_Windows\Admin\
pause

XCOPY .\RLMS-Bot\extra .\Local_Windows\Admin\extra /i
pause

COPY .\RLMS-Bot\docker\admin\stories.md .\Local_Windows\Admin\data\
COPY .\RLMS-Bot\docker\admin\base.md .\Local_Windows\Admin\extra\
COPY .\RLMS-Bot\docker\admin\domain.yml .\Local_Windows\Admin\
pause

pause

cd .\Local_Windows\Admin\

python nlu_refresh.py
pause
rasa train
pause
rasa run -p 5081 --debug --cors "*"