import subprocess
import os
import glob
from getpass import getpass
from winreg import *
import ctypes

def agent_install():
    folder="C:\Program Files (x86)\ScreenConnect Client*"
    if not glob.glob(folder,recursive=False):
        os.system(r"msiexec /i C:\UTIL\Project\Agent_Install.msi /qb") 
        
def bitdefender_install():
    folder="C:\Program Files\Bitdefender"
    if not os.path.isdir(folder):
        os.system(r"msiexec /i C:\UTIL\Project\eps_installer_signed.msi /qb GZ_PACKAGE_ID=aHR0cHM6Ly9jbG91ZC1lY3MuZ3Jhdml0eXpvbmUuYml0ZGVmZW5kZXIuY29tL1BhY2thZ2VzL0JTVFdJTi8wL0RlUkQ0WS9pbnN0YWxsZXIueG1sP2xhbmc9ZW4tVVM=")

def applications_install():
    folder="C:\Program Files\WindowsApps\Microsoft.VCLibs*"
    
    if not glob.glob(folder,recursive=False):
        subprocess.call(r"powershell.exe Add-AppPackage -Path 'C:\UTIL\Project\Microsoft.VCLibs.x64.14.00.Desktop.appx'", shell=True)
    #output_arr = []
    ##output_arr.append(subprocess.check_output(r"powershell.exe get-appxpackage Microsoft.VCLibs.140.00.UWPDesktop", shell=True))
    #output_arr.append(subprocess.check_output(r"powershell.exe get-appxpackage Microsoft.VCLibs.140.00", shell=True))

    #for i in output_arr:
    #    if not i.decode('utf-8'):
    #        subprocess.call(r"powershell.exe Add-AppPackage -Path 'C:\UTIL\Project\Microsoft.VCLibs.x64.14.00.Desktop.appx'", shell=True)

    subprocess.call(r"powershell.exe Add-AppPackage -Path 'C:\UTIL\Project\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle'", shell=True)
    subprocess.call(r"powershell.exe winget install --id=Oracle.JavaRuntimeEnvironment; winget install --id=Google.Chrome; winget install --id=Mozilla.Firefox; winget install --id=Microsoft.RemoteDesktopClient; winget install --id=Adobe.AdobeAcrobatReaderDC; winget install --id=JAMSoftware.TreeSizeFree", shell=True)

def office_install():
    os.system(r"C:\Util\Project\setup.exe /configure C:\UTIL\Project\Configuration_test.xml")
    
def network_settings():
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

def computer_rename():
    #powershell command to rename computer. uncomment when variable is setup with computer name
    #current_computer_name=subprocess.call(r"powershell.exe [System.Net.Dns]::GetHostByName($env:computerName).hostname", shell=True)
    new_computer_name=input("Please enter the new Computer Name: ")
    subprocess.call(r"powershell.exe Rename-Computer -NewName "+new_computer_name,shell=True)

def create_user():
    subprocess.call(r"powershell.exe Set-ExecutionPolicy RemoteSigned -Scope LocalMachine -Force")
    fname=input("Please enter the user's first name: ")
    lname=input("Please enter the user's last name: ")

    lnamelist=list(lname)
    lnamelist.insert(0, fname[0])

    for i in range(len(lnamelist)):
        lnamelist[i]=lnamelist[i].lower()

    username="".join(map(str, lnamelist))
    pass_key=getpass("Please enter the user's password: ")
    subprocess.call(r"powershell.exe New-LocalUser "+ username + " -Password (ConvertTo-SecureString " +pass_key+ " -AsPlainText -Force) -FullName '" + fname + " " + lname + "'; Add-LocalGroupMember -Group 'Users' -Member " + username + ";",shell=True)
    return username,pass_key

def apply_defaults(username):
    current_computer_name=((subprocess.check_output(r"powershell.exe [System.Net.Dns]::GetHostByName($env:computerName).hostname", shell=True)).decode('utf-8')).strip()
    action=r"(New-ScheduledTaskAction -execute powershell.exe -Argument c:\util\project\defaultsetup.ps1)"
    trigger=r"(New-ScheduledTaskTrigger -atlogon)"
    credentials=r"-Credential (New-Object System.Management.Automation.PSCredential " +str(current_computer_name)+"\\"+str(username[0])+",(ConvertTo-SecureString " +str(username[1])+ " -AsPlainText -Force))"
    principal=r"(New-ScheduledTaskPrincipal -UserId "+username[0]+" -LogonType ServiceAccount)"
    arguments=r"register-scheduledtask -action "+action+" -trigger "+trigger+" -principal "+principal+" -taskname pls -taskpath defaults -description fta_scheduled_task"#; get-scheduledtask pls"
    
    subprocess.call(r"powershell.exe start-process powershell.exe -argumentlist '"+arguments+"' ", shell=True)
    
    #aKey = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
    #aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    #store1 = 0
    #store2 = 0
    #aKey = OpenKey(aReg, aKey)
    #for i in range(10):
    #    asubkey_name = EnumKey(aKey, i)
    #    print(asubkey_name)
    #    asubkey = OpenKey(aKey, asubkey_name)
    #    print(asubkey)
    #    val = QueryValueEx(asubkey, r"ProfileImagePath")
    #    store = str(val)
    #    if username in store:
    #        store2 = str(asubkey_name)

    #subprocess.call("powershell.exe REG LOAD HKEY_USERS\\" +store2+ r" 'C:\Users\\" +username+ r"NTUSER.DAT'; " + "New-Item 'Registry::HKEY_USERS\\" + store2 + r"\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce'")
    #subprocess.call("powershell.exe REG LOAD HKEY_USERS\\" +store2+ r" 'C:\Users\\" +username+ r"NTUSER.DAT'; " + "Set-ItemProperty 'Registry::HKEY_USERS\\" + store2 + r"\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce' -Name 'DefaultSetup' -Value 'C:\UTIL\Project\defaultsetup.ps1' -Type 'String'")
    #subprocess.call("powershell.exe REG UNLOAD HKEY_USERS\\" +store2)
    
def menu():
    choices = ['1','2','3','4','5','6','7','8','9']
    chances = 4
    value = 0
    while chances != 0:
        chances = chances - 1
        print("Welcome to the automated installer, please select an option:\n"
        " 1. Install Office Only\n 2. Install Connectwise Only\n 3. Install BitDefender Only\n 4. Install Applications "
        "Only\n 5. Install All\n 6. Install Connectwise and BitDefender only\n 7. Quit\n 9. Install Applications and Office only")
        value = input("What is your selection: ")
        if value in choices:
            break
        elif chances == 0:
            print('You have responded incorrectly too many time, the program will now exit, please re-run the program and try again')
            exit()
        else:
            print("you have made an incorrect choice, please chose again, you have " + str(chances) + " chances remaining")
    return value

def powersettings():
    subprocess.call("powercfg /x monitor-timeout-ac 0")
    subprocess.call("powercfg /x monitor-timeout-dc 0")
    subprocess.call("powercfg /x disk-timeout-ac 0")
    subprocess.call("powercfg /x disk-timeout-dc 0")
    subprocess.call("powercfg /x standby-timeout-ac 0")
    subprocess.call("powercfg /x standby-timeout-dc 0")
    subprocess.call("powercfg /x hibernate-timeout-ac 0")
    subprocess.call("powercfg /x hibernate-timeout-dc 0")
    subprocess.call("powercfg /x processor-throttle-ac none")
    subprocess.call("powercfg /x processor-throttle-dc none")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

