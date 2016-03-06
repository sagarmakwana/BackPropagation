class KNOWLEDGE_BASE:
    ruleCount = 0

    def __init__(self,listofRules):
        KNOWLEDGE_BASE.ruleCount = len(listofRules)
        self.rules = listofRules[:]

    def standardize_knowledge_base(self):

        openIndex = -1
        closeIndex = -1

        ruleCount = 1
        for rule in self.rules:
            remaining = rule[:]
            newRule = ''
            openIndex = remaining.find('(')
            closeIndex = remaining.find(')')

            while (openIndex != -1 and closeIndex != -1):
                variables = remaining[openIndex+1:closeIndex]
                newRule = newRule + remaining[0:openIndex]
                remaining = remaining[closeIndex+1:]

                variables = variables.split(',')

                subsVar = ''
                for l in range (0,len(variables)):
                    variables[l] = variables[l].strip()
                    if ord(str(variables[l][0])) >= 97:
                        subsVar = subsVar + variables[l]+''+str(ruleCount)+', '
                    else:
                        subsVar = subsVar + variables[l] + ', '


                subsVar = '(' + subsVar[0:len(subsVar)-2] + ')'
                newRule = newRule + subsVar

                openIndex = remaining.find('(')
                closeIndex = remaining.find(')')

            self.rules[ruleCount-1] = newRule
            ruleCount = ruleCount + 1

    def fetch_rules_for_goal(self,goal):
        goalName = goal[0:goal.index('(')]

        #List of rules that match with goal
        fetched_rules = []

        for rule in self.rules:
            implicationSplit = rule.split(' => ')

            name = ''
            if len(implicationSplit) == 2:
                consequent = implicationSplit[1].strip()
                name = consequent[0:consequent.index('(')]
            else:
                name = rule[0:rule.index('(')]

            if name == goalName:
                fetched_rules.append(rule)

        return fetched_rules

    def fetch_all_rules(self):
        return self.rules

#----------------------------------------Input and Control-------------------------------------

#filename = sys.argv[-1]
filename = 'input.txt'

#Reading the input file
inputFile = open(filename)

#Reading the goal Inference
goalInput = inputFile.readline().strip()

goals = goalInput.split(" && ")

for i in range(0,len(goals)):
    goals[i] = goals[i].strip()


kbCount = int(inputFile.readline().strip())
kb = []

for i in range(0,kbCount):
    rule = inputFile.readline().strip()
    kb.append(rule)

print 'Before'
KB = KNOWLEDGE_BASE(kb)

print KB.fetch_all_rules()

KB.standardize_knowledge_base()

print 'After'

print  KB.fetch_all_rules()





