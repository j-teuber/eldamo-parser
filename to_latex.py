from time import perf_counter
from os import unlink
from sqlalchemy import select
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait, ALL_COMPLETED
from re import sub

from datamodel.reference import Reference
from datamodel.word import Word

from eldarin_text import language_names


def latex_escape(string: str) -> str:
    escape = [('\\', '\\textbackslash'),
              ('{', '\\{'), ('}', '\\}'),
              ('$', '\\$'), ('&', '\\&'),
              ('#', '\\#'), ('°', '\\textdegree'),
              ('^', '\\^{}'), ('_', '\\_'),
              ('~', '\\textasciitilde{}'),
              ('%', '\\%'),
              ('\u203D', '\\mytextinterrobang{}'), ('⚠', '\\mywarning{}'),
              ('\u2605', '\\mybigstar{}'), ('\u2736', '\\mybigstar{}'),
              ('<i>', '\\textit{'), ('</i>', '}'),
              ('<b>', '\\textit{'), ('</b>', '}'),
              ('<p>', ''), ('</p>', '{\\par}'),
              ('<u>', '\\ul{'), ('</u>', '}'),
              ('&lt;', r'{\textless}'), ('&gt;', r'{\textgreater}'),
              ('<blockquote>', '\\begin{quote}'), ('</blockquote>', '\\end{quote}'),
              ]
    for old, new in escape:
        string = string.replace(old, new)

    string = sub(r'<a href="([^"]*)">([^<]*)</a>', '\\\\href{\\g<1>}{\\g<2>}', string)
    string = sub(r'<a[^>]*>([^<]*)</a>', '\\g<1>', string)
    string = sub(r'<a l="([^"]*)" v="([^"]*)"/>', '\\g<2>', string)
    return string


def cut_ref(source: str) -> str:
    return source.split('.', maxsplit=1)[0]


def word_ref(w: Word) -> str:
    return f'{language_names[w.language]} \\textit{{{w.verbum}}}'


def commas(l):
    return ', '.join(l)


def ref_entry(ref: Reference) -> str:
    entry = f'{ref.verbum}'
    if ref.gloss:
        entry += f' ‘{ref.gloss}’'
    entry += f' ({cut_ref(ref.source)}):'

    if ref.cognate_left or ref.cognate_right:
        entry += 'Cognates: '
        entry += commas({word_ref(c.second_reference.parent_word) for c in ref.cognate_left}.union(
            {word_ref(c.first_reference.parent_word) for c in ref.cognate_right}
        ))

    return entry[:-1] if entry[-1] == ':' else entry


def word_entry(word, f):
    f.write('{\\par}{\\noindent}')
    f.write(latex_escape(language_names[word.language]))
    f.write(' \\textbf{\\textit{')
    f.write(latex_escape(word.verbum))
    f.write('}} \\textit{(')
    f.write(latex_escape(word.part_of_speech))
    f.write('.')

    if word.stem_form:
        f.write(', ')
        f.write(latex_escape(word.stem_form))
    if word.tengwar_hints:
        f.write(', ')
        f.write(latex_escape(word.tengwar_hints))
    f.write(')} ')

    if word.gloss:
        f.write('‘')
        f.write(latex_escape(word.gloss))
        f.write('’. ')

    for notes in word.notes:
        f.write(latex_escape(notes.text))

    if word.see_left:
        f.write('{\\par\\noindent}→ ')
        f.write(latex_escape(', '.join(
            {f'{language_names[s.second_word.language]} {s.second_word.verbum}' for s in word.see_left})))

    if word.references:
        f.write('{\\par\\noindent}\\myrefsymbol{}')
        f.write(', '.join({ref_entry(r) for r in word.references}))

    f.write('\n')


def do_language(language, session):
    with open(f'latex/{language}.tex', 'w') as f:
        statement = (select(Word)
                     .where(Word.language.in_([language]))
                     .where(Word.part_of_speech.notin_(['phrase', 'text', 'phonetic-group',
                                                        'phonetic-rule', 'phoneme', 'grammar',
                                                        'phonetics']))
                     .order_by(Word.sort_key.asc()))
        for row in session.execute(statement):
            word_entry(row[0], f)

    print(language, 'finished.')


def write_latex(session):
    languages = sorted([row[0] for row in session.query(Word.language).distinct()])
    unlink('latex/eldamo.tex')
    for language in languages:
        with open('latex/eldamo.tex', 'a') as f:
            f.write(f'\\section{{{language}}}\\input{{{language}}}\\clearpage\n')

    start = perf_counter()

    futures = []
    with ThreadPoolExecutor() as executor:
        for language in languages:
            #f = executor.submit((lambda: do_language(language, session)))
            #futures.append(f)
            print('started', language)
            do_language(language, session)

        #wait(futures, return_when=ALL_COMPLETED)

    end = perf_counter()

    print('Finished:', end - start, 'seconds')
