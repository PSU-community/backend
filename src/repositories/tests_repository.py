from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func

from src.models.tables.tables import TestTable, TestQuestionAnswerTable, TestQuestionTable, TestResultTable, UserTestResultTable, UserTestAnswerTable
from src.models.schemas.tests import TestResult
from src.utils.abstract.db_repository import SQLAlchemyRepository
from src.database.session import async_session_maker

class TestQuestionAnswerRepository(SQLAlchemyRepository):
    table_model = TestQuestionAnswerTable


class TestQuestionRepository(SQLAlchemyRepository):
    table_model = TestQuestionTable

    options = [selectinload(TestQuestionTable.answers)]


class TestResultRepository(SQLAlchemyRepository):
    table_model = TestResultTable

    async def get_test_result(self, user_test_result_id: int) -> TestResult:
        async with async_session_maker() as session:
            points_sum_stmt = (
                select(func.sum(TestQuestionAnswerTable.points))
                .filter(
                    TestQuestionAnswerTable.id.in_(
                        select(UserTestAnswerTable.answer_id)
                        .where(UserTestAnswerTable.user_test_result_id==user_test_result_id)
                    )
                )
            )
            points_sum = points_sum_stmt.label("user_sum")
            select_test_result_with_sum = (
                select(
                    TestResultTable,
                    points_sum,
                )
                .where(and_(points_sum >= TestResultTable.min_points, points_sum <= TestResultTable.max_points) )

            )
            res = await session.execute(select_test_result_with_sum)
            return res.scalar_one().to_schema_model()


class TestRepository(SQLAlchemyRepository):
    table_model = TestTable

    options = [
        selectinload(TestTable.questions).selectinload(TestQuestionTable.answers),
        selectinload(TestTable.results)
    ]


class UserTestResultRepository(SQLAlchemyRepository):
    table_model = UserTestResultTable

    options = [selectinload(UserTestResultTable.answers)]


class UserTestAnswerRepository(SQLAlchemyRepository):
    table_model = UserTestAnswerTable