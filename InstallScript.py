import subprocess


subprocess.call(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe Add-AppPackage -Path 'C:\UTIL\Project\Microsoft.VCLibs.x64.14.00.Desktop.appx'", shell=True)    
subprocess.call(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe Add-AppPackage -Path 'C:\\UTIL\\Project\\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle'", shell=True)
subprocess.call(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe winget import --import-file C:\\UTIL\\Project\\winstall-2557.json", shell=True)
subprocess.call(r"powershell.exe msiexec /i C:\UTIL\Project\Agent_Install.msi /qb")
subprocess.call(r"powershell.exe msiexec /i C:\UTIL\Project\eps_installer_signed.msi /qb GZ_PACKAGE_ID=aHR0cHM6Ly9jbG91ZC1lY3MuZ3Jhdml0eXpvbmUuYml0ZGVmZW5kZXIuY29tL1BhY2thZ2VzL0JTVFdJTi8wL0RlUkQ0WS9pbnN0YWxsZXIueG1sP2xhbmc9ZW4tVVM=")
