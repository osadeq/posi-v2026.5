@echo off
REM ============================================
REM TOSA - Webapp Candidate Starter
REM ============================================

echo.
echo ============================================
echo   TOSA - Webapp Candidate
echo ============================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé
    echo Veuillez installer Python depuis python.org
    pause
    exit /b 1
)

REM Aller dans le dossier webapp
cd /d "%~dp0webapp"

REM Installer les dépendances si nécessaire
if not exist "venv" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Installer les dépendances
echo Installation des dependances...
pip install -r requirements.txt -q

echo.
echo Lancement de la webapp...
echo Adresse: http://localhost:5000
echo.
echo Pour arreter: Ctrl+C
echo.

REM Lancer l'application
python app.py

pause