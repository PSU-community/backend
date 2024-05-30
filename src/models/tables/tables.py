from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, Text, UniqueConstraint, PrimaryKeyConstraint 
from sqlalchemy.sql import func as server_func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects import postgresql

from src.database.base import BaseTable, int_pk, str_128
from src.models.enums import MediaTypes, PersonalInformationTypes
from src.models.schemas.content import (
    CategorySchema,
    MediaFileSchema, SubCategorySchema,
    PostSchema,
    PersonalInformationSchema,
)
from src.models.schemas.guide import GuideSchema
from src.models.schemas.tests import TestQuestion, TestQuestionAnswer, TestResult, TestSchema, UserTestAnswer, UserTestResultSchema
from src.models.tables.users import UserTable


class CategoryTable(BaseTable):
    __tablename__ = "categories"

    id: Mapped[int_pk]
    name: Mapped[str_128]

    subcategories: Mapped[list["SubCategoryTable"]] = relationship(
        back_populates="category",
        lazy="noload",
    )
    post: Mapped[Optional["PostTable"]] = relationship(
        back_populates="category",
        lazy="noload",
        primaryjoin="and_(CategoryTable.id == PostTable.category_id, PostTable.subcategory_id == None)"
    )
 
    def to_schema_model(self, *, load_subcategories: bool = False, load_subcategories_posts: bool = False, load_post: bool = False):
        return CategorySchema(
            id=self.id,
            name=self.name,
            subcategories=[subcategory.to_schema_model(load_post=load_subcategories_posts) for subcategory in self.subcategories] if load_subcategories and self.subcategories else None,
            post=self.post.to_schema_model(load_category=False, load_subcategory=False) if load_post and self.post else None,
        )


class SubCategoryTable(BaseTable):
    __tablename__ = "subcategories"

    id: Mapped[int_pk]
    category_id: Mapped[int] = mapped_column(ForeignKey(CategoryTable.id, ondelete="CASCADE"))
    name: Mapped[str_128]

    category: Mapped["CategoryTable"] = relationship(
        back_populates="subcategories",
        lazy="noload",
    )
    post: Mapped["PostTable"] = relationship(back_populates="subcategory", lazy="noload")

    def to_schema_model(self, *, load_post: bool = False, load_category: bool = False):
        return SubCategorySchema(
            id=self.id,
            category_id=self.category_id,
            name=self.name,
            category=self.category.to_schema_model() if load_category and self.category else None,
            post=self.post.to_schema_model() if load_post and self.post else None,
        )


class PostTable(BaseTable):
    __tablename__ = "posts"

    id: Mapped[int_pk]
    category_id: Mapped[int] = mapped_column(ForeignKey(CategoryTable.id, ondelete="CASCADE"), default=None)
    subcategory_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(SubCategoryTable.id, ondelete="CASCADE"),
        nullable=True,
        default=None
    )
    content: Mapped[str] = mapped_column(Text, default=None)
    views: Mapped[int] = mapped_column(default=0)

    category: Mapped["CategoryTable"] = relationship(back_populates="post", lazy="noload")
    subcategory: Mapped[Optional["SubCategoryTable"]] = relationship(back_populates="post", lazy="noload")

    __table_args__ = (
        UniqueConstraint("category_id", "subcategory_id", name="unique_post"),
    )

    def to_schema_model(self, *, load_category: bool = False, load_subcategory: bool = False, load_category_subcategories: bool = False, load_subcategories_posts: bool = False):
        return PostSchema(
            id=self.id,
            category_id=self.category_id,
            subcategory_id=self.subcategory_id,
            content=self.content,
            views=self.views,
            category=self.category.to_schema_model(load_subcategories=load_category_subcategories, load_subcategories_posts=load_subcategories_posts) if load_category and self.category else None,
            subcategory=self.subcategory.to_schema_model() if load_subcategory and self.subcategory else None
        )


class MediaFileTable(BaseTable):
    __tablename__ = "media_files"

    id: Mapped[int_pk]
    type: Mapped[int]
    file_name: Mapped[Optional[str_128]] = mapped_column(default=None)
    file_url: Mapped[Optional[str_128]] = mapped_column(default=None)
    data: Mapped[Optional[str]] = mapped_column(Text, default=None)

    def to_schema_model(self, is_nested: bool = False):
        return MediaFileSchema(
            id=self.id,
            file_name=self.file_name,
            file_url=self.file_url,
            type=MediaTypes(self.type),
            data=self.data,
        )


