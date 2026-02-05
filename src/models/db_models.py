"""SQLAlchemy database models for DataCatalog AI."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    pass


class User(Base, UUIDMixin, TimestampMixin):
    """User model for authentication."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="viewer", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


class DataSource(Base, UUIDMixin, TimestampMixin):
    """Data source connection model."""

    __tablename__ = "data_sources"

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )  # postgres, mysql, bigquery, etc.
    connection_string: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )  # Should be encrypted in production
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    tables: Mapped[list["Table"]] = relationship(
        back_populates="data_source",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<DataSource(id={self.id}, name={self.name}, type={self.source_type})>"


class Table(Base, UUIDMixin, TimestampMixin):
    """Table metadata model."""

    __tablename__ = "tables"

    data_source_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("data_sources.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    schema_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    row_count: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # Relationships
    data_source: Mapped["DataSource"] = relationship(back_populates="tables")
    columns: Mapped[list["Column"]] = relationship(
        back_populates="table",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Table(id={self.id}, name={self.schema_name}.{self.name})>"


class Column(Base, UUIDMixin, TimestampMixin):
    """Column metadata model."""

    __tablename__ = "columns"

    table_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tables.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    data_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_nullable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_primary_key: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ordinal_position: Mapped[int] = mapped_column(default=0, nullable=False)

    # Relationships
    table: Mapped["Table"] = relationship(back_populates="columns")

    def __repr__(self) -> str:
        return f"<Column(id={self.id}, name={self.name}, type={self.data_type})>"
