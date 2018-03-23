from datetime import datetime
import sys
import yaml


def _fmt_authors(authors):
    if len(authors) == 1:
        out = '{} '.format(_fmt_author(authors[0]))
    elif len(authors) > 1:
        out = ', '.join(_fmt_author(author) for author in authors[:-1])
        out += ', and {} '.format(_fmt_author(authors[-1]))
    else:
        out = ''
    return out


def _fmt_emph(x):
    if x:
        return '*{}* '.format(x)
    else:
        return ''


def _fmt_author(author):
    given = author['given'].split(' ')
    initial = ' '.join('{}.'.format(g[0]) for g in given)
    if author['family'][:6] == 'Tilley':
        return '**{}, {}**'.format(author['family'], initial)
    else:
        return '{}, {}'.format(author['family'], initial)


def _fmt_title(title):
    if title:
        return '"{}" '.format(title)
    else:
        return ''


def _fmt_issued(issued):
    if len(issued) == 0:
        return ''
    if len(issued) == 1:
        return _fmt_year(issued[0]['year'])
    else:
        raise RuntimeError


def _fmt_year(year):
    if year:
        return '**({})** '.format(year)
    else:
        return ''


def _fmt_volume(volume):
    if volume:
        return 'Vol: {}, '.format(volume)
    else:
        return ''


def _fmt_page(page):
    if page:
        return 'pp: {} '.format(page)
    else:
        return ''


def _fmt_doi(doi):
    if doi:
        return 'DOI: [{0}](https://doi.org/{0}) '.format(doi)
    else:
        return ''


def _fmt_pmcid(pmcid):
    if pmcid:
        return 'PMCID: [{0}](https://www.ncbi.nlm.nih.gov/pmc/articles/{0}) '.format(pmcid)
    else:
        return ''


def _fmt_arxiv(arxiv):
    if arxiv:
        return 'arXiv: [{0}](https://arxiv.org/abs/{0}) '.format(arxiv)
    else:
        return ''


def _sort_key(ref):
    issued = ref['issued'][0]
    return datetime(issued['year'], issued.get('month', 1), issued.get('day', 1))


if __name__ == '__main__':

    _fmt_container = _fmt_emph
    _fmt_publisher = _fmt_emph

    for l in sys.stdin:
        if l == '```{=yaml}\n':
            assert sys.stdin.readline() == '---\n'
            yamlblock = ''
            for l in sys.stdin:
                if l == '---\n':
                    assert sys.stdin.readline() == '```\n'
                    break
                yamlblock += l
            data = yaml.load(yamlblock)
            if len(data) != 1 or 'references' not in data.keys():
                raise RuntimeError
            else:
                for ref in sorted(data['references'], key=_sort_key, reverse=True):
                    print(_fmt_authors(ref.get('author', [])), end='')
                    print(_fmt_issued(ref.get('issued', [])), end='')
                    print(_fmt_title(ref.get('title', '')), end='')
                    print(_fmt_container(ref.get('container-title', '')), end='')
                    print(_fmt_publisher(ref.get('publisher', '')), end='')
                    print(_fmt_volume(ref.get('volume', '')), end='')
                    print(_fmt_page(ref.get('page', '')), end='')
                    print(_fmt_doi(ref.get('DOI', '')), end='')
                    print(_fmt_pmcid(ref.get('PMCID', '')), end='')
                    print(_fmt_arxiv(ref.get('arXiv', '')), end='')

                    print('\n\n', end='')
        else:
            print(l, end='')