class PersonalInformationTable(BaseTable):
    __tablename__ = "personal_information"

    id: Mapped[int_pk]
    post_id: Mapped[int] = mapped_column(ForeignKey(PostTable.id))
    user_id: Mapped[int] = mapped_column(ForeignKey(UserTable.id))
    content_type: Mapped[PersonalInformationTypes] = mapped_column(
        postgresql.ENUM(PersonalInformationTypes)
    )
    content: Mapped[Optional[str]] = mapped_column(default=None)

    post: Mapped["PostTable"] = relationship(lazy="noload")

    def to_schema_model(self, load_post: bool = False, load_category: bool = False, load_subcategory: bool = False):
        return PersonalInformationSchema(
            id=self.id,
            post_id=self.post_id,
            user_id=self.user_id,
            content_type=self.content_type,
            content=self.content,
            post=self.post.to_schema_model(load_category=load_category, load_subcategory=load_subcategory) if load_post else None,
        )


class GuideTable(BaseTable):
    __tablename__ = "guide"

    id: Mapped[int_pk]
    name: Mapped[str_128]
    content: Mapped[str]

    def to_schema_model(self) -> BaseModel:
        return GuideSchema(
            id=self.id,
            name=self.name,
            content=self.content,
        )


class TestQuestionAnswerTable(BaseTable):
    __tablename__ = "test_question_answers"

    id: Mapped[int_pk]
    test_question_id: Mapped[int] = mapped_column(ForeignKey("test_questions.id", ondelete="CASCADE"))
    answer: Mapped[str]
    points: Mapped[int]

    def to_schema_model(self) -> TestQuestionAnswer:
        return TestQuestionAnswer(
            id=self.id,
            test_question_id=self.test_question_id,
            answer=self.answer,
            points=self.points,
        )


class TestQuestionTable(BaseTable):
    __tablename__ = "test_questions"

    id: Mapped[int_pk]
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id", ondelete="CASCADE"))
    title: Mapped[str]
    type: Mapped[int]

    answers: Mapped[list["TestQuestionAnswerTable"]] = relationship(lazy="noload")

    def to_schema_model(self) -> TestQuestion:
        return TestQuestion(
            id=self.id,
            test_id=self.test_id,
            title=self.title,
            type=self.type,
            answers=[answer.to_schema_model() for answer in self.answers]
        )


class TestResultTable(BaseTable):
    __tablename__ = "test_results"

    id: Mapped[int_pk]
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id", ondelete="CASCADE"))
    min_points: Mapped[int]
    max_points: Mapped[int]
    content: Mapped[str]

    def to_schema_model(self) -> TestResult:
        return TestResult(
            id=self.id,
            test_id=self.test_id,
            min_points=self.min_points,
            max_points=self.max_points,
            content=self.content,
        )


class TestTable(BaseTable):
    __tablename__ = "tests"

    id: Mapped[int_pk]
    name: Mapped[str_128]

    questions: Mapped[list["TestQuestionTable"]] = relationship(lazy="noload")
    results: Mapped[list["TestResultTable"]] = relationship(lazy="noload")

    def to_schema_model(self) -> TestSchema:
        return TestSchema(
            id=self.id,
            name=self.name,
            questions=[q.to_schema_model() for q in self.questions],
            results=[r.to_schema_model() for r in self.results]
        )


class UserTestResultTable(BaseTable):
    __tablename__ = "user_test_results"

    id: Mapped[int_pk]
    test_id: Mapped[int] = mapped_column(ForeignKey(TestTable.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(UserTable.id, ondelete="CASCADE"))
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=server_func.now())

    answers: Mapped[list["UserTestAnswerTable"]] = relationship(lazy="noload")

    def to_schema_model(self) -> UserTestResultSchema:
        return UserTestResultSchema(
            id=self.id,
            test_id=self.test_id,
            user_id=self.user_id,
            date=self.date,
            answers=[a.to_schema_model() for a in self.answers]
        )


class UserTestAnswerTable(BaseTable):
    __tablename__ = "user_test_answer"

    user_test_result_id: Mapped[int] = mapped_column(ForeignKey("user_test_results.id", ondelete="CASCADE"))
    question_id: Mapped[int] = mapped_column(ForeignKey("test_questions.id", ondelete="CASCADE"))
    answer_id: Mapped[int] = mapped_column(ForeignKey("test_question_answers.id", ondelete="CASCADE"))

    __table_args__ = (
        PrimaryKeyConstraint("user_test_result_id", "question_id", "answer_id", name="user_test_answer_pk"),
    )

    def to_schema_model(self) -> UserTestAnswer:
        return UserTestAnswer(
            user_test_result_id=self.user_test_result_id,
            question_id=self.question_id,
            answer_id=self.answer_id
        )
