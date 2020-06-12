rd /s /q .\Local_Windows\Action\
mkdir .\Local_Windows\Action\

COPY .\RLMS-Bot\actions.py .\Local_Windows\Action\
COPY .\RLMS-Bot\docker\config.py .\Local_Windows\Action\

cd .\Local_Windows\Action\
pause

python -m rasa run actions --debug