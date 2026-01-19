@echo off
echo Starting IPv6 Network Manager...
echo Activating Virtual Environment...

REM check path and activate venv
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo Error: 'venv' folder not found. Please set up the project first.
    pause
    exit
)

echo Launching Streamlit Dashboard...
streamlit run app.py

pause