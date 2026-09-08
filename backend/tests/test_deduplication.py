from app.providers.base import BookSource, UnifiedBook
from app.services.deduplication import canonical_key, merge_books, normalize_text


def test_normalize_text():
    assert normalize_text("The Hobbit: There & Back Again") == "thehobbittherebackagain"


def test_same_book_merges_sources():
    first = UnifiedBook(
        title="The Hobbit",
        authors=["J. R. R. Tolkien"],
        publication_year=1937,
        sources=[BookSource("openlibrary", "OL1")],
    )
    second = UnifiedBook(
        title="The Hobbit",
        authors=["J.R.R. Tolkien"],
        publication_year=1937,
        sources=[BookSource("gutenberg", "PG1")],
    )
    result = merge_books([first, second])
    assert len(result) == 1
    assert {source.provider for source in result[0].sources} == {"openlibrary", "gutenberg"}


def test_canonical_key_is_stable_for_title_and_author_formatting():
    a = UnifiedBook(title="The Hobbit", authors=["J. R. R. Tolkien"], publication_year=1937)
    b = UnifiedBook(title="the-hobbit", authors=["JRR Tolkien"], publication_year=1937)
    assert canonical_key(a) == canonical_key(b)
