#define MyAppName "Dashboard Frotas"
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
