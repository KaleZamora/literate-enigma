import definitions

print("Welcome to the automated installer, please select an option:\n"
      " 1. Install Office Only\n 2. Install Connectwise Only\n 3. Install BitDefender Only\n 4. Install Applications "
      "Only\n 5. Install All\n 6. Install Connectwise and BitDefender only\n 7. Quit\n 9. Install Applications and Office only")
value = input("What is your selection: ")    
    
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
      
else:
      print("You have chosen an invalid number, please relaunch exe and try again")
      exit()

yn = input("Do you want to configure the network settings? Y/N: ")
if yn.lower() == "y":
    print('Configuring network settings')
    definitions.network_settings()

else:
    print("Skipping network configuration...")

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

