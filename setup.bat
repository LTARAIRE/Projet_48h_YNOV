@echo off

REM Vérifie si Python est installé
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installé ou n'est pas dans le PATH.
    exit /b 1
)

REM Crée l'environnement virtuel s'il n'existe pas
IF NOT EXIST .venv (
    echo Création de l'environnement virtuel...
    python -m venv .venv
) ELSE (
    echo L'environnement virtuel existe déjà.
)

REM Active l'environnement virtuel
echo Activation de l'environnement virtuel...
call .venv\Scripts\activate

REM Met à jour pip
echo Mise à jour de pip...
pip install --upgrade pip

REM Installe les dépendances depuis requirements.txt
IF EXIST requirements.txt (
    echo Installation des dépendances...
    pip install -r requirements.txt
) ELSE (
    echo Le fichier requirements.txt est introuvable.
)

echo Configuration terminée. Activez l'environnement avec :
echo   .venv\Scripts\activate
exit /b 0
