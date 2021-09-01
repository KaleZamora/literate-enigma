import os
import subprocess

print("Welcome to the automated installer, please select an option:\n"
      " 1. Install Office Only\n 2. Install Connectwise Only\n 3. Install BitDefender Only\n 4. Install Applications "
      "Only\n 5. Install All\n 6. Install Connectwise and BitDefender only\n 7. Quit")
value = input("What is your selection: ")

if value == "1":
      os.system(r"C:\Util\Project\setup.exe /configure C:\UTIL\Project\Configuration_test.xml")

elif value == "2":
      os.system(r"msiexec /i C:\UTIL\Project\Agent_Install.msi /qb")

elif value == "3":
      os.system(r"msiexec /i C:\UTIL\Project\eps_installer_signed.msi /qb GZ_PACKAGE_ID=aHR0cHM6Ly9jbG91ZC1lY3MuZ3Jhdml0eXpvbmUuYml0ZGVmZW5kZXIuY29tL1BhY2thZ2VzL0JTVFdJTi8wL0RlUkQ0WS9pbnN0YWxsZXIueG1sP2xhbmc9ZW4tVVM=")

elif value == "4":
      output_arr = []
      output_arr.append(subprocess.check_output(r"powershell.exe get-appxpackage Microsoft.VCLibs.140.00.UWPDesktop", shell=True))
      output_arr.append(subprocess.check_output(r"powershell.exe get-appxpackage Microsoft.VCLibs.140.00", shell=True))

      for i in output_arr:
            if not i.decode('utf-8'):
                  subprocess.call(r"powershell.exe Add-AppPackage -Path 'C:\UTIL\Project\Microsoft.VCLibs.x64.14.00.Desktop.appx'", shell=True)

      subprocess.call(r"powershell.exe Add-AppPackage -Path 'C:\UTIL\Project\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle'", shell=True)
      subprocess.call(r"powershell.exe winget import --import-file 'C:\UTIL\Project\winstall-9138.json'", shell=True)

elif value == "5":
      output_arr = []
      output_arr.append(subprocess.check_output(r"powershell.exe get-appxpackage Microsoft.VCLibs.140.00.UWPDesktop", shell=True))
      output_arr.append(subprocess.check_output(r"powershell.exe get-appxpackage Microsoft.VCLibs.140.00", shell=True))

      for i in output_arr:
            if not i.decode('utf-8'):
                  subprocess.call(r"powershell.exe Add-AppPackage -Path 'C:\UTIL\Project\Microsoft.VCLibs.x64.14.00.Desktop.appx'", shell=True)

      subprocess.call(r"powershell.exe Add-AppPackage -Path 'C:\UTIL\Project\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle'", shell=True)
      subprocess.call(r"powershell.exe winget import --import-file 'C:\UTIL\Project\winstall-9138.json'", shell=True)
      os.system(r"msiexec /i C:\UTIL\Project\Agent_Install.msi /qb")
      os.system(r"msiexec /i C:\UTIL\Project\eps_installer_signed.msi /qb GZ_PACKAGE_ID=aHR0cHM6Ly9jbG91ZC1lY3MuZ3Jhdml0eXpvbmUuYml0ZGVmZW5kZXIuY29tL1BhY2thZ2VzL0JTVFdJTi8wL0RlUkQ0WS9pbnN0YWxsZXIueG1sP2xhbmc9ZW4tVVM=")
      os.system(r"C:\Util\Project\setup.exe /configure C:\UTIL\Project\Configuration_test.xml")

elif value == "6":
      os.system(r"msiexec /i C:\UTIL\Project\Agent_Install.msi /qb")
      os.system(r"msiexec /i C:\UTIL\Project\eps_installer_signed.msi /qb GZ_PACKAGE_ID=aHR0cHM6Ly9jbG91ZC1lY3MuZ3Jhdml0eXpvbmUuYml0ZGVmZW5kZXIuY29tL1BhY2thZ2VzL0JTVFdJTi8wL0RlUkQ0WS9pbnN0YWxsZXIueG1sP2xhbmc9ZW4tVVM=")

elif value == "7":
      print("Goodbye!")

else:
      print("You have chosen an invalid number, please relaunch exe and try again")
