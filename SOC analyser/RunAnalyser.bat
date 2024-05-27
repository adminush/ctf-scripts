@echo off
echo    _____ ____  ______                     __                    
echo   / ___// __ \/ ____/  ____ _____  ____ _/ /_  __________  _____
echo   \__ \/ / / / /      / __ `/ __ \/ __ `/ / / / / ___/ _ \/ ___/
echo  ___/ / /_/ / /___   / /_/ / / / / /_/ / / /_/ (__  )  __/ /    
echo /____/\____/\____/   \__,_/_/ /_/\__,_/_/\__, /____/\___/_/     
echo                                         /____/                  
echo - - - -
echo 1. Enter the domain name of Windows PC;
echo 2. The main event logs, registry values and console output will be saved to the RESULT folder;
echo 3. The Security log is analyzed first, press: "ENTER", "ENTER", "N";
echo 4. The second is analyze the Sysmon log, press "ENTER", "ENTER", "ENTER".
echo - - - -
set /p Hostname=Enter hostname (example: win2022serv): 
echo Wait some seconds...
powershell -Command "& {New-Item -Path '.\Result\' -Name "%Hostname%" -ItemType 'directory'}" 
powershell -Command "& {Copy-Item \\%Hostname%\C$\WINDOWS\System32\winevt\Logs\Security.evtx -Destination .\Result\%Hostname%\; Rename-Item -Path ".\Result\%Hostname%\Security.evtx" -NewName "%Hostname%-Security.evtx"; Copy-Item \\%Hostname%\C$\WINDOWS\System32\winevt\Logs\Microsoft-Windows-Sysmon%%4Operational.evtx -Destination .\Result\%Hostname%; Rename-Item -Path ".\Result\%Hostname%\Microsoft-Windows-Sysmon%%4Operational.evtx" -NewName "%Hostname%-Sysmon.evtx"; Copy-Item \\%Hostname%\C$\WINDOWS\System32\winevt\Logs\Application.evtx -Destination .\Result\%Hostname%\; Rename-Item -Path ".\Result\%Hostname%\Application.evtx" -NewName "%Hostname%-Application.evtx"}"
echo Security and Sysmon logs saved.
echo Get Info about host:
.\PsExec.exe \\%Hostname% cmd /c "(systeminfo & ipconfig /all & tasklist) > C:\tmp\%Hostname%-info-cmd.txt"
.\PsExec.exe \\%Hostname% powershell /c "(systeminfo & ipconfig /all & tasklist) > C:\tmp\%Hostname%-info-cmd.txt"
powershell -Command "& {Copy-Item \\%Hostname%\C$\tmp\%Hostname%-info-cmd.txt -Destination .\Result\%Hostname%\; Remove-Item \\%Hostname%\C$\tmp\%Hostname%-info-cmd.txt}"
.\PsExec.exe \\%Hostname% powershell /c "& { Get-Item -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run; Get-Item -Path HKLM:\SOFTWARE\Microsoft\'Windows NT'\CurrentVersion\IniFileMapping\system.ini\boot; Get-Item -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\'Shell Folders' } | Out-File -FilePath C:\tmp\%Hostname%-registry.txt"
powershell -Command "& {Copy-Item \\%Hostname%\C$\tmp\%Hostname%-registry.txt -Destination .\Result\%Hostname%\; Remove-Item \\%Hostname%\C$\tmp\%Hostname%-registry.txt}"
echo Analyse Security log:
.\hayabusa-2.15.0-win-x64\hayabusa-2.15.0-win-x64.exe csv-timeline --low-memory-mode -f .\Result\%Hostname%\%Hostname%-Security.evtx -o .\Result\%Hostname%\%Hostname%-Security-hayabusa.csv
echo Analyse Sysmon log:
.\hayabusa-2.15.0-win-x64\hayabusa-2.15.0-win-x64.exe csv-timeline --low-memory-mode -f .\Result\%Hostname%\%Hostname%-Sysmon.evtx -o .\Result\%Hostname%\%Hostname%-Sysmon-hayabusa.csv
pause
