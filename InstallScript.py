import definitions
import ctypes
import sys

if definitions.is_admin():
    value = definitions.menu()

    if value == "1":
        definitions.office_install()

    elif value == "2":
        definitions.agent_install()    

    elif value == "3":
        definitions.bitdefender_install()

    elif value == "4":
        definitions.applications_install()
      
    elif value == "5":
        definitions.applications_install()
        definitions.agent_install()
        definitions.bitdefender_install()
        definitions.office_install()
      
    elif value == "6":
        definitions.agent_install()
        definitions.bitdefender_install()
    
    elif value == "7":
        print("Goodbye!")
        exit()
      
    elif value == "8":
        print("testing network setup")

    elif value == "9":
        definitions.applications_install()
        definitions.office_install()
      

    yn = input("Do you want to configure the network settings? Y/N: ")
    if yn.lower() == "y":
        print('Configuring network settings')
        definitions.network_settings()

    else:
        print("Skipping network configuration...")

    power = input("Do you want to configure power settings? Y/N: ")
    if power.lower() == "y":
        print("Configuring power settings...")
        definitions.powersettings()
        
    else:
        print("Skipping power settings.")

    #powershell command to set protocol defaults and file type association defaults for target user. needs variable to hold username, and variable to hold password. dependent on setfta.ps1. must be ran AFTER user creation is completed
    #can be cleaned up using variables to hold commands in between semi-colons. 
    #currently sets chrome as default, adobe reader, and outlook for target user from admin context. will affect user, not admin.

    #        r"start-process powershell.exe -argumentlist 'import-module c:\util\project\setfta.ps1; set-pta chromehtml http; set-pta chromehtml https; set-fta AcroExch.Document.DC .pdf; set-pta Outlook.URL.mailto.15 mailto; set-fta chromehtml .html'"
    #        r" -Credential (New-Object System.Management.Automation.PSCredential " + str(current_computer_name)+"\\"+username+",$password)", shell=True)

    yn = input("Do you want to create a user? Y/N: ")
    if yn.lower() == "y":    
        definitions.apply_defaults(definitions.create_user())
    
    else:
        print("Skipping user creation...")



else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
