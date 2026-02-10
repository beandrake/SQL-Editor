REM - This is a batch script.
REM - Lines that start with REM are informational comments, not code that runs.

REM Record current working directory for convenience.
set cwd=%~dp0



REM --------------- BACK END -----------------

REM It's important to run the backend from backend dir because of .env file.
cd backend

REM Create a Python virtual environment for Python packages.
call python -m venv venv

REM Activate the virtual environment.
call venv\Scripts\activate

REM Install needed Python packages in virtual environment.
call pip install -r requirements.txt

REM Start the backend, which is a Flask Python API.
start venv\Scripts\flask run
REM start venv\Scripts\flask run --no-debugger

REM Navigate to parent directory.
cd ..



REM --------------- FRONT END -----------------

REM Navigate to frontend directory.
cd frontend

REM Start the frontend, which uses React.
start npm run dev


REM Return to parent directory.
cd ..


REM Open Chrome to the default front end URL.
REM If something was already on 5173, our frontend will be at a different port!
start chrome http://localhost:5173/