# LEI to BODS conversion

**Work in progress, use with caution**

A basic python library to convert [GLEIF](https://www.gleif.org/en/about/this-is-gleif) data on company identity and ownership onto [BODS](https://standard.openownership.org/en/0.2.0/) v0.2 statements. Documentation and mapping details yet to be developed.

## Usage

All functions are contained in the file `lei_to_bods.py`. Some example data are provided in the `sample_data` folder.

To run the functions, clone this repo, navigate to the directory, and run:

```
import lei_to_bods as lb
```

### Read in a GLEIF submission

LEI data consist of three main data types: level 1 statements about entities, level 2 statements about ownership relationships, and level 2 data on reporting exceptions. See the `sample_data` folder for example statements of each.

To read in any of these statements and return a python list with one string per statement, use the following:

```
# level 1 data
lei = lb.read_lei('sample_data/20220705-gleif-concatenated-file-lei2-sample.xml')

#level 2 relationship data
rr = lb.read_lei('sample_data/20220705-gleif-concatenated-file-rr-sample.xml')

#level 2 exception data
repex = lb.read_lei('sample_data/20220705-gleif-concatenated-file-repex-sample.xml')
```


### Convert a single statement

**LEI level 1 statement**

View a single LEI level 1 statement in original xml format:

```
print(lei[0])
```

Convert to a BODS JSON entity statement

```
entityStatement = lb.lei1_to_entity_statement(lei[0])
print(entityStatement)
```

**LEI level 2 relationship statement**

View a single LEI level 2 relationship statement in original xml format:

```
print(rr[0])
```

Convert to a BODS JSON ownership or control statement

```
oocStatement = lb.lei2_relationship_to_ooc_statement(rr[0])
print(oocStatement)
```

**LEI level 2 exception statement**

View a single LEI level 2 exception statement in original xml format:

```
print(repex[0])
```

Convert to a BODS JSON ownership or control statement with unknown interested party

```
oocExceptionStatement = lb.lei2_exception_to_ooc_statement(repex[0])
print(oocExceptionStatement)
```

### Convert an entire declaration

If you have a set of LEI statements in a file that represent a single declaration (i.e. a set of relationship statements combined with all connected LEI level 1 statements), you can convert directly to a BODS array as follows:

```
lb.lei_statement_to_bods('sample_data/20220705-gleif-concatenated-file-statement-sample.xml', write = True, outfile = 'sample_data/20220705-gleif-concatenated-file-statement-sample.json')
```

You can view this file in the `sample_data` folder and check using the [BODS data review tool](https://datareview.openownership.org/), and visualise using the [BODS visualiser](https://www.openownership.org/en/publications/beneficial-ownership-visualisation-system/bods-data-visualiser/)

### Notes on mapping

To follow