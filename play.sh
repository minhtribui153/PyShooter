if ! command -v python3
then
    echo "[ERROR] Python 3 could not be found. Please install the latest version of Python 3 on https://www.python.org/"
    exit 1
fi

clear
echo =======================
echo Installing Dependencies
echo =======================
pip3 install -r requirements.txt

clear
echo =====================
echo Welcome to PyShooter!
echo =====================
python3 src/main.py