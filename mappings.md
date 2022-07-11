# LEI to BODS field mappings

## Entity statements from LEI level 1 data

|BODS v0.2 field|LEI level 1 field|Notes
|---|---|---|
`statementID`|`lei:LEI`| Only 20 chars
`statementType`|'entityStatement'|Hard coded
`statementDate`|`lei:LastUpdateDate`|
`entityType`|'registeredEntity'|Hard coded
`name`|`lei:LegalName`|
`jurisdiction`|`lei:LegalJurisdiction`|
`identifiers`|`lei:LEI`|
`foundingDate`|`lei:EntityCreationDate`|
`addresses`|`lei:LegalAddress`| (type = 'registered')
`addresses`|`lei:HeadquartersAddress`| (type = 'business')
`source.type`|'officialRegister'| Hard coded
`source.description`|'GLEIF'|Hard coded   

## Ownership or control statements from LEI level 2 relationship data

|BODS v0.2 field|LEI level 1 field|Notes
|---|---|---|
`statementID`|Randomly generated|
`statementType`|'ownershipOrControlStatement'|Hard coded
`statementDate`|`rr:LastUpdateDate`|
`subject.describedByEntityStatement`|`rr:EndNode`|
`interestedParty.describedByEntityStatement`|`rr:StartNode`|
`interests.type`|'otherInfluenceOrControl'|Hard coded
`interests.interestLevel`|`rr:RelationshipType`|'direct if directly consolidating, 'indirect' if ultimately consolidating, 'unknown' if no data available
`interests.startDate`|`rr:StartDate`| Uses relationship period if available, otherwise accounting period
`interests.beneficialOwnershipOrControl`|False|Hard coded
`source.type `|'officialRegister'|Hard coded
`source.description`|'GLEIF'|Hard coded

## Ownership or control statements from LEI level 2 exception data

|BODS v0.2 field|LEI level 1 field|Notes
|---|---|---|
`statementID`|Randomly generated|
`statementType`|'ownershipOrControlStatement'|Hard coded
`subject.describedByEntityStatement`|`repex:LEI`|
`interestedParty.unspecified`|`repex:ExceptionReason`|
`interests.type`|'unknownInterest'|
`interests.interestLevel`|`repex:ExceptionCategory`|'direct if directly consolidating, 'indirect' if ultimately consolidating, 'unknown' if no data available
`source.type`|'officialRegister'|Hard coded
`source.description`|'GLEIF'|Hard coded