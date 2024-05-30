from datetime import datetime
from enum import IntEnum
from typing import Optional
from pydantic import BaseModel, Field


class TestTypes(IntEnum):
    SINGLE_ANSWER_OPTION = 1
    TEXT_FIELD = 2


class TestQuestionAnswer(BaseModel):
    id: Optional[int] = Field(default=None)
    test_question_id: Optional[int] = Field(default=None)
    answer: str
    points: int


class TestQuestion(BaseModel):
    id: Optional[int] = Field(default=None)
    test_id: Optional[int] = Field(default=None)
    title: str
    type: TestTypes

    answers: list[TestQuestionAnswer]


class TestResult(BaseModel):
    id: Optional[int] = Field(default=None)
    test_id: Optional[int] = Field(default=None)
    min_points: int
    max_points: int
    content: str

    test: Optional["TestSchema"] = Field(default=None)


class TestSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str

    questions: list[TestQuestion]
    results: list[TestResult]


class UserTestAnswer(BaseModel):
    user_test_result_id: Optional[int] = Field(default=None)
    question_id: int
    answer_id: int


class UserTestResultSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    test_id: int
    user_id: int
    date: datetime

    answers: list[UserTestAnswer]