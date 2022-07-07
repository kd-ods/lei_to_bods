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