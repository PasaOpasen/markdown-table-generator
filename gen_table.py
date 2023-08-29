
from typing import List, Dict, Sequence, Optional, TypedDict, Union, Set

import sys
from pathlib import Path
from collections import defaultdict

import argparse


def split_text(s: str, max_len: int) -> List[str]:
    """
    Splits text to several parts with len<=max
    Args:
        s:
        max_len: max len, 0 means split disabling

    Returns:

    >>> _ = split_text
    >>> _('t', max_len=10)
    ['t']
    >>> _('text', max_len=1)
    ['t', 'e', 'x', 't']
    >>> _('text with spaces', max_len=5)
    ['text', 'with', 'space', 's']
    >>> _('some usual text with many words', max_len=14)
    ['some usual', 'text with many', 'words']
    >>> _s = 'simple not so short test string'
    >>> for i in range(1, len(_s) + 3):
    ...     result = _(_s, max_len=i)
    ...     assert all(len(r) <= i for r in result), (i, result)
    """

    assert max_len >= 0

    if max_len == 0:
        return [s]

    words = s.split()
    lines: List[List[str]] = [[]]

    cur_len = 0

    def process_word(w: str):
        nonlocal cur_len

        wlen = len(w)
        slen = 1 if cur_len else 0
        next_len = cur_len + slen + wlen

        if next_len <= max_len:
            lines[-1].append(w)
            cur_len = next_len
        elif wlen <= max_len:
            lines.append([w])
            cur_len = wlen
        else:
            symbols_left = max_len - cur_len - slen
            if symbols_left <= 0:
                lines.append([])
                cur_len = 0
                process_word(w)
                return

            lines[-1].append(w[:symbols_left])

            lines.append([])
            cur_len = 0
            process_word(w[symbols_left:])

    for _w in words:
        process_word(_w)

    return [' '.join(row) for row in lines]


def split_text_to_markdown_lines(s: str, max_len: int) -> str:
    """
    adds <br> to text to split it in markdown

    >>> _ = split_text_to_markdown_lines
    >>> _('some text', max_len=3)
    'som<br />e t<br />ext'
    """
    subs = split_text(s, max_len)
    if len(subs) == 1:
        return subs[0]
    return '<br />'.join(subs)


_aligns = {
    'left': ':---',
    'center': ':---:',
    'right': '---:'
}


def get_table(
    data: Dict[str, Sequence[str]],
    max_lens: Optional[Dict[str, int]] = None,
    aligns: Optional[Dict[str, str]] = None,
    default_align: str = 'center'
) -> str:
    """
    generates markdown table depends on data and params
    Args:
        data:
        max_lens:
        aligns:
        default_align:

    Returns:

    >>> dt = dict(c1=['column 1 some text'], c2=['column 2 text'])
    >>> c3 = 'very long name for the column'
    >>> dt[c3] = ['column3 text']
    >>> al = {'c1': 'left', 'c2': 'center', c3: 'right'}
    >>> print(get_table(data=dt, aligns=al))
    | c1 | c2 | very long name for the column |
    | :--- | :---: | ---: |
    | column 1 some text | column 2 text | column3 text |
    >>> for k in list(dt.keys()):
    ...     dt[k].append('some common text')
    >>> mx = {'c1': 10, c3: 14}
    >>> print(get_table(data=dt, aligns=al, max_lens=mx))
    | c1 | c2 | very long name<br />for the column |
    | :--- | :---: | ---: |
    | column 1<br />some text | column 2 text | column3 text |
    | some<br />common<br />text | some common text | some common<br />text |

    """

    colums_to_rows_count = {k: len(v) for k, v in data.items()}
    rows_counts = set(colums_to_rows_count.values())
    if len(rows_counts) != 1:
        raise ValueError(f"rows counts mismatch: {colums_to_rows_count}")
    rows_count = rows_counts.pop()

    max_lens = max_lens or {}
    aligns = aligns or {}

    columns = set(data.keys())
    for k in max_lens.keys():
        assert k in columns, (max_lens, k, columns)
    for k, v in aligns.items():
        assert k in columns, (aligns, k, columns)
        assert v in _aligns, (aligns, v, _aligns)

    columns = {
        k: [
            split_text_to_markdown_lines(k, max_lens.get(k, 0)),
            _aligns[aligns.get(k, default_align)]
        ] + [split_text_to_markdown_lines(v, max_lens.get(k, 0)) for v in rows]
        for k, rows in data.items()
    }
    rows_count += 2

    strings = [
        '| ' + ' | '.join(columns[k][i] for k in columns.keys()) + ' |'
        for i in range(rows_count)
    ]
    return '\n'.join(strings)


class Column(TypedDict):
    label: Optional[str]
    """short column label to use in rows dicts"""
    max_len: int
    align: str


class Config(TypedDict):
    columns: Dict[str, Column]
    order: Optional[List[str]]
    rows: List[Dict[str, str]]


def get_table_from_config(
    cfg: Union[str, Config]
) -> str:
    """

    Args:
        cfg: config or path to it

    Returns:

    >>> print(get_table_from_config('./config.json'))
    | Data<br />in<br />the<br />colu<br />mn 2 | Data in<br />the column<br />1 |
    | :--- | ---: |
    | data<br />for<br />colu<br />mn 2 | data for<br />column 1 |
    | next<br />row | next row |

    """

    if isinstance(cfg, str):
        import json
        with open(cfg, 'r', encoding='utf-8') as f:
            cfg: Config = json.load(f)

    all_colums: Set[str] = set()
    name2label: Dict[str, str] = {}
    max_lens: Dict[str, int] = {}
    aligns: Dict[str, str] = {}

    def put(column_name: str, column_meta: Column, meta_key: str, target_dict: Dict):
        _v = column_meta.get(meta_key)
        if _v:
            if column_name in target_dict:
                raise ValueError(f"{column_name} column already exist in {target_dict}")
            target_dict[column_name] = _v

    for name, meta in cfg['columns'].items():
        all_colums.add(name)
        put(name, meta, 'label', name2label)
        put(name, meta, 'max_len', max_lens)
        put(name, meta, 'align', aligns)

    label2name = {v: k for k, v in name2label.items()}

    def to_column_name(s: str) -> str:
        if s in label2name:
            return label2name[s]
        return s

    order = [to_column_name(c) for c in (cfg.get('order') or [])]

    data: Dict[str, List[str]] = defaultdict(list)

    for row in cfg['rows']:
        row_keys = set()
        for k, v in row.items():
            k = to_column_name(k)
            assert k in all_colums, f"{k} is not listed in columns fields, available columns are {all_colums}"
            data[k].append(v)
            row_keys.add(k)
        unmentioned_keys = set(data.keys()) - row_keys
        for k in unmentioned_keys:
            data[k].append('')

    if order:
        assert sorted(order) == sorted(all_colums), (set(order) - all_colums, all_colums - set(order))
        data = {
            k: data[k] for k in order
        }

    return get_table(data=data, max_lens=max_lens, aligns=aligns)


#region CLI

parser = argparse.ArgumentParser(
    prog=f"{str(Path(__file__).name)}",
    description=(
        'Script for creating markdown tables using json config'
    ),
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument('CONFIG_FILE', type=str, help='json file with the configuration')

#endregion


if __name__ == '__main__':

    parsed = parser.parse_args(sys.argv[1:])

    res = get_table_from_config(
        cfg=parsed.CONFIG_FILE,
    )
    print(res)











