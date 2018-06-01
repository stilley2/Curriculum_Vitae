from datetime import datetime
import sys
import yaml


def _fmt_authors(authors):
    if len(authors) == 1:
        out = '{} '.format(_fmt_author(authors[0]))
    elif len(authors) > 1:
        out = ', '.join(_fmt_author(author) for author in authors[:-1])
        out += ', and {}'.format(_fmt_author(authors[-1]))
    else:
        out = ''
    return out, ' '


def _fmt_emph(x):
    if x:
        return '*{}*'.format(x), ' '
    else:
        return '', None


def _fmt_author(author):
    given = author['given'].split(' ')
    initial = ' '.join('{}.'.format(g[0]) for g in given)
    if author['family'][:6] == 'Tilley':
        return '**{}, {}**'.format(author['family'], initial)
    else:
        return '{}, {}'.format(author['family'], initial)


def _fmt_title(title):
    if title:
        return '"{}"'.format(title), ' '
    else:
        return '', None


def _fmt_issued(issued):
    if len(issued) == 0:
        return '', None
    if len(issued) == 1:
        return _fmt_year(issued[0]['year']), ' '
    else:
        raise RuntimeError


def _fmt_year(year):
    if year:
        return '**({})**'.format(year)
    else:
        return ''


def _fmt_volume(volume):
    if volume:
        return 'Vol: {}'.format(volume), ', '
    else:
        return '', None


def _fmt_page(page):
    if page:
        return 'pp: {}'.format(page), ', '
    else:
        return '', None


def _fmt_doi(doi):
    if doi:
        return 'DOI: [{0}](https://doi.org/{0})'.format(doi), ', '
    else:
        return '', None


def _fmt_pmcid(pmcid):
    if pmcid:
        return 'PMCID: [{0}](https://www.ncbi.nlm.nih.gov/pmc/articles/{0})'.format(pmcid), ', '
    else:
        return '', None


def _fmt_arxiv(arxiv):
    if arxiv:
        return 'arXiv: [{0}](https://arxiv.org/abs/{0})'.format(arxiv), ', '
    else:
        return '', None


def _fmt_url(url):
    if url:
        url = url.strip("'")
        return '[URL]({0})'.format(url), ', '
    else:
        return '', None


def _sort_key(ref):
    issued = ref['issued'][0]
    return datetime(issued['year'], issued.get('month', 1), issued.get('day', 1))


def _print_wrapper(toprint, outstrlist):
    val, sep = toprint
    if val:
        outstrlist.append(val)
        outstrlist.append(sep)


if __name__ == '__main__':

    _fmt_container = _fmt_emph
    _fmt_publisher = _fmt_emph
    _fmt_event = _fmt_emph

    for l in sys.stdin:
        if l == '---\n':
            yamlblock = ''
            for l in sys.stdin:
                if l == '---\n':
                    break
                yamlblock += l
            data = yaml.load(yamlblock)
            if len(data) == 1 and 'references' in data.keys():
                for ref in sorted(data['references'], key=_sort_key, reverse=True):
                    outstrlist = []
                    _print_wrapper(_fmt_authors(ref.get('author', [])), outstrlist)
                    _print_wrapper(_fmt_issued(ref.get('issued', [])), outstrlist)
                    _print_wrapper(_fmt_title(ref.get('title', '')), outstrlist)
                    if ref['type'] == 'paper-conference':
                        _print_wrapper(_fmt_container(ref.get('container-title', '')), outstrlist)
                    elif ref['type'] == 'article-journal':
                        _print_wrapper(_fmt_publisher(ref.get('publisher', '')), outstrlist)
                    elif ref['type'] == 'speech':
                        _print_wrapper(_fmt_event(ref.get('event', '')), outstrlist)
                    _print_wrapper(_fmt_volume(ref.get('volume', '')), outstrlist)
                    _print_wrapper(_fmt_page(ref.get('page', '')), outstrlist)
                    _print_wrapper(_fmt_doi(ref.get('DOI', '')), outstrlist)
                    _print_wrapper(_fmt_pmcid(ref.get('PMCID', '')), outstrlist)
                    _print_wrapper(_fmt_arxiv(ref.get('arXiv', '')), outstrlist)
                    _print_wrapper(_fmt_url(ref.get('URL', '')), outstrlist)

                    print(''.join(outstrlist[:-1]), end='\n\n')
            else:
                print('---')
                print(yamlblock, end='')
                print('---')
        else:
            print(l, end='')
