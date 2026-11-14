# Recursion Lab

A free, independent study tool for UC Berkeley CS 61A exams and quizzes. Practice recursion and iteration with interactive Python exercises, editable doctests, and hints.

**[Open Recursion Lab in your browser](https://ruthvik102008.github.io/recursion-lab/lessons/home.html)**

To open the lab in a new tab from GitHub, Ctrl-click the link (Command-click on macOS).

## Run locally

1. Install Python 3 if you don't already have it.
2. On this repository's GitHub page, select **Code → Download ZIP**, then unzip it. You can also clone it with `git clone https://github.com/Ruthvik102008/recursion-lab.git`.
3. Open a terminal in the extracted or cloned folder, where `README.md` is located. Run the command for your system:

   | System | Command |
   | --- | --- |
   | Windows | `py -3 -m http.server 8000 --bind 127.0.0.1` |
   | macOS or Linux | `python3 -m http.server 8000 --bind 127.0.0.1` |

   On Windows, if `py` is unavailable and `python --version` reports Python 3, use `python -m http.server 8000 --bind 127.0.0.1`.

4. Keep the terminal open and visit [Recursion Lab](http://127.0.0.1:8000/) in a current browser. Press **Ctrl+C** in the terminal when you're done.

Use the local URL so the browser can load the Python worker and exercises. If port 8000 is already in use, choose another port in both the command and the URL. Keep using the same browser profile and URL to retain your saved work.

## How it works

The app runs Python in your browser through Pyodide. Internet access is needed to load the Python runtime and open linked videos. Drafts and progress are stored in your browser.

Course references and videos are credited in the lesson notes.
