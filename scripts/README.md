## Scripts for making ko-wikitext

First, download and decompress dump data from https://dumps.wikimedia.org/kowiki/20200920/

```
wget https://dumps.wikimedia.org/kowiki/20200920/kowiki-20200920-pages-articles-multistream.xml.bz2
wget https://dumps.wikimedia.org/kowiki/20200920/kowiki-20200920-pages-articles-multistream-index.txt.bz2

bzip2 -vd kowiki-20200920-pages-articles-multistream-index.txt.bz2
bzip2 -vd kowiki-20200920-pages-articles-multistream.xml.bz2
```

Check `dump_xml_file`, `text_root`, and `DEBUG` in `split_dump_to_wikitext_files.py` and run it

```
python split_dump_to_wikitext_files.py
```

Snapshot of `text_root`. Redirected pages are removed

```
├── 000
|    ├── ...
|    ├── 97000.txt
|    ├── 98000.txt
|    └── 99000.txt
├── ...
├── 998
└── 999
```


ko-wikipedia statistics
- number of articles: 1542616
- after removing redirect page: 886621
