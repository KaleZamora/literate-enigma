#subprocess is for calling powershell and start process. 
#os is for cmd prompt calls
#glob is for using wildcards and other regex like features
#getpass is used to get a password from stdin but block it out for privacy

import subprocess
import os
import glob
from getpass import getpass
import ctypes
import re
import sys


dirname = os.getcwd()

#folder is assigned the path to screenconnect client but with a wildcard symbol (*). glob then treats that as a wildcard, searches the directory for anything matching screen connect client and reports the output.
#if nothing matches the query, the next step is to install the agent.

def agent_install():
    folder="C:\Program Files (x86)\ScreenConnect Client*"
    
    if not glob.glob(folder,recursive=False):
        os.system(r"msiexec /i " + dirname + "\Agent_Install.msi /qb") 

#same as before, check the directory to see if it exists, if not, install the program. Needs an else        
def bitdefender_install():
    folder="C:\Program Files\Bitdefender"
    if not os.path.isdir(folder):
        file_target = "setupdownloader*"
        results = glob.glob(file_target)
        info = re.search("\[" + "(.+?)" + "\]", results[0]).group(1)
        os.system(r"msiexec /i " + dirname + "\eps_installer_signed.msi /qb GZ_PACKAGE_ID=" + info)

#vclibs is a dependancy of winget. globs reports how many instances of vclibs exist and if it's less than the necessary 4, we install vclibs followed by winget and then followed by all the programs winget installs.
def applications_install():
    folder="C:\Program Files\WindowsApps\Microsoft.VCLibs*"
    
    if len(glob.glob(folder,recursive=False)) < 4:
        subprocess.call(r"powershell.exe Add-AppPackage -Path '" + dirname + "\Microsoft.VCLibs.x64.14.00.Desktop.appx'", shell=True)
    subprocess.call(r"powershell.exe Add-AppPackage -Path '" + dirname + "\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle'", shell=True)
    subprocess.call(r"powershell.exe winget install --id=Oracle.JavaRuntimeEnvironment; winget install --id=Google.Chrome; winget install --id=Mozilla.Firefox; winget install --id=Microsoft.RemoteDesktopClient; winget install --id=Adobe.AdobeAcrobatReaderDC; winget install --id=JAMSoftware.TreeSizeFree", shell=True)

#call to cmd to run setup.exe to install office by first downloading the files and then installing them.
def office_install():
    os.system(dirname + r"\setup.exe /configure " + dirname + "\Configuration_test.xml")
    
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
    subprocess.call(r"powershell.exe Rename-Computer -NewName '"+new_computer_name+"'",shell=True)

#function to setup user through powershell calls after getting info from user via stdin. the name is converted into the format required (eg gherrera). it's then added to a group (either standard or admin).
# !! must be able to specify if it's a standard user or an admin user !!
#This part here also gives powershell the ability to run scripts that are unsigned because it will be running a script later via task scheduler by itself without python
#the username won't appear in the login shell until you reboot the computer.
#it returns the username and password as a tuple which gets sent into apply_defaults
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
    flag = 1

    while flag != 0:

        yn = input("Do you want to make this user an administrator? Y/N: ").lower()
        if yn == "y":
            subprocess.call("powershell.exe AddLocalGroupMember -Group 'Administrators' -Member '" +username+ "'")
            flag = 0
        elif yn == "n":
            print("Skipping admin elevation...")
            flag = 0
        else:
            print("Invalid choice. Please try again...")
    return username,pass_key

#this is a mess, but the gist of it is this: we get the computername to append it to the username and add a forward slash (eg WORKSTATION3\gherrera) in order to create a scheduled task that runs on login that runs a script that sets defaults how we want them to.
#defaults here meaning use adobe for default pdf reader, use chrome for html, use outlook for mail.to items etc. 
#currently, windows fights back and resets defaults on occasion for arbitrary reasons.
def apply_defaults(username):

    current_computer_name=((subprocess.check_output(r"powershell.exe [System.Net.Dns]::GetHostByName($env:computerName).hostname", shell=True)).decode('utf-8')).strip()
    action=r"(New-ScheduledTaskAction -execute powershell.exe -Argument " + dirname + "\defaultsetup.ps1)"
    trigger=r"(New-ScheduledTaskTrigger -atlogon)"
    credentials=r"-Credential (New-Object System.Management.Automation.PSCredential " +str(current_computer_name)+"\\"+str(username[0])+",(ConvertTo-SecureString " +str(username[1])+ " -AsPlainText -Force))"
    principal=r"(New-ScheduledTaskPrincipal -UserId "+username[0]+" -LogonType ServiceAccount)"
    arguments=r"register-scheduledtask -action "+action+" -trigger "+trigger+" -principal "+principal+" -taskname User_Defaults -taskpath defaults -description fta_scheduled_task"
    
    subprocess.call(r"powershell.exe start-process powershell.exe -argumentlist '"+arguments+"' ", shell=True)
    
    
