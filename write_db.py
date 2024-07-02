from os import unlink
from sqlite3 import connect
from xml.etree.ElementTree import parse

eldamo_data = parse('eldamo-data.xml')
unlink('eldamo-db.sqlite3')
db = connect('eldamo-db.sqlite3')
cursor = db.cursor()

cursor.execute("""create table words(
    page_id not null unique, 
    language not null, word_form not null, 
    stem_form, mark, tengwar, part_of_speech, 
    gloss, semantic_category, neo_gloss, neo_version,neo_creator, vetted_by,
    phonetic_rule_from, phonetic_rule_to, 
    phoneme_order, phoneme_orthography, phoneme_column, phoneme_row,
    parent,
    primary key (language, word_form))""")

cursor.execute('create table word_class(lang, word, form, variant)')

cursor.execute("""create table relation_word(
type, 
first_lang, first_word, 
second_lang, second_word, 
mark,
form, variant, text)""")

cursor.execute("""create table relation_refs(
type,
first_source, first_word,
second_source, second_word,
mark, example_type, form, variant,
intermediate1, intermediate2, intermediate3,
text
)""")

cursor.execute("""create table language_metadata(lang_id, type, text)""")

cursor.execute("""create table word_inflect(lang, word, form, variant, source_word, source)""")

cursor.execute("""create table word_notes(lang, word, text)""")

cursor.execute("""create table refs(
source, parent_lang, parent_word, ref_lang, word_form, gloss, mark, rule_lang, rule_to, rule_from)""")

cursor.execute("""create table rule_example (
first_source, first_word,
second_source, second_word,
sort, rule_lang, rule_to, rule_form,
stage
)""")

cursor.execute("""create table rule_start (
first_source, first_word,
second_source, second_word,
stage
)""")

cursor.execute("""create table semantic_categories (id, parent, label, num)""")
cursor.execute("""create table semantic_parents (id, label, num)""")

cursor.execute("""create table sources (name, prefix, type, cite, note)""")

cursor.execute("""create table rule_components (word_lang, word_form, rule_lang, rule_to, rule_from)""")
cursor.execute("""create table order_examples (first_lang, first_word, second_lang, second_word, source, ref_form)""")


def warning(child, parent):
    print(f'unrecognized: {child.tag} {child.attrib} in {parent.tag} {parent.attrib}')


def insert_word(word, parent):
    cursor.execute(
        "insert into words values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            word.get('page-id'),
            word.get('l'),
            word.get('v'),
            word.get('stem'),
            word.get('mark'),
            word.get('tengwar'),
            word.get('speech'),
            word.get('gloss'),
            word.get('cat'),
            word.get('ngloss'),
            word.get('neo-version'),
            word.get('created'),
            word.get('vetted'),
            word.get('from'),
            word.get('rule'),
            word.get('order'),
            word.get('orthography'),
            word.get('phone-col'),
            word.get('phone-row'),
            parent.get('page-id')
        )
    )


def insert_word_class(tag, word):
    cursor.execute(
        """insert into word_class values (?, ?, ?, ?)""",
        (
            word.get('l'),
            word.get('v'),
            tag.get('form'),
            tag.get('variant')))


def insert_language_metadata(lang, type, text):
    cursor.execute(
        """insert into language_metadata values (?,?,?)""",
        (lang, type, text)
    )


def insert_inflect_word(tag, word):
    cursor.execute(
        """insert into word_inflect values (?,?,?,?,?,?)""",
        (
            word.get('l'),
            word.get('v'),
            tag.get('form'),
            tag.get('variant'),
            tag.get('v'),
            tag.get('source')
        )
    )


def insert_word_note(tag, word):
    cursor.execute(
        """insert into word_notes values (?,?,?)""",
        (
            word.get('l'),
            word.get('v'),
            tag.text
        )
    )


def insert_ref(tag, word):
    cursor.execute(
        """insert into refs values (?,?,?,?,?,?,?,?,?,?)""",
        (
            tag.get('source'),
            word.get('l'),
            word.get('v'),
            tag.get('l'),
            tag.get('v'),
            tag.get('gloss'),
            tag.get('mark'),
            tag.get('rl'),
            tag.get('rule'),
            tag.get('from')
        )
    )


def insert_word_related(type, tag, word):
    cursor.execute(
        """insert into relation_word values (?,?,?,?,?,?,?,?,?)""",
        (
            type,
            word.get('l'),
            word.get('v'),
            tag.get('l'),
            tag.get('v'),
            tag.get('mark'),
            tag.get('form'),
            tag.get('variant'),
            tag.text
        )
    )


