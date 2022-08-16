WHERE python
IF %ERRORLEVEL% NEQ 0 ECHO "[ERROR] Python could not be found. Please install the latest version of Python on https://www.python.org/" && exit 1

cls
echo =======================
echo Installing Dependencies
echo =======================
pip install -r requirements.txt

cls
echo =======================
echo Opening Level Editor...
echo =======================
python src/level_editor.py