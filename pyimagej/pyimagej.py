import subprocess
import threading
import ctk_cli


class RunCmd(threading.Thread):
    '''RunCmd Class
        This class allow for running a command line program using threads
        Also implement a timeout option that allow for killing the process if
        it takes longer than timeout
    '''

    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = subprocess.Popen(self.cmd)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.kill()      #use self.p.terminate() if process dont needs a kill -9
            self.join()

class ImageJ(object):
    '''imagej Class
        This class is an abstraction for an instance of ImageJ
        It allows for calling macros from a python script
    '''

    def __init__(self, imagej_exe):
        try:
            assert imagej_exe != ''
        except:
            print "[ERROR]: ImageJ path is empty"
        self._executable = imagej_exe

    def runImageJMacro(self, macroPath, macroParams, timeout = 60, macroName = 'Macro'):
        '''Run a ImageJ Macro using command line

        Keyword arguments:
        macroPath                      -- Path to macro file *.ijm (mandatory)
        macroParams                    -- Parameters that the macro uses (mandatory)
        msgOpt [\'Running Macro ...\'] -- Message for debugging the will be shown when macro is running

        '''

        cmdline = self._executable + ' --no-splash -macro  \"' + macroPath + '\" \"' + macroParams + '\"'

        RunCmd(cmdline, timeout).Run()

class MacroImageJ(ImageJ):
    '''macroImageJ Class
        This class is an abstraction for an instance of an imagej macro
        It allows for calling macros from a python script.
        Uses ctk_cli XML standard for the description of the inputs parameters of the macro
    '''

    def __init__(self, imagejPath, macroPath, xmlDefinition, defaultTimeout = 60):
        super(MacroImageJ, self).__init__(imagejPath)
        self._macroPath = macroPath
        self._xmlDefinition = xmlDefinition
        self.readXmlDefinition()
        self.defaultTimeout = defaultTimeout

    def readXmlDefinition(self):
        '''Read the XML definition and creates the dictionary for the parameters of the macro'''
        #print "Reading xml macro description"
        self._CLImodule = ctk_cli.CLIModule(self._xmlDefinition)
        (arguments, options, outputs) =  self._CLImodule.classifyParameters()

        self._NumParameters = len(options)

        for e in options:
            e.flag = e.flag[1::] # delete the '-' symbol before parameter flag
            if(e.default == None):
                e.index = True
            else:
                e.index = False

        self._XMLparameters = options
        self._paramDictionary = {}
        for param in self._XMLparameters:
            self._paramDictionary[param.flag] = [param.index,param.default]
            #print "    -Reading... (", param.flag, ")"

        return

    def printArgs(self):
        '''Print information about the macro call'''
        for param in self._paramDictionary:
            if(self._paramDictionary[param][0]):
                print "    -", param, ": ", self._paramDictionary[param][1], " (required)"
            else:
                print "    -", param, ": ", self._paramDictionary[param][1]

    def printArgsInfo(self):
        '''Prints complete description about the macro'''
        print "Macro         :[", self._CLImodule.title, "]"
        print "Description   :", self._CLImodule.description
        print "Category      :", self._CLImodule.category
        print "Author        :", self._CLImodule.contributor
        print "Parameters    :"
        for e in self._XMLparameters:
            if(e.index):
                print "    -",e.flag, " [", e.default ,"] (required)", e.description
            else:
                print "    -",e.flag, " [", e.default ,"]", e.description

    def runMacro(self, **kwargs):
        '''Run the macro'''
        #print "#########################################################"
        #print "               ",self._CLImodule.title
        #print "#########################################################"

        readyForRun = False

        #Read arguments
        for paramName in kwargs.keys():
            self._paramDictionary[paramName][1] = kwargs[paramName]

        #self.printArgs()
        #print "#########################################################"



        # Prepare macroParams string
        macroParams = ''
        for param in self._paramDictionary:
            macroParams = macroParams + "-" + param + " " + str(self._paramDictionary[param][1]) + " "

        self.runImageJMacro( macroPath = self._macroPath , macroParams = macroParams, timeout = self.defaultTimeout, macroName = self._CLImodule.title)

        paramsReturn = {}
        for param in self._paramDictionary:
            paramsReturn[param] = self._paramDictionary[param][1]

        return paramsReturn

    def runMacroData(self, **kwargs):
        '''Run the macro fake, for testing'''
        #print "#########################################################"
        #print "               ",self._CLImodule.title
        #print "#########################################################"

        readyForRun = False

        #Read arguments
        for paramName in kwargs.keys():
            self._paramDictionary[paramName][1] = kwargs[paramName]

        #self.printArgs()
        #print "#########################################################"

        # Prepare macroParams string
        macroParams = ''
        for param in self._paramDictionary:
            macroParams = macroParams + "-" + param + " " + str(self._paramDictionary[param][1]) + " "

        paramsReturn = {}
        for param in self._paramDictionary:
            paramsReturn[param] = self._paramDictionary[param][1]

        return paramsReturn
