# ============================================
# CREER UN REPO PROPRE SANS GROS FICHIERS
# ============================================

Write-Host "Creation d'un repository propre" -ForegroundColor Cyan
Write-Host "============================================================"

# ETAPE 1 : Creer le bon .gitignore
Write-Host ""
Write-Host "ETAPE 1 : Creation du .gitignore" -ForegroundColor Yellow

$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
venv*/
.venv/
*.egg-info/

# IDEs
.vscode/
.idea/
.DS_Store

# DONNEES (gere par DVC) - NE PAS POUSSER
data/raw/*.csv
data/processed/*.csv
data/interim/
!data/raw/.gitignore
!data/processed/.gitignore

# MODELES (gere par DVC/MLflow) - NE PAS POUSSER
models/*.pkl
models/*.h5
models/*.pt
models/*.pth
models/exported/
!models/.gitignore

# MLFLOW - NE PAS POUSSER
mlruns/
mlartifacts/
*.db

# DVC STORAGE - NE PAS POUSSER
dvc_storage/
.dvc/cache/
.dvc/tmp/

# ZENML - NE PAS POUSSER
zenml/
.zen/

# Tests
.pytest_cache/
*.log
"@

$gitignoreContent | Out-File -FilePath .gitignore -Encoding UTF8 -Force
Write-Host "OK - .gitignore cree" -ForegroundColor Green

# ETAPE 2 : Sauvegarder l'ancien repo
Write-Host ""
Write-Host "ETAPE 2 : Backup de l'ancien .git" -ForegroundColor Yellow
if (Test-Path .git) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    Rename-Item .git ".git.backup.$timestamp"
    Write-Host "OK - Ancien .git sauvegarde : .git.backup.$timestamp" -ForegroundColor Green
}

# ETAPE 3 : Initialiser un nouveau repo
Write-Host ""
Write-Host "ETAPE 3 : Initialisation d'un nouveau repo Git" -ForegroundColor Yellow
git init
git branch -M main
Write-Host "OK - Nouveau repo initialise" -ForegroundColor Green

# ETAPE 4 : Ajouter les fichiers (le .gitignore va filtrer)
Write-Host ""
Write-Host "ETAPE 4 : Ajout des fichiers (sans les gros fichiers)" -ForegroundColor Yellow
git add .

# Verifier ce qui sera commite
Write-Host ""
Write-Host "Fichiers a commiter :" -ForegroundColor Cyan
$filesToCommit = git status --short
$filesToCommit | Select-Object -First 30

$fileCount = ($filesToCommit | Measure-Object).Count
Write-Host ""
Write-Host "Total : $fileCount fichiers" -ForegroundColor White

# Verifier la taille
Write-Host ""
Write-Host "Taille du commit :" -ForegroundColor Cyan
git count-objects -vH

# ETAPE 5 : Commit initial propre
Write-Host ""
Write-Host "ETAPE 5 : Commit initial" -ForegroundColor Yellow
git commit -m "Initial commit: MLOps fraud detection project (without large files)"

# ETAPE 6 : Ajouter les remotes
Write-Host ""
Write-Host "ETAPE 6 : Configuration des remotes" -ForegroundColor Yellow
git remote add origin git@github.com:amalsaidi29/fraud-detection-mlops.git
git remote add gitlab https://gitlab.com/amalsaidi29/fraud-detection-mlops.git
git remote -v

# ETAPE 7 : Push
Write-Host ""
Write-Host "ETAPE 7 : Push vers GitLab" -ForegroundColor Yellow
Write-Host "ATTENTION : Cela va ecraser le repository GitLab actuel" -ForegroundColor Red
$confirm = Read-Host "Continuer ? (O/N)"

if ($confirm -eq "O" -or $confirm -eq "o") {
    Write-Host ""
    Write-Host "Push vers GitLab..." -ForegroundColor Green
    git push gitlab main --force
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "SUCCES ! Repository propre pushe vers GitLab" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "Push vers GitHub..." -ForegroundColor Green
        git push origin main --force
        
        Write-Host ""
        Write-Host "TERMINE !" -ForegroundColor Green
        Write-Host ""
        Write-Host "Verifie :" -ForegroundColor Cyan
        Write-Host "   GitLab: https://gitlab.com/amalsaidi29/fraud-detection-mlops" -ForegroundColor White
        Write-Host "   Pipelines: https://gitlab.com/amalsaidi29/fraud-detection-mlops/-/pipelines" -ForegroundColor White
        Write-Host ""
        Write-Host "Ancien .git sauvegarde si besoin de recuperer quelque chose" -ForegroundColor Yellow
    } else {
        Write-Host ""
        Write-Host "Erreur lors du push" -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "Operation annulee" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan