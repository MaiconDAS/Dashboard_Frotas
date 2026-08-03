# Build completo: PyInstaller + Inno Setup
param(
    [string]$InnoSetupPath = ""
)

$ErrorActionPreference = "Stop"
Write-Host "=== BUILD DASHBOARD FROTA ===" -ForegroundColor Cyan

# Detectar PyInstaller
$pyiPath = (Get-Command pyinstaller -ErrorAction SilentlyContinue).Source
if (-not $pyiPath) {
    $candidates = @(
        "C:\Users\amari\AppData\Local\Python\pythoncore-3.14-64\Scripts\pyinstaller.exe"
        "C:\Users\amari\AppData\Local\Programs\Python\Python314\Scripts\pyinstaller.exe"
        "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\Scripts\pyinstaller.exe"
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) { $pyiPath = $c; break }
    }
}
if (-not $pyiPath) {
    Write-Error "PyInstaller nao encontrado. Rode: pip install pyinstaller"
    exit 1
}
Write-Host "PyInstaller: $pyiPath" -ForegroundColor Green

# Detectar Inno Setup
if (-not $InnoSetupPath) {
    $isccCandidates = @(
        "C:\Program Files\Inno Setup 7\ISCC.exe"
        "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
        "C:\Program Files\Inno Setup 6\ISCC.exe"
    )
    foreach ($c in $isccCandidates) {
        if (Test-Path $c) { $InnoSetupPath = $c; break }
    }
}
if (-not (Test-Path $InnoSetupPath)) {
    Write-Error "Inno Setup nao encontrado. Instale em https://jrsoftware.org/isdl.php"
    exit 1
}
Write-Host "Inno Setup: $InnoSetupPath" -ForegroundColor Green

# Limpar
Write-Host "[1/4] Limpando..." -ForegroundColor Green
Remove-Item -Path ".\build",".\dist",".\dist_installer" -Recurse -Force -ErrorAction SilentlyContinue

# Build PyInstaller
Write-Host "[2/4] PyInstaller..." -ForegroundColor Green
& $pyiPath DashboardFrota.spec --clean --noconfirm
if (-not (Test-Path ".\dist\DashboardFrota\DashboardFrota.exe")) {
    Write-Error "Falha no PyInstaller."; exit 1
}
Write-Host "[3/4] EXE OK!" -ForegroundColor Green

# Build Installer
Write-Host "[4/4] Inno Setup..." -ForegroundColor Green
& $InnoSetupPath ".\installer.iss"
if (Test-Path ".\dist_installer\DashboardFrota_Setup_v1.0.0.exe") {
    Write-Host ""
    Write-Host "=== CONCLUIDO ===" -ForegroundColor Green
    Write-Host "Instalador: $(Resolve-Path .\dist_installer\DashboardFrota_Setup_v1.0.0.exe)" -ForegroundColor Cyan
} else {
    Write-Error "Falha no Inno Setup."
}
