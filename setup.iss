[Setup]
AppName=DontForgetToSave
AppVersion=1.0
DefaultDirName={pf}\DontForgetToSave
DefaultGroupName=DontForgetToSave
OutputDir=.
OutputBaseFilename=DontForgetToSave_installer
PrivilegesRequired=admin
AllowNoIcons=yes
RestartIfNeededByRun=false

[Files]
Source: "dist\DontForgetToSave\DontForgetToSave.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DontForgetToSave"; Filename: "{app}\DontForgetToSave.exe"
Name: "{commondesktop}\DontForgetToSave"; Filename: "{app}\DontForgetToSave.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\DontForgetToSave.exe"; Description: "Run DontForgetToSave"; Flags: nowait postinstall skipifsilent
