import os
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(r"C:\Dashboard_Frota_Dev")
ISCC = Path(r"C:\Program Files\Inno Setup 7\ISCC.exe")
VERSION = "2.2.0"

def run(cmd, cwd=None):
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=False, text=True)
    if result.returncode != 0:
        print(f"[ERRO] Comando falhou com codigo {result.returncode}")
        sys.exit(1)
    return result

print("=" * 60)
print(f"  BUILD COMPLETO: PyInstaller + Inno Setup v{VERSION}")
print("  Dashboard Frotas - MADEMAXI")
print("=" * 60)

# ============================================================
# ETAPA 1: LIMPEZA
# ============================================================
print("\n=== ETAPA 1/5: LIMPANDO ARQUIVOS TEMPORARIOS ===")

db = BASE / "data" / "app.db"
if db.exists():
    db.unlink()
    print(f"  [OK] Removido: {db}")

logs = BASE / "data" / "logs"
if logs.exists():
    for f in logs.iterdir():
        f.unlink()
    print(f"  [OK] Logs limpos")

config_json = BASE / "data" / "config.json"
if config_json.exists():
    config_json.unlink()
    print(f"  [OK] Removido: {config_json}")

for root, dirs, files in os.walk(BASE):
    for d in dirs:
        if d == "__pycache__":
            p = Path(root) / d
            shutil.rmtree(p, ignore_errors=True)
    for f in files:
        if f.endswith(".pyc"):
            (Path(root) / f).unlink(missing_ok=True)

for folder in ["dist", "build", "dist_installer"]:
    p = BASE / folder
    if p.exists():
        shutil.rmtree(p, ignore_errors=True)
        print(f"  [OK] Removido: {p}")

print("  [OK] Limpo!")

# ============================================================
# ETAPA 2: PYINSTALLER
# ============================================================
print("\n=== ETAPA 2/5: COMPILANDO COM PYINSTALLER ===")

venv_python = BASE / ".venv" / "Scripts" / "python.exe"
if not venv_python.exists():
    print("[ERRO] Ambiente virtual nao encontrado!")
    sys.exit(1)

run([str(venv_python), "-m", "pip", "install", "pyinstaller", "-q"])

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
# ETAPA 3: GERAR CREDITOS E EULA
# ============================================================
print("\n=== ETAPA 3/5: GERANDO CREDITOS E EULA ===")

credits = """\
============================================================
  DASHBOARD FROTAS - MADEMAXI v""" + VERSION + r"""
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

eula_text = """TERMO DE LICENCA DE USO DE SOFTWARE (EULA)
Dashboard Frotas - MADEMAXI
Versao """ + VERSION + """

IMPORTANTE: AO INSTALAR, COPIAR OU UTILIZAR ESTE SOFTWARE, VOCE ACEITA
OS TERMOS E CONDICOES DESTE CONTRATO DE LICENCA. CASO NAO CONCORDE,
NAO INSTALE NEM UTILIZE O SOFTWARE.

1. PROPRIEDADE INTELECTUAL
   Este software e propriedade exclusiva da MADEMAXI - Materiais de
   Construcao e Ferragem e do seu desenvolvedor, Maicon do Amarilho
   Silveira. Todos os direitos autorais, marcas e outros direitos de
   propriedade intelectual pertencem exclusivamente aos seus titulares.

2. LICENCA DE USO
   E concedida ao usuario uma licenca nao exclusiva, intransferivel e
   revogavel para utilizar este software estritamente para fins internos
   da empresa MADEMAXI. Qualquer uso fora deste escopo e estritamente
   proibido.