def menu():
    choices = ['1','2','3','4','5','6','7','8','9']
    chances = 1
    value = 0
    while chances != 0:
        print("Welcome to the automated installer, please select an option:\n"
        " 1. Install Office Only\n 2. Install Connectwise Only\n 3. Install BitDefender Only\n 4. Install Applications "
        "Only\n 5. Install All\n 6. Install Connectwise and BitDefender only\n 7. Quit\n 9. Install Applications and Office only")
        value = input("What is your selection: ")
        if value in choices:
            chances=0
        else:
            print("Incorrect choice. Please try again...")
    return value

#simple string of calls to powershell to run powercfg. need to supress output or redirect it to a log or some such.
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

#ctypes is used here to check to see if the user is running the program as admin. Need to stdout a message that tells the user to try again as admin.
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

#default network settings are applied.
def netmenu():
    flag=1
    #chances = 4
    while flag != 0:
        yn=input("Do you want to configure the network settings? Y/N: ").lower()
        #chances = chances - 1
        if yn == "y":
            print('Configuring network settings')
            network_settings()
            flag=0
        elif yn == "n":
            print("Skipping network configuration...")
            flag=0
        #elif chances == 0:
        #    print('You have responded incorrectly too many time, the program will now skip configuring network settings')
        #    print("Skipping network configuration...")
        #    break
        else:
            print("Invalid choice. Please try again...")
            #print("you have made an incorrect choice, please chose again, you have " + str(chances) + " chances remaining")
    #return yn
#power settings are applied.
def powermenu():
    flag=1
    while flag != 0:
        #chances = chances - 1
        yn = input("Do you want to configure the power settings? Y/N: ").lower()
        if yn == "y":
            print("Configuring power settings...")
            powersettings()
            flag=0
        elif yn == "n":
            print("Skipping power settings.")
            flag=0
        #else:
        #    print('You have responded incorrectly too many time, the program will now skip configuring power settings')
        #    print("Skipping power settings.")
        #    break
        else:
            print("Invalid choice. Please try again...")
#apply defaults is chained with create user. whatever create user returns is sent to apply defaults
def usermenu():
    flag=1
    while flag != 0:
        #chances = chances - 1
        yn = input("Do you want to create a user? Y/N: ").lower()
        if yn == "y":
            apply_defaults(create_user())
            flag=0
        elif yn == "n":
            print("Skipping user creation...")
            flag=0
        #elif chances == 0:
        #    print('You have responded incorrectly too many time, the program will now skip creating a user')
        #    print("Skipping user creation...")
        #    break
        else:
            print("Invalid choice. Please try again...")
#function to rename the computer. first it asks for a new name and then it calls on powershell to change it.
def comp_name_menu():
    flag=1
    while flag != 0:
        #chances = chances - 1
        yn = input("Do you want to rename the machine? Y/N: ").lower()
        if yn == "y":
            new_computer_name=input("Please enter the new Computer Name: ")
            subprocess.call(r"powershell.exe Rename-Computer -NewName '"+new_computer_name+"'",shell=True)
            flag=0
        elif yn == "n":
            print("Skipping computer rename...")
            flag=0
        #elif chances == 0:
        #    print('You have responded incorrectly too many time, the program will now skip renaming the machine')
        #    print("Skipping computer rename...")
        #    break
        else:
            print("Invalid choice. Please try again..")

def restart_menu():
    flag = 1
    while flag != 0:
        yn = input("Would you like to restart now? Y/N: ").lower()
        if yn == "y":
            print("Restarting in 30 seconds.")
            subprocess.call("shutdown -r -t 0030")
            flag = 0
        elif yn == "n":
            print("Skipping restart...")
            flag = 0
        else:
            print("Invalid choice. Please try again..")
            
def myexcepthook(type, value, traceback, oldhook=sys.excepthook):
    oldhook(type, value, traceback)
    input("Press RETURN. ")    # use input() in Python 3.x
