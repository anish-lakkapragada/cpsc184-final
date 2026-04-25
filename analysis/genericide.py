import spacy

from models import GenericideReport



nlp = spacy.load("en_core_web_sm")



def _classify(text, brand):

    brand_lower = brand.lower()
    doc = nlp(text)


    for token in doc:

        if token.lemma_.lower() != brand_lower and token.text.lower() != brand_lower:
            continue


        # rule 1: spacy NER says ORG -> branded
        if token.ent_type_ == "ORG":
            return "branded"

        # rule 2: verb -> generic ("just uber there")
        if token.pos_ == "VERB":
            return "generic"

        # rule 3: possessive -> branded ("Uber's stock")
        if token.i + 1 < len(doc) and doc[token.i + 1].text == "'s":
            return "branded"

        # rule 4: uppercase proper noun -> branded ("Uber is great")
        if token.pos_ == "PROPN" and token.text[0].isupper():
            return "branded"

        # rule 5: lowercase common noun -> generic ("call an uber")
        # but skip compound modifiers like "apple juice" or "amazon river"
        if token.pos_ == "NOUN" and token.text[0].islower() and token.dep_ != "compound":
            return "generic"

        # rule 6: indefinite article before -> generic ("need an uber")
        if token.i > 0 and doc[token.i - 1].text.lower() in ("a", "an") and token.dep_ != "compound":
            return "generic"


    return None



def analyze(brand, items):

    generic_count = 0
    branded_count = 0

    examples_generic = []
    examples_branded = []


    for mention in items:

        res = _classify(mention.text, brand)


        if res == "generic":
            generic_count = generic_count + 1
            if len(examples_generic) < 5:
                examples_generic.append(mention)

        elif res == "branded":
            branded_count = branded_count + 1
            if len(examples_branded) < 5:
                examples_branded.append(mention)


    return GenericideReport(
        brand=brand,
        generic_count=generic_count,
        branded_count=branded_count,
        examples_generic=examples_generic,
        examples_branded=examples_branded,
    )
