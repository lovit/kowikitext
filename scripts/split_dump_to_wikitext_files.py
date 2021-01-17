import os
import re
import xmltodict
import wikitextparser as wtp
from tqdm import tqdm

from normalizer import text_preprocess, text_postprocess, title_preprocess


dump_xml_file = "../../kowiki-20200920-pages-articles-multistream.xml"
text_root = '../../texts/'
DEBUG = False
multiline_pattern = re.compile('\\n{3,}')


def transform_page_to_wikitext(page):
    title = page['title']
    sections = wtp.parse(page['revision']['text']['#text']).sections
    wikitext = []
    first_section_text = sections[0].plain_text()
    if first_section_text and first_section_text[0] != '=':
        lines = first_section_text.split('\n')
        lines = [text_preprocess(line) for line in lines]
        first_section_text = text_postprocess('\n'.join(lines))
        wikitext.append(f' = {title} =\n\n{first_section_text}\n')
    for section in sections[1:]:
        section_title = section.title.strip()
        if section_title is not None:
            section_title = section_title.strip()
        if ((section_title is None) or
            (section_title in ["같이 보기", "각주", "참고 문헌", "외부 링크"]) or
            (not section_title)
        ):
            continue
        plain_text = section.plain_text()
        lines = plain_text.split("\n")
        level = 0
        if lines:
            level = lines[0].split()[0].count("=")
        if level == 0 or level >= 3:
            continue
        lines = [text_preprocess(line) for line in lines]
        text = text_postprocess("\n".join(lines)).strip()
        if not text:
            continue
        wikitext.append(f"\n\n{text}\n\n")
    wikitext = ''.join(wikitext)
    wikitext = re.sub('\n{3,}', '\n\n', wikitext).strip()
    return wikitext


def get_path(index): 
    suffix = '{:07}'.format(index)[-3:] 
    path = f'{text_root}/{suffix}/{index}.txt'
    return path


def check_dir(path):
    dirname = os.path.abspath(os.path.dirname(path))
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def load_pages(dump_xml_file):
    with open(dump_xml_file) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    mediawiki = data_dict['mediawiki']
    pages = mediawiki['page'][1:]  # type(pages) == list
    if DEBUG:
        pages = pages[:200]
    return pages


pages = load_pages(dump_xml_file)
desc = 'Transform wikitext'
page_iterator = tqdm(pages, desc=desc, total=len(pages))
n_success = 0
for index, page in enumerate(page_iterator):
    desc = f'Transform wikitext #success={n_success}'
    page_iterator.set_description(desc)
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
    n_success += 1