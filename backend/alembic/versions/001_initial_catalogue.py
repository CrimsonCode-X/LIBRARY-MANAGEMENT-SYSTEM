"""initial catalogue

Revision ID: 001_initial_catalogue
Revises:
Create Date: 2026-09-08
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001_initial_catalogue"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("canonical_title", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("publication_year", sa.Integer()),
        sa.Column("language", sa.String(length=32)),
        sa.Column("cover_url", sa.String(length=1000)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_books_canonical_title", "books", ["canonical_title"])
    op.create_index("ix_books_language", "books", ["language"])

    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=300), nullable=False, unique=True),
    )
    op.create_index("ix_authors_name", "authors", ["name"])

    op.create_table(
        "book_authors",
        sa.Column("book_id", sa.Integer(), sa.ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider", sa.String(length=64), nullable=False, unique=True),
    )

    op.create_table(
        "book_sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("book_id", sa.Integer(), sa.ForeignKey("books.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_id", sa.Integer(), sa.ForeignKey("sources.id", ondelete="CASCADE"), nullable=False),
        sa.Column("external_id", sa.String(length=128), nullable=False),
        sa.Column("source_url", sa.String(length=1000)),
        sa.Column("reading_url", sa.String(length=1000)),
        sa.Column("access_type", sa.String(length=32), nullable=False),
        sa.Column("formats", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("metadata_json", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("last_checked_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("source_id", "external_id", name="uq_book_source_external"),
    )
    op.create_index("ix_book_sources_book_id", "book_sources", ["book_id"])


def downgrade() -> None:
    op.drop_index("ix_book_sources_book_id", table_name="book_sources")
    op.drop_table("book_sources")
    op.drop_table("sources")
    op.drop_table("book_authors")
    op.drop_index("ix_authors_name", table_name="authors")
    op.drop_table("authors")
    op.drop_index("ix_books_language", table_name="books")
    op.drop_index("ix_books_canonical_title", table_name="books")
    op.drop_table("books")
