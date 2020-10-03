import os
import re
import xmltodict
import wikitextparser as wtp
from tqdm import tqdm


dump_xml_file = "../../kowiki-20200920-pages-articles-multistream.xml"
text_root = '../../texts/'
DEBUG = False
multiline_pattern = re.compile('\\n{3,}')


def transform_page_to_wikitext(page):
    def as_wikitext_header(line):
        if line and line[0] == '=' and line[-1] == '=':
            line = line.replace('=', ' =') + '\n'
        return line

    def normalize(line):
        line = line.strip()
        if not line:
            return line
        if line[:3] == '파일:' or line[:3] == '분류:' or line[:4] == '섬네일|':
            return ''
        if line[:2] == '* ' or line[:2] == '**':
            return line[2:].strip()
        if line[:2] == '{|' or line[:1] == '|' or 'right|' in line[:20] or 'px|' in line[:20]:
            return ''
        return line.strip()

    title = page['title']
    sections = wtp.parse(page['revision']['text']['#text']).sections
    wikitext = []
    first_section_text = sections[0].plain_text()
    if first_section_text and first_section_text[0] != '=':
        lines = first_section_text.split('\n')
        lines = [as_wikitext_header(normalize(line)) for line in lines]
        first_section_text = '\n'.join(lines)
        wikitext.append(f' = {title} =\n\n{first_section_text}\n')
    for section in sections[1:]:
        lines = section.plain_text().split('\n')
        lines = [as_wikitext_header(normalize(line)) for line in lines]
        text = '\n'.join(lines)
        wikitext.append(text)
    wikitext = '\n\n'.join(wikitext)
    wikitext = multiline_pattern.sub('\n\n', wikitext)
    return wikitext


def get_path(index): 
    suffix = '{:07}'.format(index)[-3:] 
    path = f'{text_root}/{suffix}/{index}.txt'
    return path


def check_dir(path):
    dirname = os.path.abspath(os.path.dirname(path))
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def load_pages():
    with open(dump_xml_file) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    mediawiki = data_dict['mediawiki']
    pages = mediawiki['page'][1:]  # type(pages) == list
    if DEBUG:
        pages = pages[:200]
    return pages


pages = load_pages()
for index, page in enumerate(tqdm(pages, desc='Transform wikitext', total=len(pages))):
    try:
        wikitext = transform_page_to_wikitext(page)
    except:
        continue
    if wikitext.count('\n') <= 4 and (('#REDIRECT' in wikitext) or ('#넘겨주기' in wikitext) or ('#redirect' in wikitext)):
        continue
    outpath = get_path(index)
    check_dir(outpath)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(wikitext)
