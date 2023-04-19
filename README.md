# Download and unzip files

```shell
wget https://dblp.org/xml/release/dblp-2023-04-02.xml.gz
wget https://dblp.org/xml/release/dblp-2019-11-22.dtd
gzip -d dblp-2023-04-02.xml.gz 
```

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


# CSV TO MLG

```shell
python csv_to_mlg.py -s [start-year] -e [end-year]
```

- Start year is set to be 2016 by default, while end year is set to be 2022 by default.

- In default setting, we can get a graph with 7 layers, in each layer, there are 689k nodes and 14M edges in total

- In detail, 
    ```shell

    NodeNum = 689886
    EdgeNum = {1: 1287806, 2: 1514599, 3: 1846423, 4: 2238252, 5: 2487581, 6: 2706280, 7: 2793023}

    ```

- Layer 1-6 represent year 2016 to year 2022.

- Each node represent an author, while an edge connecting two nodes in a layer l represents that two author co-author a certain paper in year l.

