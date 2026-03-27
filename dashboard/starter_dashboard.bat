@echo off
REM ============================================
REM TOSA - Dashboard Admin Starter
REM ============================================

echo.
echo ============================================
echo   TOSA - Dashboard Admin
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

REM Aller dans le dossier dashboard
cd /d "%~dp0dashboard"

REM Installer les dépendances si nécessaire
if not exist "venv" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Vérifier si Flask est installé
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Installation de Flask...
    pip install flask -q
)

echo.
echo Lancement du dashboard...
echo Adresse: http://localhost:5001
echo.
echo Fonctionnalites:
echo   - Tableau de bord
echo   - Gestion des candidats
echo   - Tests recus
echo   - Programmes generes
echo   - Import CSV
echo.
echo Pour arreter: Ctrl+C
echo.

REM Lancer l'application
python main.py

pause