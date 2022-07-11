import json, random

def read_lei(file):
    if '-lei2-' in file:
        itemtag = 'lei:LEIRecord xmlns'
    elif '-rr-' in file:
        itemtag = 'rr:RelationshipRecord xmlns'
    elif '-repex-' in file:
        itemtag = 'repex:Exception xmlns'
    else:
        raise ValueError("file type invalid")
    
    with open(file) as f:
        dd = f.readlines()

    f.close()

    out = []
    record = ''

    for line in dd:  
        if '<' + itemtag in line:
            out.append(record)
            record = line
        else:
            record = record + line
    
    out.append(record)
    return(out[1:len(out)])

def lei1_to_entity_statement(lei1Object):
    splitRecord = lei1Object.split('\n')

    statementID = ''
    statementType = 'entityStatement'
    statementDate = ''
    entityType = 'registeredEntity'
    name = ''
    jurisdiction = ''
    identifiers = ''
    foundingDate = ''
    registeredAddress = ''
    registeredAddressPostCode = ''
    registeredAdressCountry = ''
    registeredAddressSwitch = 0
    businessAddress = ''
    businessAddressPostCode = ''
    businessAddressCountry = ''
    businsessAddressSwitch = 0
    sourceType = ['officialRegister']
    sourceDescription = 'GLEIF'

    for line in splitRecord:
        if '<lei:LegalName' in line:
            name = line.split('>')[1].split('<')[0]
        if '<lei:LastUpdateDate>' in line:
            statementDate = line.split('>')[1].split('<')[0]
        if '<lei:LegalJurisdiction>' in line:
            jurisdiction = {'code':line.split('>')[1].split('<')[0]}
        if '<lei:LEI>' in line:
            identifiers = [{'id':line.split('>')[1].split('<')[0],
            'scheme':'XI-LEI',
            'schemeName':'Global Legal Entity Identifier Index'}]
            statementID = line.split('>')[1].split('<')[0]
        if '<lei:EntityCreationDate>' in line:
            foundingDate = line.split('>')[1].split('<')[0]
        if '<lei:LegalAddress' in line:
            registeredAddressSwitch = 1
            registeredAddressString = ''
        if '</lei:LegalAddress' in line:
            registeredAddressSwitch = 0
            registeredAddress = {'type':'registered','address':registeredAddressString,'postCode':registeredAddressPostCode,'country':registeredAdressCountry}
        if registeredAddressSwitch == 1:
            if '<lei:FirstAddressLine>' in line:
                registeredAddressString = registeredAddressString + line.split('>')[1].split('<')[0] + ','
            if '<lei:City>' in line:
                registeredAddressString = registeredAddressString + line.split('>')[1].split('<')[0]  + ','
            if '<lei:Region>' in line:
                registeredAddressString = registeredAddressString + line.split('>')[1].split('<')[0]
            if '<lei:Country>' in line:
                registeredAdressCountry = line.split('>')[1].split('<')[0]
            if '<lei:PostalCode>' in line:
                registeredAddressPostCode = line.split('>')[1].split('<')[0]
        if '<lei:HeadquartersAddress' in line:
            businsessAddressSwitch = 1
            businsessAddressString = ''
        if '</lei:HeadquartersAddress' in line:
            businsessAddressSwitch = 0
            businessAddress = {'type':'business','address':businsessAddressString,'postCode':businessAddressPostCode,'country':businessAddressCountry}
        if businsessAddressSwitch == 1:
            if '<lei:FirstAddressLine>' in line:
                businsessAddressString = businsessAddressString + line.split('>')[1].split('<')[0] + ','
            if '<lei:City>' in line:
                businsessAddressString = businsessAddressString + line.split('>')[1].split('<')[0]  + ','
            if '<lei:Region>' in line:
                businsessAddressString = businsessAddressString + line.split('>')[1].split('<')[0]
            if '<lei:Country>' in line:
                businessAddressCountry = line.split('>')[1].split('<')[0]
            if '<lei:PostalCode>' in line:
                businessAddressPostCode = line.split('>')[1].split('<')[0]
        if '<lei:ValidationSources>FULLY_CORROBORATED</lei:ValidationSources>' in line:
            sourceType.append('verified')
                

    d = {'statementID': statementID,
    'statementType':statementType,
    'statementDate':statementDate,
    'entityType':entityType,
    'name':name,
    'jurisdiction':jurisdiction,
    'identifiers':identifiers,
    'foundingDate':foundingDate,
    'addresses':[registeredAddress,businessAddress],
    'source':{'type':sourceType,'description':sourceDescription}}

    out = json.dumps(d,indent = 4)

    return(out)

