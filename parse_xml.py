from typing import Optional
from xml.etree.ElementTree import parse

from datamodel.notes import Note
from datamodel.word import Word
from datamodel.reference import Reference
from datamodel.cognate import CognateWords, CognateReferences
from datamodel.deprecated import DeprecatedWord
from datamodel.derive import DeriveWords, DeriveReferences
from datamodel.element import ElementWords, ElementReferences
from datamodel.inflect import InflectReference
from datamodel.related import RelatedWords, RelatedReferences
from datamodel.see_crossref import SeeCrossref
from eldarin_text import canonical


def word_id(xml):
    return f'{xml.get('l')}@{xml.get('v')}'


def unblank(string: str) -> Optional[str]:
    return None if string is None or string.isspace() else string.strip()


counter = 0


def next_id():
    global counter
    counter += 1
    return counter


def insert_references(xml, parent, session):
    ref = Reference(
        source=xml.get('source'),
        parent_word=parent,
        reference_language=xml.get('l'),
        verbum=xml.get('v'),
        gloss=xml.get('gloss'),
        mark=xml.get('mark')
    )
    session.add(ref)

    for cognate in xml.findall('./cognate'):
        session.add(CognateReferences(
            id=next_id(),
            first_reference=ref,
            second_ref_id=cognate.get('source'),
            mark=cognate.get('mark'),
            text=unblank(cognate.text)
        ))

    for derive in xml.findall('./deriv'):
        session.add(DeriveReferences(
            id=next_id(),
            first_reference=ref, second_ref_id=derive.get('source'),
            mark=derive.get('mark'), text=unblank(derive.text),
            intermediate1=derive.get('i1'), intermediate2=derive.get('i2'),
            intermediate3=derive.get('i3'),
        ))

    for element in xml.findall('./element'):
        session.add(ElementReferences(
            id=next_id(), first_reference=ref, second_ref_id=element.get('source'),
            mark=element.get('mark'), text=unblank(element.text),
            form=element.get('form'), variant=element.get('variant'),
        ))

    for inflect in xml.findall('./inflect'):
        session.add(InflectReference(
            id=next_id(), first_reference=ref, second_ref_id=inflect.get('source'),
            text=unblank(inflect.text), form=inflect.get('form'), variant=inflect.get('variant'),
        ))

    for related in xml.findall('./related'):
        session.add(RelatedReferences(
            id=next_id(), first_reference=ref, second_ref_id=related.get('source'),
            mark=related.get('mark'), text=unblank(related.text),
        ))


def insert_word(xml, parent, session):
    word = Word(
        id=word_id(xml),
        language=xml.get('l'),
        verbum=xml.get('v'),
        sort_key=canonical(xml.get('v')),
        part_of_speech=xml.get('speech'),
        mark=xml.get('mark'),
        gloss=xml.get('gloss'),
        stem_form=xml.get('stem'),
        tengwar_hints=xml.get('tengwar'),
        neo_gloss=xml.get('ngloss'),
        neo_creator=xml.get('created'),
        neo_version=xml.get('neo-version'),
        page_id=xml.get('page-id'),
        vetted_by=xml.get('vetted'),
        semantic_category=xml.get('cat'),
    )
    if isinstance(parent, Word):
        parent.child_words.append(word)
    session.add(word)

    for child_word in xml.findall('./word'):
        insert_word(child_word, word, session)

    for note in xml.findall('./notes'):
        session.add(Note(id=next_id(), word=word, text=note.text))

    for ref in xml.findall('./ref'):
        insert_references(ref, word, session)

    for cognate in xml.findall('./cognate'):
        session.add(CognateWords(
            id=next_id(),
            first_word=word,
            second_word_id=word_id(cognate),
            mark=cognate.get('mark'),
            text=unblank(cognate.text)
        ))

    for deprecation in xml.findall('./deprecated'):
        session.add(DeprecatedWord(id=next_id(), first_word=word, second_word_id=word_id(deprecation)))

    for derive in xml.findall('./deriv'):
        session.add(DeriveWords(
            id=next_id(),
            first_word=word, second_word_id=word_id(derive),
            mark=derive.get('mark'), text=unblank(derive.text)))

    for element in xml.findall('./element'):
        session.add(ElementWords(
            id=next_id(), first_word=word, second_word_id=word_id(element),
            mark=element.get('mark'), text=unblank(element.text),
            form=element.get('form'), variant=element.get('variant'),
        ))

    for related in xml.findall('./related'):
        session.add(RelatedWords(
            id=next_id(), first_word=word, second_word_id=word_id(related),
            mark=related.get('mark'), text=unblank(related.text),
        ))

    for tag in ('see', 'see-also', 'see-further', 'see-notes'):
        for see in xml.findall(f'./{tag}'):
            session.add(SeeCrossref(
                id=next_id(), first_word=word, second_word_id=word_id(see), type=tag
            ))


def handle_top_level(xml, session):
    for word in xml.findall('./word'):
        if word.tag == 'word':
            insert_word(word, None, session)


def parse_xml(xml_file, session):
    xml = parse(xml_file)
    handle_top_level(xml, session)
