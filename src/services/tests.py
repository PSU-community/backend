import datetime
from src.models.schemas.create import TestCreate, UserTestResultCreate
from src.models.schemas.tests import TestQuestion, TestQuestionAnswer, TestResult, TestSchema
from src.models.schemas.update import TestUpdate
from src.repositories.tests_repository import (
    TestQuestionAnswerRepository,
    TestQuestionRepository,
    TestResultRepository,
    TestRepository,
    UserTestResultRepository,
    UserTestAnswerRepository
)


class TestsService:
    def __init__(self) -> None:
        self.test_question_answer_repo = TestQuestionAnswerRepository()
        self.test_question_repo = TestQuestionRepository()
        self.test_result_repo = TestResultRepository()
        self.test_repo = TestRepository()
        self.user_test_result_repo = UserTestResultRepository()
        self.user_test_answer_repo = UserTestAnswerRepository()

    async def get_test_list(self) -> list[TestSchema]:
        return await self.test_repo.get_all()
    
    async def get_test_by_id(self, id: int) -> TestSchema:
        return await self.test_repo.get_by_id(id)

    async def add_test(self, create: TestCreate):
        test_payload = create.model_dump(exclude={"questions", "results"}, exclude_none=True)
        test = await self.test_repo.add_one(test_payload)

        for question_create in create.questions:
            question_payload = question_create.model_dump(exclude={"answers"}, exclude_none=True)
            question = await self.test_question_repo.add_one({**question_payload, "test_id": test.id})

            answers_payloads = [
                {**ac.model_dump(exclude_none=True), "test_question_id": question.id} for ac in question_create.answers
            ]
            await self.test_question_answer_repo.add_many(answers_payloads)

        await self.__add_results(test.id, create.results)

    async def __add_results(self, test_id: int, results: list[TestResult]):
        results_payloads = [
            {**rc.model_dump(exclude_none=True), "test_id": test_id} for rc in results
        ]
        await self.test_result_repo.add_many(results_payloads)

    async def __add_question(self, test_id: int, question: TestQuestionAnswer):
        question_payload = question.model_dump(exclude={"answers"}, exclude_none=True)
        return await self.test_question_repo.add_one({**question_payload, "test_id": test_id})

    async def __delete_question(self, question_id: int):
        await self.test_question_repo.remove_by_id(question_id)

    async def __add_answers(self, question_id: int, answers: list[TestQuestionAnswer]):
        answers_payloads = [
                {**ac.model_dump(exclude_none=True), "test_question_id": question_id} for ac in answers
            ]
        await self.test_question_answer_repo.add_many(answers_payloads)

    async def __update_answer(self, answer: TestQuestionAnswer):
        answer_payload = answer.model_dump(exclude={"id", "test_question_id"}, exclude_none=True)
        await self.test_question_answer_repo.update_by_id(answer.id, answer_payload)

    async def __delete_answer(self, answer_id: int):
        await self.test_question_answer_repo.remove_by_id(answer_id)

    async def __update_question(self, question: TestQuestion):
        question_payload = question.model_dump(exclude={"id", "answers", "test_id"}, exclude_none=True)
        await self.test_question_repo.update_by_id(question.id, question_payload)

    async def update_test(self, id: int, update: TestUpdate):
        print(update.model_dump_json())
        test_payload = update.model_dump(exclude={"id", "questions", "results"}, exclude_none=True)
        await self.test_repo.update_by_id(id, test_payload)
        test: TestSchema = await self.test_repo.get_by_id(id)

        for question_update in update.questions:
            if question_update.id is not None:
                await self.__update_question(question_update)

                for answer_update in question_update.answers:
                    if answer_update.id is not None:
                        await self.__update_answer(answer_update)
                new_answers = list(filter(lambda ans: ans.id is None, question_update.answers))
                if new_answers:
                        await self.__add_answers(question_update.id, new_answers)

                # Поиск удалённых из обновления ответов и удаление их из бд
                question = next(filter(lambda q: q.id == question_update.id, test.questions)) 
                if len(question.answers) > len(question_update.answers):
                    old_answ = set(map(lambda q: q.id, question.answers))
                    answ = set(map(lambda q: q.id, question_update.answers))
                    to_remove = old_answ.difference(answ)
                    for id in to_remove:
                        await self.__delete_answer(id)
            else:
                question = await self.__add_question(test.id, question_update)
                await self.__add_answers(question.id, question_update.answers)
        
        if len(test.questions) > len(update.questions):
            old_quests = set(map(lambda q: q.id, test.questions))
            quests = set(map(lambda q: q.id, update.questions))
            to_remove = old_quests.difference(quests)
            for id in to_remove:
                await self.__delete_question(id)

        for result_update in update.results:
            if result_update.id:
                result_payload = result_update.model_dump(exclude={"id", "test_id"}, exclude_none=True)
                await self.test_result_repo.update_by_id(result_update.id, result_payload)

        new_results = list(filter(lambda res: res.id is None, update.results))
        if new_results:
            await self.__add_results(test.id, new_results)

    async def delete_test(self, id: int):
        await self.test_repo.remove_by_id(id)

    async def add_user_test_result(self, create: UserTestResultCreate):
        result_payload = create.model_dump(exclude={"answers"}, exclude_none=True)
        user_test_result = await self.user_test_result_repo.add_one(result_payload)

        answer_payloads = [{**a.model_dump(), "user_test_result_id": user_test_result.id} for a in create.answers]
        await self.user_test_answer_repo.add_many(answer_payloads)

        return await self.test_result_repo.get_test_result(user_test_result.id)
    
    async def get_user_test_results(self, user_id: int):
        # Это можно было бы сделать в одном запросе, но я чувствую, что у меня поедет крыша

        user_test_result_list: list[TestResult] = await self.user_test_result_repo.get_many(user_id=user_id)
        test_results = []

        for user_test_result in user_test_result_list:
            test_result = await self.test_result_repo.get_test_result(user_test_result.id)
            test_result.test = await self.test_repo.get_by_id(user_test_result.test_id)
            test_results.append(test_result)

        return test_results



