rd /s /q .\Local_Windows\Utility\
mkdir .\Local_Windows\Utility\

xcopy .\RLMS-Utility\modules .\Local_Windows\Utility\modules /i
copy .\RLMS-Utility\app.py .\Local_Windows\Utility\

rem python -m pip install -r .\RLMS-Utility\requirements.txt
rem python -m nltk.downloader "punkt"
rem python -m nltk.downloader "wordnet" 

cd .\Local_Windows\Utility\
pause

python app.py