#!/usr/bin/python

import json
import sys


inputFile = open(sys.argv[1], "r")
outputfile = open(sys.argv[2], "w")
outputfile2 = open("extern-" + sys.argv[2], "w")
variableNames = []
externDefinitions = []

try:
    pluginMap = json.loads(inputFile.read())
except ValueError as e:
    print " --> Error loading input file \"%s\"" % (sys.argv[1])
    print "     %s" % (e)
    exit -1


def writePluginInfo(line):
    outputfile.write("%s\n" % line)


def writeExternPluginInfo(line):
    outputfile2.write("%s\n" % line)


def extractVendors(pluginMap):
    for vendor in pluginMap['vendors']:
        try:
            print("define VendorId %sVendorId = %s" % (pluginMap["idName"], vendor["id"]))
            writePluginInfo("VendorId %sVendorId = VendorId(\"%s\");" % (vendor["idName"], vendor["id"]))
            createExternDefinition("VendorId", "%sVendorId" % (vendor["idName"]))
        except:
            pass
        extractDeviceClasses(vendor)


def extractDeviceClasses(vendorMap):
    for deviceClass in vendorMap["deviceClasses"]:
        try:
            variableName = "%sDeviceClassId" % (deviceClass["idName"]) 
            if not variableName in variableNames:
                variableNames.append(variableName)
                print("define DeviceClassId %s = %s" % (variableName, deviceClass["deviceClassId"]))
                writePluginInfo("DeviceClassId %s = DeviceClassId(\"%s\");" % (variableName, deviceClass["deviceClassId"]))
                createExternDefinition("DeviceClassId", variableName)
            else:
                print("duplicated variable name \"%s\" for DeviceClassId %s -> skipping") % (variableName, deviceClass["deviceClassId"])
        except:
            pass
        extractActionTypes(deviceClass)
        extractStateTypes(deviceClass)
        extractEventTypes(deviceClass)


def extractStateTypes(deviceClassMap):
    try:
        for stateType in deviceClassMap["stateTypes"]:
            try:
                variableName = "%sStateTypeId" % (stateType["idName"])
                if not variableName in variableNames:
                    variableNames.append(variableName)
                    print("define StateTypeId %s = %s" % (variableName, stateType["id"]))
                    writePluginInfo("StateTypeId %s = StateTypeId(\"%s\");" % (variableName, stateType["id"]))
                    createExternDefinition("StateTypeId", variableName)
                else:
                    print("duplicated variable name \"%s\" for StateTypeId %s -> skipping") % (variableName, stateType["id"])
                # create ActionTypeId if the state is writable
                if 'writable' in stateType:
                    vName = "%sActionTypeId" % (stateType["idName"]) 
                    if not vName in variableNames:
                        variableNames.append(vName)
                        print("define ActionTypeId %s for writable StateType %s = %s" % (vName, variableName, stateType["id"]))
                        writePluginInfo("ActionTypeId %s = ActionTypeId(\"%s\");" % (vName, stateType["id"]))
                        createExternDefinition("ActionTypeId", vName)
                    else:
                        print("duplicated variable name \"%s\" for ActionTypeId %s -> skipping") % (variableName, stateType["id"])
            except:
                pass
    except:
        pass


def extractActionTypes(deviceClassMap):
    try:
        for actionType in deviceClassMap["actionTypes"]:
            try:
                variableName = "%sActionTypeId" % (actionType["idName"])
                if not variableName in variableNames:
                    variableNames.append(variableName)
                    writePluginInfo("ActionTypeId %s = ActionTypeId(\"%s\");" % (variableName, actionType["id"]))
                    createExternDefinition("ActionTypeId", variableName)
                else:
                    print("duplicated variable name \"%s\" for ActionTypeId %s -> skipping") % (variableName, actionType["id"])
            except:
                pass
    except:
        pass


def extractEventTypes(deviceClassMap):
    try:
        for eventType in deviceClassMap["eventTypes"]:
            try:
                variableName = "%sEventTypeId" % (eventType["idName"])
                if not variableName in variableNames:
                    variableNames.append(variableName)
                    writePluginInfo("EventTypeId %s = EventTypeId(\"%s\");" % (variableName, eventType["id"]))
                    createExternDefinition("EventTypeId", variableName)                    
                else:
                    print("duplicated variable name \"%s\" for EventTypeId %s -> skipping") % (variableName, eventType["id"])
            except:
                pass
    except:
        pass

def createExternDefinition(type, name):
    definition = {}
    definition['type'] = type
    definition['variable'] = name
    externDefinitions.append(definition)


##################################################################################################################
# write plugininfo.h
print " --> generate plugininfo.h"
print "PluginId for plugin \"%s\" = %s" %(pluginMap['name'], pluginMap['id'])
    
writePluginInfo("/* This file is generated by the guh build system. Any changes to this file will")
writePluginInfo(" * be lost.")
writePluginInfo(" *")
writePluginInfo(" * If you want to change this file, edit the plugin's json file and add")
writePluginInfo(" * idName tags where appropriate.")
writePluginInfo(" */")
writePluginInfo("")
writePluginInfo("#ifndef PLUGININFO_H")
writePluginInfo("#define PLUGININFO_H")
writePluginInfo("#include \"typeutils.h\"")
writePluginInfo("#include <QLoggingCategory>")
writePluginInfo("")
writePluginInfo("// Id definitions")
writePluginInfo("PluginId pluginId = PluginId(\"%s\");" % pluginMap['id'])

extractVendors(pluginMap)
writePluginInfo("")
writePluginInfo("// Loging category")

if 'idName' in pluginMap:
    writePluginInfo("Q_DECLARE_LOGGING_CATEGORY(dc%s)" % pluginMap['idName'])
    writePluginInfo("Q_LOGGING_CATEGORY(dc%s, \"%s\")" % (pluginMap['idName'], pluginMap['idName']))
    print "define logging category: \"dc%s\"" % pluginMap['idName']
    
writePluginInfo("")
writePluginInfo("#endif // PLUGININFO_H")
print " --> generated successfully \"%s\"" % sys.argv[2] 


##################################################################################################################
# write extern-plugininfo.h 
print " --> generate extern-plugininfo.h"
writeExternPluginInfo("/* This file is generated by the guh build system. Any changes to this file will")
writeExternPluginInfo(" * be lost.")
writeExternPluginInfo(" *")
writeExternPluginInfo(" * If you want to change this file, edit the plugin's json file and add")
writeExternPluginInfo(" * idName tags where appropriate.")
writeExternPluginInfo(" */")
writeExternPluginInfo("")
writeExternPluginInfo("#ifndef EXTERNPLUGININFO_H")
writeExternPluginInfo("#define EXTERNPLUGININFO_H")
writeExternPluginInfo("#include \"typeutils.h\"")
writeExternPluginInfo("#include <QLoggingCategory>")
writeExternPluginInfo("")
writeExternPluginInfo("// Id definitions")

for externDefinition in externDefinitions:
    writeExternPluginInfo("extern %s %s;" % (externDefinition['type'], externDefinition['variable']))

writeExternPluginInfo("")
writeExternPluginInfo("// Logging category definition")

if 'idName' in pluginMap:
    writeExternPluginInfo("Q_DECLARE_LOGGING_CATEGORY(dc%s)" % pluginMap['idName'])
    
writeExternPluginInfo("")
writeExternPluginInfo("#endif // EXTERNPLUGININFO_H")

print " --> generated successfully \"extern-%s\"" % (sys.argv[2])