# DBLP2CSV
Convert a DBLP XML file (https://dblp.uni-trier.de/xml/) to CSV format. A SAX implementation of dblp-to-csv (https://github.com/ThomHurks/dblp-to-csv) that is capable to handle up-to-date large dblp xml files.

## Usage
Refer to https://github.com/ThomHurks/dblp-to-csv

## Commandline options
```
usage: parser.py xml_filename dtd_filename outputfile

Parse the DBLP XML file and convert it to CSV

Arguments:
  xml_filename          The DBLP XML file that will be parsed
  dtd_filename          The DTD file used to parse the XML file
  outputfile            The output CSV filename

```

## Some outputs
Elements & Attributes: 
```
Elements : {'book', 'proceedings', 'www', 'inproceedings', 'article', 'phdthesis', 'incollection', 'mastersthesis'}
Attributes : {
                'book': {'isbn', 'isbn-type', 'booktitle', 'publisher', 'cite', 'cite-label', 'series-href',
                         'publisher-href', 'year', 'editor', 'editor-orcid', 'author', 'note', 'pages', 'ee', 'school',
                         'note-type', 'mdate', 'month', 'url', 'title', 'ee-type', 'series', 'publtype', 'author-orcid',
                         'author-bibtex', 'crossref', 'cdrom', 'volume', 'key'},
                'proceedings': {'address', 'isbn', 'isbn-type', 'booktitle', 'publisher', 'cite', 'cite-label',
                                'series-href', 'publisher-href', 'journal', 'year', 'editor-orcid', 'editor', 'author',
                                'note', 'pages', 'ee', 'note-type', 'mdate', 'url', 'title', 'number', 'ee-type',
                                'series', 'publtype', 'volume', 'key'},
                'www': {'publtype', 'year', 'editor', 'note-type', 'author', 'mdate', 'crossref', 'note', 'url', 'cite',
                        'note-label', 'title', 'url-type', 'ee', 'key', 'author-bibtex'},
                'inproceedings': {'booktitle', 'cite', 'cite-label', 'year', 'editor', 'editor-orcid', 'author', 'note',
                                  'pages', 'ee', 'note-type', 'mdate', 'month', 'author-aux', 'url', 'title', 'number',
                                  'title-bibtex', 'ee-type', 'author-orcid', 'publtype', 'crossref', 'cdrom', 'volume',
                                  'key'},
                'article': {'booktitle', 'publisher', 'cite', 'cite-label', 'journal', 'year', 'editor', 'editor-orcid',
                            'author', 'note', 'pages', 'ee', 'note-type', 'mdate', 'month', 'author-aux', 'url',
                            'title', 'number', 'ee-type', 'title-bibtex', 'author-orcid', 'publtype', 'crossref',
                            'cdrom', 'cdate', 'volume', 'key'},
                'phdthesis': {'publtype', 'isbn', 'year', 'isbn-type', 'author', 'note-type', 'mdate', 'publisher',
                              'note', 'month', 'series', 'title', 'pages', 'ee', 'series-href', 'number', 'volume',
                              'ee-type', 'key', 'author-orcid', 'school'},
                'incollection': {'publtype', 'year', 'author', 'mdate', 'booktitle', 'crossref', 'url', 'cdrom',
                                 'publisher', 'note', 'cite', 'cite-label', 'title', 'chapter', 'pages', 'ee', 'number',
                                 'ee-type', 'key', 'publisher-href', 'author-orcid'},
                'mastersthesis': {'year', 'author', 'note-type', 'mdate', 'note', 'title', 'ee', 'ee-type', 'key',
                                  'school'}
             }
```
Example of output files: 
    ![image](output.png)