def insert_ref_related(type, tag, ref):
    cursor.execute(
        """insert into relation_refs values (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            type,
            ref.get('source'),
            ref.get('v'),
            tag.get('source'),
            tag.get('v'),
            tag.get('mark'),
            tag.get('t'),
            tag.get('form'),
            tag.get('variant'),
            tag.get('i1'),
            tag.get('i2'),
            tag.get('i3'),
            tag.text
        )
    )


rule_application_sort = 0


def insert_rule_example(first_source, first_word, second_source, second_word, tag):
    global rule_application_sort
    rule_application_sort += 1
    cursor.execute(
        """insert into rule_example values (?,?,?,?,?,?,?,?,?)""",
        (
            first_source,
            first_word,
            second_source,
            second_word,
            rule_application_sort,
            tag.get('l'),
            tag.get('rule'),
            tag.get('from'),
            tag.get('stage')
        )
    )


def insert_rule_start(first_source, first_word, second_source, second_word, tag):
    cursor.execute(
        """insert into rule_start values (?,?,?,?,?)""",
        (
            first_source,
            first_word,
            second_source,
            second_word,
            tag.get('stage')
        )
    )


def insert_semantic_category(cat, parent):
    cursor.execute(
        """insert into semantic_categories values (?,?,?,?)""",
        (
            cat.get('id'),
            parent.get('id'),
            cat.get('label'),
            cat.get('num')
        )
    )


def insert_semantic_parent(cat):
    cursor.execute(
        """insert into semantic_parents values (?,?,?)""",
        (
            cat.get('id'),
            cat.get('label'),
            cat.get('num')
        )
    )


def insert_source(source):
    cite = source.find('cite')
    note = source.find('notes')
    cursor.execute(
        """insert into sources values (?,?,?,?,?)""",
        (
            source.get('name'),
            source.get('prefix'),
            source.get('type'),
            None if cite is None else cite.text,
            None if note is None else note.text
        )
    )


def insert_rule_component(rule_component, word):
    cursor.execute(
        """insert into rule_components values (?,?,?,?,?)""",
        (
            word.get('l'),
            word.get('v'),
            rule_component.get('l'),
            rule_component.get('rule'),
            rule_component.get('from'),
        )
    )


def insert_order_example(first_source, first_word, second_source, second_word, tag):
    cursor.execute(
        """insert into order_examples values (?,?,?,?,?,?)""",
        (
            first_source,
            first_word,
            second_source,
            second_word,
            tag.get('source'),
            tag.get('v')
        )
    )


word_relation_names = ('cognate',
                       'combine',
                       'deprecated',
                       'deriv',
                       'element',
                       'related',
                       'see',
                       'see-also',
                       'see-further',
                       'see-notes',
                       'before')

ref_relation_names = ('change',
                      'cognate',
                      'correction',
                      'deriv',
                      'element',
                      'example',
                      'inflect',
                      'related')

language_metadata = ('deprecations',
                     'grammar',
                     'names',
                     'neologisms',
                     'notes',
                     'phonetics',
                     'phrases',
                     'roots',
                     'words',
                     'vocabulary'
                     )


def handle_inside_deriv(ref, deriv, tag):
    if tag.tag == 'rule-example':
        insert_rule_example(ref.get('source'), ref.get('v'), deriv.get('source'), deriv.get('v'), tag)
    elif tag.tag == 'rule-start':
        insert_rule_start(ref.get('source'), ref.get('v'), deriv.get('source'), deriv.get('v'), tag)
    else:
        warning(tag, ref)


def handle_elements(parent):
    for child in parent.findall('./*'):
        if child.tag == 'word':
            insert_word(child, parent)
        elif child.tag == 'class' and parent.tag == 'word':
            insert_word_class(child, parent)
        elif child.tag in word_relation_names and parent.tag == 'word':
            insert_word_related(child.tag, child, parent)
            if child.tag == 'before':
                for grandchild in child.findall('order-example'):
                    insert_order_example(
                        parent.get('l'), parent.get('v'), child.get('l'), child.get('v'), grandchild)
        elif child.tag == 'inflect' and parent.tag == 'word':
            insert_inflect_word(child, parent)
        elif child.tag == 'notes' and parent.tag == 'word':
            insert_word_note(child, parent)
        elif child.tag == 'ref' and parent.tag == 'word':
            insert_ref(child, parent)
        elif child.tag == 'rule' and parent.tag == 'word':
            insert_rule_component(child, parent)
        elif child.tag in ref_relation_names and parent.tag == 'ref':
            insert_ref_related(child.tag, child, parent)
            if child.tag == 'deriv':
                for grandchild in child.findall('./*'):
                    handle_inside_deriv(parent, child, grandchild)
        elif child.tag == 'language':
            insert_language_metadata(child.get('id'), 'name', child.get('name'))
            if parent.tag == 'language':
                insert_language_metadata(child.get('id'), 'child-of', parent.get('id'))
        elif child.tag in language_metadata and parent.tag == 'language':
            insert_language_metadata(parent.get('id'), child.tag, child.text)

        elif child.tag == 'cat' and parent.tag == 'cat-group':
            insert_semantic_category(child, parent)
        elif child.tag == 'cat-group':
            insert_semantic_parent(child)

        elif child.tag == 'source':
            insert_source(child)

        elif child.tag not in ('rule-start', 'rule-example', 'cite', 'notes',
                               'order-example', 'form', 'inflect-table',
                               'derivatives', 'language-cat', 'cats'):
            warning(child, parent)

        handle_elements(child)


handle_elements(eldamo_data.getroot())
db.commit()
