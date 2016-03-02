#@author Sagar Makwana

#---------------------------------------Function Definitions------------------------------------------------

#Converts the given rule from the input KNOWLEDGE BASE to standard dictionary format.
def convertRuleToDict(rule):
    #The dictionary that is to be returned after converting the rule into dictionary.
    ruleDict = ''

    implicationSplit = rule.split(' => ')

    #If it is a complex sentence
    if len(implicationSplit) == 2:
        #Premise Section
        conjunctionSplit = implicationSplit[0].split(" && ")
        ruleDict = {'premiseCount':len(conjunctionSplit)}

        for i in range(0,len(conjunctionSplit)):
            premise = conjunctionSplit[i].strip()

            if premise[0] == '~':
                ruleDict['premise'+str(i+1)] = {'not': True}
                premise = premise[1:]
            else:
                ruleDict['premise'+str(i+1)] = {'not': False}

            name = premise[0:premise.index('(')]
            variables = premise[premise.index('(')+1:premise.index(')')]
            variables = variables.split(',')
            for l in range (0,len(variables)):
                variables[l] = variables[l].strip()
            varCount = len(variables)

            ruleDict['premise'+str(i+1)]['varCount'] = varCount
            ruleDict['premise'+str(i+1)]['variables'] = variables
            ruleDict['premise'+str(i+1)]['variableSubs'] = variables[:]
            ruleDict['premise'+str(i+1)]['name'] = name

        #Conclusion Section
        conclusion = implicationSplit[1].strip()

        if conclusion[0] == '~':
            ruleDict['conclusion'] = {'not': True}
            conclusion = conclusion[1:]
        else:
            ruleDict['conclusion'] = {'not': False}

        name = conclusion[0:conclusion.index('(')]
        variables = conclusion[conclusion.index('(')+1:conclusion.index(')')]
        variables = variables.split(',')
        for l in range (0,len(variables)):
            variables[l] = variables[l].strip()
        varCount = len(variables)

        ruleDict['conclusion']['varCount'] = varCount
        ruleDict['conclusion']['variables'] = variables
        ruleDict['conclusion']['variableSubs'] = variables[:]
        ruleDict['conclusion']['name'] = name


    #If it is an atomic sentence
    elif len(implicationSplit) == 1:

        ruleDict = {'premiseCount': 0}

        conclusion = implicationSplit[0].strip()

        if conclusion[0] == '~':
            ruleDict['conclusion'] = {'not': True}
            conclusion = conclusion[1:]
        else:
            ruleDict['conclusion'] = {'not': False}

        name = conclusion[0:conclusion.index('(')]
        variables = conclusion[conclusion.index('(')+1:conclusion.index(')')]
        variables = variables.split(',')
        for l in range (0,len(variables)):
            variables[l] = variables[l].strip()
        varCount = len(variables)

        ruleDict['conclusion']['varCount'] = varCount
        ruleDict['conclusion']['variables'] = variables
        ruleDict['conclusion']['variableSubs'] = variables[:]
        ruleDict['conclusion']['name'] = name

    return ruleDict

def convertGoalInferenceToDict(goalInference):
    conjunctionSplit = goalInference.split(" && ")

    ruleDict = {'premiseCount':len(conjunctionSplit)}

    for i in range(0,len(conjunctionSplit)):
        premise = conjunctionSplit[i].strip()

        if premise[0] == '~':
            ruleDict['premise'+str(i+1)] = {'not': True}
            premise = premise[1:]
        else:
            ruleDict['premise'+str(i+1)] = {'not': False}

        name = premise[0:premise.index('(')]
        variables = premise[premise.index('(')+1:premise.index(')')]
        variables = variables.split(',')
        varCount = len(variables)

        ruleDict['premise'+str(i+1)]['varCount'] = varCount
        ruleDict['premise'+str(i+1)]['variables'] = variables
        ruleDict['premise'+str(i+1)]['variableSubs'] = variables[:]
        ruleDict['premise'+str(i+1)]['name'] = name

    return ruleDict


#TODO: Think on return values
def BackChainingOR(KNOWLEDGE_BASE,goalConclusion):

    unifiedVariables = ''
    isUnifiable = False
    for rule in KNOWLEDGE_BASE:
        if rule['conclusion']['name'] == goalConclusion['name']:
            unifiedVariables,isUnifiable = unify(rule['conclusion'],goalConclusion)
            if isUnifiable:
                rule['conclusion']['variableSubs']=unifiedVariables
                for i in range (0,rule['conclusion']['varCount']):
                    if ord(str(rule['conclusion']['variableSubs'][i][0])) < 97:
                        for j in range (0,rule['premiseCount']):
                            for k in range(0,rule['premise'+str(j+1)]['varCount']):
                                if rule['premise'+str(j+1)]['variables'][k] == rule['conclusion']['variables'][i]:
                                    rule['premise'+str(j+1)]['variableSubs'][k] = rule['conclusion']['variableSubs'][i]






                #BackChainingAnd(KNOWLEDGE_BASE,rule,unifiedVariables)

            '''print 'Rule: ',rule
            print 'UnifiedVariables: ',unifiedVariables
            print 'IsUnifiable: ',isUnifiable'''



def BackChainingAnd(KNOWLEDGE_BASE,rule,unifiedVariables):
    print 'a'




#This function unifies the given ruleConclusion and the goalConclusion and returns the
# unified substitution of variables and also returns whether they can be unifies or not.
# @return unifiedVariables : New unified substitution
# @return isUnifiable : Boolean stating whether unification is possible or not
def unify(ruleConclusion,goalConclusion):
    ruleConclusionVariables = ruleConclusion['variables']
    goalConclusionVariables = goalConclusion['variables']
    unifiedVariables = []


    for i in range (0,ruleConclusion['varCount']):
        if ord(str(goalConclusionVariables[i])[0]) >= 97 :
            unifiedVariables.append(ruleConclusionVariables[i])
        elif ord(str(ruleConclusionVariables[i])[0]) >= 97 and ord(str(goalConclusionVariables[i])[0]) < 97:
            unifiedVariables.append(goalConclusionVariables[i])
        elif str(ruleConclusionVariables[i]) == str(goalConclusionVariables[i]):
            unifiedVariables.append(ruleConclusionVariables[i])
        else:
            return unifiedVariables,False

    return unifiedVariables,True









#----------------------------------------Input and Control--------------------------------------------------

#filename = sys.argv[-1]
filename = 'input.txt'

#Reading the input file
inputFile = open(filename)

#Reading the goal Inference
goalInference = inputFile.readline().strip()
goalInference = convertGoalInferenceToDict(goalInference)
print goalInference

#Reading the Knowledge Base
kbCount = int(inputFile.readline().strip())
KNOWLEDGE_BASE = []

for i in range(0,kbCount):
    rule = inputFile.readline().strip()
    KNOWLEDGE_BASE.append(convertRuleToDict(rule))
    print KNOWLEDGE_BASE[i]

print 'Test operations:'
BackChainingOR(KNOWLEDGE_BASE,goalInference['premise1'])
print KNOWLEDGE_BASE
'''x,y = unify(KNOWLEDGE_BASE[3]['conclusion'],KNOWLEDGE_BASE[0]['premise3'])
print x
print y
'''
