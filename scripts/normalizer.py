import re


def text_preprocess(line):
    line = line.strip()
    line = line.replace("----", "").strip()
    line = line.replace("--", "\n").strip()
    line = line.replace("''''''", "").strip()
    if not line:
        return line
    if (
        line[:2] == "참고"
        or line[:2] == "각주"
        or line[:3] == "파일:"
        or line[:3] == "분류:"
        or line[:4] == "섬네일|"
    ):
        return ""
    if line[:2] == "* " or line[:2] == "**":
        return line[2:].strip()
    if line[0] == ":" or line[0] == "\\" or line[0] == "!" or line[0] == "&" or line[0] == ";":
        return ""
    if line[:2] == "==" and line[-2:] == "==":
        return title_preprocess(line)
    if line[:2] == "# ":
        line = line[2:].strip()
    if "|" in line:
        return ""
    if line[-2:] == "px":
        return ""
    line = detach_link(line)
    line = common(line)
    line = line.replace("*\n", "").strip()
    line = line.replace("()", "")
    return line.strip()


def text_postprocess(concatenate_lines):
    concatenate_lines = re.sub("\n{3,}", "\n\n", concatenate_lines).strip()
    if text_is_redirect(concatenate_lines):
        return concatenate_lines
    if len(concatenate_lines) < 20:
        return ""
    return concatenate_lines


def title_preprocess(line):
    if line[:2] == "틀:":
        return ""
    if line[:3] == "분류:" or line[:3] == "모듈:":
        return ""
    if line[:5] == "위키백과:":
        return ""
    if line[-2:] == "결과":
        return ""
    if "Cite references link" in line:
        return ""
    line = detach_link(line)
    line = common(line)
    line = '\n' + line.replace('=', ' =').strip() + '\n'
    return line


def detach_link(line):
    """
    Examples:
        >>> detach_link("abcdef [[AB|C]] def")
        $ 'abcdef AB def'
        >>> detach_link("abafsd [[D]]dd")
        $ 'abafsd Ddd'
        >>> detach_link("abcdef [[AB|C]] def abafsd [[D]]dd")
        $ 'abcdef AB def abafsd Ddd'
        >>> detach_link("abcdef {{AB|C}} def abafsd {{D}}dd")
        $ 'abcdef AB def abafsd Ddd'
    """
    group = re.findall(r"[\[\{][\[\{][^\]\}]+[\]\}][\]\}]", line)
    for matched in group:
        replace = matched[2:-2].split("|")[0]
        line = line.replace(matched, replace)
    return line.strip()


def common(line):
    line = re.sub(r"[《》]", "", line)
    line = re.sub(r"<ref>.+</ref>", " ", line)
    line = re.sub(r"<span style.+</span>", " ", line)
    line = re.sub(
        r"((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", " ", line
    )
    line = re.sub(f"\([,\s]+\)", "", line)
    return line.strip()


def text_is_redirect(text):
    return text[:5] == "#넘겨주기" or text[:9] == "#REDIRECT"


def detach_redirect_tag(text):
    if text[:5] == "#넘겨주기":
        return text[5:].strip()
    if text[:9] == "#REDIRECT":
        return text[9:].strip()
    return text
