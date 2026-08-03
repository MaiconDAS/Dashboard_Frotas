; Inno Setup 7 - Dashboard Frota Installer
; Build: rode primeiro o PyInstaller, depois compile este script no Inno Setup Compiler

#define MyAppName "Dashboard Frota"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Maicon do Amarilho Silveira"
#define MyAppExeName "DashboardFrota.exe"
#define MyAppId "{{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL=https://maiconamarilho@gmail.com
AppSupportURL=https://maiconamarilho@gmail.com
AppUpdatesURL=https://maiconamarilho@gmail.com
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=LICENSE.txt
OutputDir=.\dist_installer
OutputBaseFilename=DashboardFrota_Setup_v{#MyAppVersion}
SetupIconFile=logo.ico
WizardImageFile=logo.bmp
WizardSmallImageFile=logo_small.bmp
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
CloseApplications=force

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: ".\dist\DashboardFrota\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "logo.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\logo.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\logo.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
  UninstallString: String;
begin
  Result := True;
  
  if RegQueryStringValue(HKLM, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppId}_is1', 'UninstallString', UninstallString) then
  begin
    if MsgBox('Uma versao anterior do Dashboard Frota foi detectada.' + #13#10 + #13#10 + 'Deseja desinstalar a versao anterior antes de continuar?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      Exec(RemoveQuotes(UninstallString), '/SILENT', '', SW_SHOWNORMAL, ewWaitUntilTerminated, ResultCode);
      Sleep(2000);
    end;
  end
  else if RegQueryStringValue(HKCU, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppId}_is1', 'UninstallString', UninstallString) then
  begin
    if MsgBox('Uma versao anterior do Dashboard Frota foi detectada.' + #13#10 + #13#10 + 'Deseja desinstalar a versao anterior antes de continuar?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      Exec(RemoveQuotes(UninstallString), '/SILENT', '', SW_SHOWNORMAL, ewWaitUntilTerminated, ResultCode);
      Sleep(2000);
    end;
  end;
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpLicense then
  begin
    WizardForm.LicenseMemo.Text := WizardForm.LicenseMemo.Text + #13#10 + #13#10 +
      'Duvidas ou suporte: maiconamarilho@gmail.com' + #13#10 +
      'Desenvolvedor: Maicon do Amarilho Silveira';
  end;
end;