3. RESTRICOES
   a) E expressamente proibida a venda, aluguel, sublicenciamento ou
      distribuicao comercial deste software, no todo ou em parte.
   b) Nao e permitida a engenharia reversa, descompilacao ou
      desmontagem do software.
   c) A distribuicao nao e permitida sem autorizacao expressa e
      por escrito de Maicon do Amarilho Silveira ou da MADEMAXI.
   d) O download e a utilizacao sao permitidos exclusivamente via
      GitHub (https://github.com/MaiconDAS/Dashboard_Frotas) para fins
      de teste e avaliacao. A utilizacao em ambiente de producao sem
      autorizacao e proibida.

4. ISENCAO DE GARANTIA
   Este software e fornecido "no estado em que se encontra", sem
   garantias de qualquer tipo, expressas ou implicitas. O desenvolvedor
   e a MADEMAXI nao se responsabilizam por quaisquer danos diretos,
   indiretos, incidentais ou consequenciais resultantes do uso ou da
   impossibilidade de uso deste software.

5. SUPORTE
   Para suporte tecnico, entre em contato atraves do GitHub ou e-mail
   institucional da MADEMAXI.

6. ATUALIZACOES
   Este EULA se aplica a todas as atualizacoes, suplementos e
   componentes adicionais do software, salvo disposicao em contrario.

Copyright (C) 2026 MADEMAXI - Todos os direitos reservados.
Desenvolvido por Maicon do Amarilho Silveira.
"""
(BASE / "EULA.txt").write_text(eula_text, encoding="utf-8")
print("  [OK] EULA.txt gerado")

# ============================================================
# ETAPA 4: GERAR SCRIPT ISS
# ============================================================
print("\n=== ETAPA 4/5: GERANDO SCRIPT ISS ===")

iss_lines = [
    '#define MyAppName "Dashboard Frotas"',
    '#define MyAppVersion "' + VERSION + '"',
    '#define MyAppPublisher "MADEMAXI - Materiais de Construcao e Ferragem"',
    '#define MyAppURL "https://github.com/MaiconDAS/Dashboard_Frotas"',
    '#define MyAppExeName "Dashboard_Frotas.exe"',
    '#define MyAppId "{{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}}"',
    '',
    '[Setup]',
    'AppId={#MyAppId}',
    'AppName={#MyAppName}',
    'AppVersion={#MyAppVersion}',
    'AppPublisher={#MyAppPublisher}',
    'AppPublisherURL={#MyAppURL}',
    'AppSupportURL={#MyAppURL}',
    'AppUpdatesURL={#MyAppURL}',
    'DefaultDirName={autopf}\\Dashboard_Frotas',
    'DefaultGroupName=Dashboard Frotas',
    'OutputDir={#SourcePath}\\dist_installer',
    'OutputBaseFilename=Dashboard_Frotas_MADEMAXI_Setup_v{#MyAppVersion}',
    'Compression=lzma',
    'SolidCompression=yes',
    'WizardStyle=modern',
    'PrivilegesRequired=admin',
    'LicenseFile={#SourcePath}\\EULA.txt',
    'InfoAfterFile={#SourcePath}\\credits.txt',
    'VersionInfoCompany={#MyAppPublisher}',
    'VersionInfoDescription=Dashboard de Atividades de Veiculos - Desenvolvido por Maicon do Amarilho Silveira',
    'VersionInfoCopyright=Copyright (C) 2026 MADEMAXI - Todos os direitos reservados',
    'VersionInfoVersion={#MyAppVersion}',
    'UninstallDisplayName={#MyAppName}',
    'UninstallDisplayIcon={app}\\{#MyAppExeName}',
    '',
    '[Languages]',
    'Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\\BrazilianPortuguese.isl"',
    '',
    '[Tasks]',
    'Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked',
    '',
    '[Files]',
    'Source: "{#SourcePath}\\dist\\Dashboard_Frotas.exe"; DestDir: "{app}"; Flags: ignoreversion',
    'Source: "{#SourcePath}\\app\\assets\\logo_mademaxi.png"; DestDir: "{app}\\app\\assets"; Flags: ignoreversion',
    '',
    '[Dirs]',
    'Name: "{app}\\data"',
    'Name: "{app}\\data\\logs"',
    '',
    '[Icons]',
    'Name: "{group}\\Dashboard Frotas"; Filename: "{app}\\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\\{#MyAppExeName}"',
    'Name: "{autodesktop}\\Dashboard Frotas"; Filename: "{app}\\{#MyAppExeName}"; Tasks: desktopicon; WorkingDir: "{app}"; IconFilename: "{app}\\{#MyAppExeName}"',
    '',
    '[Run]',
    'Filename: "{app}\\{#MyAppExeName}"; Description: "Executar Dashboard Frotas agora"; Flags: nowait postinstall skipifsilent',
    '',
    '[Code]',
    'var',
    '  KeepDatabase: Boolean;',
    '  OldDataDir: String;',
    '',
    'function InitializeSetup(): Boolean;',
    'var',
    '  ResultCode: Integer;',
    '  UninstallString: String;',
    'begin',
    '  Result := true;',
    '',
    '  if RegQueryStringValue(HKLM, \'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{#MyAppId}_is1\', \'UninstallString\', UninstallString) then',
    '  begin',
    '    if MsgBox(\'Uma versao anterior do Dashboard Frotas foi detectada neste computador.\' + #13#10 + #13#10 +',
    '              \'Deseja remove-la antes de instalar a nova versao?\', mbConfirmation, MB_YESNO) = IDYES then',
    '    begin',
    '      if MsgBox(\'Deseja MANTER o banco de dados existente?\' + #13#10 + #13#10 +',
    '                \'SIM = Manter veiculos, registros de atividades, cadastros de usuarios e senha mestra.\' + #13#10 +',
    '                \'NAO = Apagar tudo e comecar do zero (irreversivel).\', mbConfirmation, MB_YESNO) = IDYES then',
    '      begin',
    '        KeepDatabase := true;',
    '        OldDataDir := ExpandConstant(\'{app}\\data\');',
    '        if DirExists(OldDataDir) then',
    '        begin',
    '          if not DirExists(ExpandConstant(\'{tmp}\\DashboardFrotasBackup\')) then',
    '            CreateDir(ExpandConstant(\'{tmp}\\DashboardFrotasBackup\'));',
    '          FileCopy(OldDataDir + \'\\app.db\', ExpandConstant(\'{tmp}\\DashboardFrotasBackup\\app.db\'), false);',
    '          FileCopy(OldDataDir + \'\\config.json\', ExpandConstant(\'{tmp}\\DashboardFrotasBackup\\config.json\'), false);',
    '        end;',
    '      end',
    '      else',
    '      begin',
    '        KeepDatabase := false;',
    '      end;',
    '',
    '      Exec(RemoveQuotes(UninstallString), \'/SILENT /NORESTART /SUPPRESSMSGBOXES\', \'\', SW_HIDE, ewWaitUntilTerminated, ResultCode);',
    '    end;',
    '  end;',
    'end;',
    '',
    'procedure CurStepChanged(CurStep: TSetupStep);',
    'begin',
    '  if CurStep = ssPostInstall then',
    '  begin',
    '    if KeepDatabase and FileExists(ExpandConstant(\'{tmp}\\DashboardFrotasBackup\\app.db\')) then',
    '    begin',
    '      if not DirExists(ExpandConstant(\'{app}\\data\')) then',
    '        CreateDir(ExpandConstant(\'{app}\\data\'));',
    '      FileCopy(ExpandConstant(\'{tmp}\\DashboardFrotasBackup\\app.db\'), ExpandConstant(\'{app}\\data\\app.db\'), false);',
    '    end;',
    '    if KeepDatabase and FileExists(ExpandConstant(\'{tmp}\\DashboardFrotasBackup\\config.json\')) then',
    '    begin',
    '      if not DirExists(ExpandConstant(\'{app}\\data\')) then',
    '        CreateDir(ExpandConstant(\'{app}\\data\'));',
    '      FileCopy(ExpandConstant(\'{tmp}\\DashboardFrotasBackup\\config.json\'), ExpandConstant(\'{app}\\data\\config.json\'), false);',
    '    end;',
    '  end;',
    'end;',
]
iss = "\n".join(iss_lines)
(BASE / "Dashboard_Frotas.iss").write_text(iss, encoding="utf-8")
print("  [OK] Dashboard_Frotas.iss gerado")

# ============================================================
# ETAPA 5: INNO SETUP
# ============================================================
print("\n=== ETAPA 5/5: COMPILANDO INSTALADOR ===")

if not ISCC.exists():
    print(f"[ERRO] Inno Setup nao encontrado em: {ISCC}")
    sys.exit(1)

run([str(ISCC), str(BASE / "Dashboard_Frotas.iss")])

installer = BASE / "dist_installer" / f"Dashboard_Frotas_MADEMAXI_Setup_v{VERSION}.exe"
if installer.exists():
    size_mb = installer.stat().st_size / (1024 * 1024)
    print(f"\n{'=' * 60}")
    print("  BUILD CONCLUIDO COM SUCESSO!")
    print(f"{'=' * 60}")
    print(f"  Instalador: {installer}")
    print(f"  Tamanho: {size_mb:.2f} MB")
    print(f"  Versao: {VERSION}")
    print(f"{'=' * 60}")
else:
    print("[ERRO] Instalador nao foi gerado!")
    sys.exit(1)
