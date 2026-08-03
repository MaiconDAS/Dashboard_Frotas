import os
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(r"C:\Dashboard_Frota_Dev")
ISCC = Path(r"C:\Program Files\Inno Setup 7\ISCC.exe")

def run(cmd, cwd=None):
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=False, text=True)
    if result.returncode != 0:
        print(f"[ERRO] Comando falhou com codigo {result.returncode}")
        sys.exit(1)
    return result

print("=" * 60)
print("  BUILD COMPLETO: PyInstaller + Inno Setup")
print("  Dashboard Frotas - MADEMAXI")
print("=" * 60)

# ============================================================
# ETAPA 1: LIMPEZA
# ============================================================
print("\n=== ETAPA 1/4: LIMPANDO ARQUIVOS TEMPORARIOS ===")

# Dados sensiveis
db = BASE / "data" / "app.db"
if db.exists():
    db.unlink()
    print(f"  [OK] Removido: {db}")

logs = BASE / "data" / "logs"
if logs.exists():
    for f in logs.iterdir():
        f.unlink()
    print(f"  [OK] Logs limpos")

# Caches
for root, dirs, files in os.walk(BASE):
    for d in dirs:
        if d == "__pycache__":
            p = Path(root) / d
            shutil.rmtree(p)
    for f in files:
        if f.endswith(".pyc"):
            (Path(root) / f).unlink()

# Builds anteriores
for folder in ["dist", "build", "dist_installer"]:
    p = BASE / folder
    if p.exists():
        shutil.rmtree(p)
        print(f"  [OK] Removido: {p}")

print("  [OK] Limpo!")

# ============================================================
# ETAPA 2: PYINSTALLER
# ============================================================
print("\n=== ETAPA 2/4: COMPILANDO COM PYINSTALLER ===")

venv_python = BASE / ".venv" / "Scripts" / "python.exe"
if not venv_python.exists():
    print("[ERRO] Ambiente virtual nao encontrado!")
    sys.exit(1)

# Instala pyinstaller
run([str(venv_python), "-m", "pip", "install", "pyinstaller", "-q"])

# Compila
run([
    str(venv_python), "-m", "PyInstaller",
    "--name", "Dashboard_Frotas",
    "--windowed",
    "--onefile",
    "--add-data", f"app{os.pathsep}app",
    "--add-data", f"data{os.pathsep}data",
    "--icon", str(BASE / "app" / "assets" / "logo_mademaxi.png"),
    "--distpath", str(BASE / "dist"),
    "--workpath", str(BASE / "build"),
    "--specpath", str(BASE),
    "--noconfirm",
    str(BASE / "run.py")
], cwd=BASE)

exe_path = BASE / "dist" / "Dashboard_Frotas.exe"
if not exe_path.exists():
    print("[ERRO] Executavel nao foi gerado!")
    sys.exit(1)

print(f"  [OK] Executavel: {exe_path}")

# ============================================================
# ETAPA 3: GERAR CREDITOS E ISS
# ============================================================
print("\n=== ETAPA 3/4: GERANDO CREDITOS E SCRIPT ISS ===")

credits = """\
============================================================
  DASHBOARD FROTAS - MADEMAXI
============================================================

Empresa: MADEMAXI - Materiais de Construcao e Ferragem
Todos os direitos reservados (C) 2026

Desenvolvido por:
  Maicon do Amarilho Silveira
  GitHub: https://github.com/MaiconDAS

Este software e propriedade exclusiva da MADEMAXI.
Qualquer reproducao, distribuicao ou modificacao sem
autorizacao expressa e estritamente proibida.

Para suporte tecnico, entre em contato com o desenvolvedor
atraves do GitHub ou e-mail institucional.

Obrigado por utilizar o Dashboard Frotas!
============================================================
"""
(BASE / "credits.txt").write_text(credits, encoding="utf-8")
print("  [OK] credits.txt gerado")

iss = r'''#define MyAppName "Dashboard Frotas"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "MADEMAXI - Materiais de Construcao e Ferragem"
#define MyAppURL "https://github.com/MaiconDAS"
#define MyAppExeName "Dashboard_Frotas.exe"
#define MyAppId "{{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}}"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\Dashboard_Frotas
DefaultGroupName=Dashboard Frotas
OutputDir={#SourcePath}\dist_installer
OutputBaseFilename=Dashboard_Frotas_MADEMAXI_Setup_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
InfoAfterFile={#SourcePath}\credits.txt
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Dashboard de Atividades de Veiculos - Desenvolvido por Maicon do Amarilho Silveira
VersionInfoCopyright=Copyright (C) 2026 MADEMAXI - Todos os direitos reservados
VersionInfoVersion={#MyAppVersion}
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#SourcePath}\dist\Dashboard_Frotas.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}\app\assets\logo_mademaxi.png"; DestDir: "{app}\app\assets"; Flags: ignoreversion

[Dirs]
Name: "{app}\data"
Name: "{app}\data\logs"

[Icons]
Name: "{group}\Dashboard Frotas"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Dashboard Frotas"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Executar Dashboard Frotas agora"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
  UninstallString: String;
begin
  if RegQueryStringValue(HKLM, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppId}_is1', 'UninstallString', UninstallString) then
  begin
    if MsgBox('Uma versao anterior do Dashboard Frotas foi detectada.' + #13#10 + 'Deseja remove-la antes de instalar a nova versao?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      Exec(RemoveQuotes(UninstallString), '/SILENT /NORESTART /SUPPRESSMSGBOXES', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    end;
  end;
  Result := true;
end;
'''
(BASE / "Dashboard_Frotas.iss").write_text(iss, encoding="utf-8")
print("  [OK] Dashboard_Frotas.iss gerado")

# ============================================================
# ETAPA 4: INNO SETUP
# ============================================================
print("\n=== ETAPA 4/4: COMPILANDO INSTALADOR ===")

if not ISCC.exists():
    print(f"[ERRO] Inno Setup nao encontrado em: {ISCC}")
    sys.exit(1)

run([str(ISCC), str(BASE / "Dashboard_Frotas.iss")])

installer = BASE / "dist_installer" / "Dashboard_Frotas_MADEMAXI_Setup_v1.0.0.exe"
if installer.exists():
    size_mb = installer.stat().st_size / (1024 * 1024)
    print(f"\n{'=' * 60}")
    print("  BUILD CONCLUIDO COM SUCESSO!")
    print(f"{'=' * 60}")
    print(f"  Instalador: {installer}")
    print(f"  Tamanho: {size_mb:.2f} MB")
    print(f"{'=' * 60}")
else:
    print("[ERRO] Instalador nao foi gerado!")
    sys.exit(1)
