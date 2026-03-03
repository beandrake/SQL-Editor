# SQL-Editor
Playing around with making my own interface to tinker with SQL on the fly, using React and Flask. Currently very much a work in progress.

## Windows Instructions:
1. You'll need [`git`](https://git-scm.com/), [`Node.js`](https://nodejs.org/) 25.2.1 or later , and [`Python`](https://nodejs.org/) 3.14.0 or later, so install those if you need them. 

2. Make a local clone of this repository via your preferred method.

3. Ideally, you should just be able to run `runDev.bat`, which will open command windows for the backend and frontend.   It will also try to open a new Chrome browser tab to `http://localhost:5173/`, which is the default port the frontend will attach to so long as that port isn't already occupied.

4. If you prefer to use a different web browser, simply open it to `http://localhost:5173/`.

5. The interface allows you to write and execute [`SQLite`](https://sqlite.org/index.html) queries.  Several database tables are preloaded with some simple statistical data each time the program is run, in case you'd like to play around with that.