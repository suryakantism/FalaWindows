rd /s /q .\Local_Windows\Visitor\
pause

mkdir .\Local_Windows\Visitor\
mkdir .\Local_Windows\Visitor\data\

COPY .\RLMS-Bot\credentials.yml .\Local_Windows\Visitor\
COPY .\RLMS-Bot\config.yml .\Local_Windows\Visitor\
COPY .\RLMS-Bot\docker\endpoints.yml .\Local_Windows\Visitor\
COPY .\RLMS-Bot\nlu_refresh.py .\Local_Windows\Visitor\
pause

XCOPY .\RLMS-Bot\extra .\Local_Windows\Visitor\extra /i
pause

COPY .\RLMS-Bot\docker\visitor\stories.md .\Local_Windows\Visitor\data\
COPY .\RLMS-Bot\docker\visitor\base.md .\Local_Windows\Visitor\extra\
COPY .\RLMS-Bot\docker\visitor\domain.yml .\Local_Windows\Visitor\
pause

cd .\Local_Windows\Visitor\

python nlu_refresh.py
pause
rasa train
pause
rasa run -p 5083 --debug --cors "*"

