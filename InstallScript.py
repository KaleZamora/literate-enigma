import os
import subprocess

print("Welcome to the automated installer, please select an option:\n"
      " 1. Install Office Only\n 2. Install Connectwise Only\n 3. Install BitDefender Only\n 4. Install Applications "
      "Only\n 5. Install All\n 6. Install Connectwise and BitDefender only\n 7. Quit\n 9. Install Applications and Office only")
value = input("What is your selection: ")

if value == "1":
      os.system(r"C:\Util\Project\setup.exe /configure C:\UTIL\Project\Configuration_test.xml")

elif value == "2":
      inst = False
      folder = "ScreenConnect"
      for root in os.walk(r"C:\Program Files (x86)"):
          for name in root:
              if folder not in name:
                  continue
              else:
                  inst = True
      if inst == False:
            os.system(r"msiexec /i C:\UTIL\Project\Agent_Install.msi /qb")

elif value == "3":
      folder2 = "Bitdefender"
      inst = False
      for root in os.walk(r"C:\Program Files"):
          for name in root:
              if folder2 not in name:
                  continue
              else:
                  inst = True
      if inst == False:
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
      inst = False
      folder = "ScreenConnect"
      for root in os.walk(r"C:\Program Files (x86)"):
          for name in root:
              if folder not in name:
                  continue
              else:
                  inst = True
      if inst == False:
            os.system(r"msiexec /i C:\UTIL\Project\Agent_Install.msi /qb")
      folder2 = "Bitdefender"
      inst = False
      for root in os.walk(r"C:\Program Files"):
          for name in root:
              if folder2 not in name:
                  continue
              else:
                  inst = True
      if inst == False:
            os.system(r"msiexec /i C:\UTIL\Project\eps_installer_signed.msi /qb GZ_PACKAGE_ID=aHR0cHM6Ly9jbG91ZC1lY3MuZ3Jhdml0eXpvbmUuYml0ZGVmZW5kZXIuY29tL1BhY2thZ2VzL0JTVFdJTi8wL0RlUkQ0WS9pbnN0YWxsZXIueG1sP2xhbmc9ZW4tVVM=")
      os.system(r"C:\Util\Project\setup.exe /configure C:\UTIL\Project\Configuration_test.xml")
      
elif value == "6":
      inst = False
      folder = "ScreenConnect"
      for root in os.walk(r"C:\Program Files (x86)"):
          for name in root:
              if folder not in name:
                  continue
              else:
                  inst = True
      if inst == False:
            os.system(r"msiexec /i C:\UTIL\Project\Agent_Install.msi /qb")
      folder2 = "Bitdefender"
      inst = False
      for root in os.walk(r"C:\Program Files"):
          for name in root:
              if folder2 not in name:
                  continue
              else:
                  inst = True
      if inst == False:
            os.system(r"msiexec /i C:\UTIL\Project\eps_installer_signed.msi /qb GZ_PACKAGE_ID=aHR0cHM6Ly9jbG91ZC1lY3MuZ3Jhdml0eXpvbmUuYml0ZGVmZW5kZXIuY29tL1BhY2thZ2VzL0JTVFdJTi8wL0RlUkQ0WS9pbnN0YWxsZXIueG1sP2xhbmc9ZW4tVVM=")

elif value == "7":
      print("Goodbye!")
      exit()
      
elif value == "8":
      print("testing network setup")

elif value == "9":
      output_arr = []
      output_arr.append(subprocess.check_output(r"powershell.exe get-appxpackage Microsoft.VCLibs.140.00.UWPDesktop", shell=True))
      output_arr.append(subprocess.check_output(r"powershell.exe get-appxpackage Microsoft.VCLibs.140.00", shell=True))

      for i in output_arr:
            if not i.decode('utf-8'):
                  subprocess.call(r"powershell.exe Add-AppPackage -Path 'C:\UTIL\Project\Microsoft.VCLibs.x64.14.00.Desktop.appx'", shell=True)

      subprocess.call(r"powershell.exe Add-AppPackage -Path 'C:\UTIL\Project\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle'", shell=True)
      subprocess.call(r"powershell.exe winget import --import-file 'C:\UTIL\Project\winstall-9138.json'", shell=True)
      os.system(r"C:\Util\Project\setup.exe /configure C:\UTIL\Project\Configuration_test.xml")
      