def lei2_relationship_to_ooc_statement(lei2Object):
    splitRecord = lei2Object.split('\n')

    statementID = ''.join(random.choice('0123456789ABCDEF') for i in range(32))
    statementType = 'ownershipOrControlStatement'
    statementDate = ''
    subjectDescribedByEntityStatement = ''
    subjectSwitch = 0
    interestedPartyDescribedByEntityStatement = ''
    interestedPartySwitch = 0
    interestType = 'otherInfluenceOrControl'
    interestLevel = 'unknown'
    interestStartDate = ''
    interestStartDateRelationship = ''
    interestStartDateAccounting = ''
    interestStartDateSwitch = 0
    beneficialOwnershipOrControl = False
    sourceType = ['officialRegister']
    sourceDescription = 'GLEIF'

    for line in splitRecord:
        if '<rr:LastUpdateDate>' in line:
            statementDate = line.split('>')[1].split('<')[0]
        if '<rr:StartNode>' in line:
            interestedPartySwitch = 1
        if '</rr:StartNode>' in line:
            interestedPartySwitch = 0
        if  interestedPartySwitch == 1 and '<rr:NodeID>' in line:
                interestedPartyDescribedByEntityStatement = line.split('>')[1].split('<')[0]
        if '<rr:EndNode>' in line:
            subjectSwitch = 1
        if '</rr:EndNode>' in line:
            subjectSwitch = 0
        if  subjectSwitch == 1 and '<rr:NodeID>' in line:
                subjectDescribedByEntityStatement = line.split('>')[1].split('<')[0]             
        if '<rr:RelationshipType>IS_ULTIMATELY_CONSOLIDATED_BY</rr:RelationshipType>' in line:
            interestLevel = 'indirect'
        if '<rr:RelationshipType>IS_DIRECTLY_CONSOLIDATED_BY</rr:RelationshipType>' in line:
            interestLevel = 'direct'
        if '<rr:RelationshipPeriod>' in line:
            interestStartDateSwitch = 1
        if '</rr:RelationshipPeriod>' in line:
            interestStartDateSwitch = 0
        if  interestStartDateSwitch == 1 and '<rr:StartDate>' in line: 
                interestStartDate = line.split('>')[1].split('<')[0]
        if  interestStartDateSwitch == 1 and '<rr:PeriodType>RELATIONSHIP_PERIOD</rr:PeriodType>' in line:
                interestStartDateRelationship = interestStartDate
        if '<rr:ValidationSources>FULLY_CORROBORATED</rr:ValidationSources>' in line:
            sourceType.append('verified')

    if interestStartDateRelationship != '':
        interestStartDate = interestStartDateRelationship


    d = {'statementID': statementID,
    'statementType':statementType,
    'statementDate':statementDate,
    'subject':{'describedByEntityStatement':subjectDescribedByEntityStatement},
    'interestedParty':{'describedByEntityStatement':interestedPartyDescribedByEntityStatement},
    'interests':[{'type':interestType,
    'interestLevel':interestLevel,
    'beneficialOwnershipOrControl':beneficialOwnershipOrControl,
    'startDate':interestStartDate}],
    'source':{'type':sourceType,'description':sourceDescription}}

    out = json.dumps(d,indent = 4)

    return(out)

def lei2_exception_to_ooc_statement(lei2Object):
    splitRecord = lei2Object.split('\n')

    statementID = ''.join(random.choice('0123456789ABCDEF') for i in range(32))
    statementType = 'ownershipOrControlStatement'
    subjectDescribedByEntityStatement = ''
    interestedPartyUnspecifiedReason = ''
    interestType = 'unknownInterest'
    interestLevel = 'unknown'
    sourceType = ['officialRegister']
    sourceDescription = 'GLEIF'

    for line in splitRecord:
        if '<rr:StartNode>' in line:
            interestedPartySwitch = 1
        if '<repex:ExceptionReason>' in line:
            interestedPartyUnspecifiedReason = line.split('>')[1].split('<')[0]
        if '<repex:LEI>' in line:
            subjectDescribedByEntityStatement = line.split('>')[1].split('<')[0]             
        if '<repex:ExceptionCategory>ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT</repex:ExceptionCategory>' in line:
            interestLevel = 'indirect'
        if '<repex:ExceptionCategory>DIRECT_ACCOUNTING_CONSOLIDATION_PARENT</repex:ExceptionCategory>' in line:
            interestLevel = 'direct'


    d = {'statementID': statementID,
    'statementType':statementType,
    'subject':{'describedByEntityStatement':subjectDescribedByEntityStatement},
    'interestedParty':{'unspecified':interestedPartyUnspecifiedReason},
    'interests':[{'type':interestType,
    'interestLevel':interestLevel,
    'source':{'type':sourceType,'description':sourceDescription}}]
    }

    out = json.dumps(d,indent = 4)

    return(out)

def lei_statement_to_bods(leifile, write = False, outfile = 'out.json'):
    with open(leifile) as f:
        dd = f.readlines()
    f.close()

    itemtags = ['lei:LEIRecord xmlns','rr:RelationshipRecord xmlns','repex:Exception xmlns']

    out = []
    record = ''

    for line in dd:  
        if any(item in line for item in itemtags):
            out.append(record)
            record = line
        else:
            record = record + line
    
    out.append(record)
    out = out[1:len(out)]

    finalout = '[\n'

    for item in out:
        if 'lei:LEIRecord xmlns' in item:
            finalout = finalout + lei1_to_entity_statement(item) + ',\n'
        elif 'rr:RelationshipRecord xmlns' in item:
            finalout = finalout + lei2_relationship_to_ooc_statement(item) + ',\n'
        elif 'repex:Exception xmlns' in item:
            finalout = finalout + lei2_exception_to_ooc_statement(item) + ',\n'

    finalout = finalout[0:(len(finalout)-2)] + '\n]'

    if write == True:
        with open(outfile, 'w') as f:
            f.write(finalout)
    
    f.close()

    return(finalout)   