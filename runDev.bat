REM set current working directory for convenience
set cwd=%~dp0


REM --- back end ---
REM important to run command from backend dir because of .env
cd backend

REM install needed Python packages
call venv\Scripts\activate
call pip install -r requirements.txt

REM run backend api
start venv\Scripts\flask run
REM start venv\Scripts\flask run --no-debugger
cd ..


REM --- front end ---
cd frontend
start npm run dev
cd ..


REM open Chrome to the default front end URL
REM if something was already on 5173, our frontend will be at a different port
start chrome http://localhost:5173/