else:
      print("You have chosen an invalid number, please relaunch exe and try again")
      exit()
print('Configuring network settings')

#create registry key named private and a dword named autosetup and set it to 0 to prevent windows from setting up network devices
subprocess.call(r"powershell.exe New-Item -Path 'hklm:\SOFTWARE\Microsoft\Windows\CurrentVersion\NcdAutoSetup' -Name 'Private'")
subprocess.call(r"powershell.exe New-ItemProperty 'hklm:\SOFTWARE\Microsoft\Windows\CurrentVersion\NcdAutoSetup\Private' -Name 'AutoSetup' -Value 0 -PropertyType 'DWord'")

#turn off ipv6 for all network adapters
subprocess.call(r"powershell.exe $nic=get-netadapter; Disable-NetAdapterBinding -Name $nic.name -ComponentID ms_tcpip6", shell=True)

#set current network profile to private
subprocess.call(r"powershell.exe $profile=get-netconnectionprofile; Set-NetConnectionProfile -InterfaceAlias $profile.InterfaceAlias -NetworkCategory Private", shell=True)

#powershell commands to add firewall rules to allow network discovery and enable file and printer sharing
subprocess.call(r"powershell.exe netsh advfirewall firewall set rule group='network discovery' new enable=Yes")
subprocess.call(r"powershell.exe netsh advfirewall firewall set rule group='File and Printer Sharing' new enable=Yes")

#key for turning off windows managing default printer
subprocess.call(r"powershell.exe reg add 'HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\Windows' /v LegacyDefaultPrinterMode /t REG_DWORD /d 1 /f", shell=True)

#powershell command to rename computer. uncomment when variable is setup with computer name
current_computer_name=subprocess.call(r"powershell.exe [System.Net.Dns]::GetHostByName($env:computerName).hostname", shell=True)
new_computer_name=input("Please enter the new Computer Name: ")


subprocess.call(r"powershell.exe Rename-Computer -NewName "+new_computer_name,shell=True)

#powershell command to set protocol defaults and file type association defaults for target user. needs variable to hold username, and variable to hold password. dependent on setfta.ps1. must be ran AFTER user creation is completed
#can be cleaned up using variables to hold commands in between semi-colons. 
#currently sets chrome as default, adobe reader, and outlook for target user from admin context. will affect user, not admin.

print("Do you want to create a user?")
yn = input("Y/N: ")
if yn == "Y" or "y":

    subprocess.call(r"powershell.exe set-executionpolicy remotesigned")
    current_computer_name=((subprocess.check_output(r"powershell.exe [System.Net.Dns]::GetHostByName($env:computerName).hostname", shell=True)).decode('utf-8')).strip()
    fname=input("Please enter the user's first name: ")
    lname=input("Please enter the user's last name: ")

    lnamelist=list(lname)
    lnamelist.insert(0, fname[0])

    for i in range(len(lnamelist)):
        lnamelist[i]=lnamelist[i].lower()

    username="".join(map(str, lnamelist))
    subprocess.call(r"powershell.exe Write-Host 'Please enter their password: '; $password=Read-Host -assecurestring; "
        r"New-LocalUser "+ username + " -Password $password -FullName '" + fname + " " + lname + "'; Add-LocalGroupMember -Group 'Users' -Member " + username + ";"
        r"start-process powershell.exe -argumentlist 'import-module c:\util\project\setfta.ps1; set-pta chromehtml http; set-pta chromehtml https; set-fta AcroExch.Document.DC .pdf; set-pta Outlook.URL.mailto.15 mailto; set-fta chromehtml .html'"
        r" -Credential (New-Object System.Management.Automation.PSCredential " + str(current_computer_name)+"\\"+username+",$password)", shell=True)


elif yn == "N" or "n":
      print("User creation skipped")
else:
      print("Invalid Response, skipping user creation.")
