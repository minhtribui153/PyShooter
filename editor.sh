if ! command -v python3
then
    echo "[ERROR] Python 3 could not be found. Please install the latest version of Python 3."
    exit 1
fi

clear
echo =======================
echo Installing Dependencies
echo =======================
pip3 install -r requirements.txt

clear
echo =======================
echo Opening Level Editor...
echo =======================
python3 src/level_editor.py