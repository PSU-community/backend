from fastapi import APIRouter

from src.api.dependencies import ICurrentUser, TestsServiceDep, IAdminUser
from src.models.schemas.create import TestCreate, UserTestResultCreate, UserTestResultRequest
from src.models.schemas.tests import TestSchema
from src.models.schemas.update import TestUpdate

router = APIRouter(tags=["Психологические тесты"])


@router.get("/tests/list")
async def get_test_list(service: TestsServiceDep) -> list[TestSchema]:
    return await service.get_test_list()


@router.get("/tests/{test_id}")
async def get_test_by_id(test_id: int, service: TestsServiceDep) -> TestSchema | None:
    return await service.get_test_by_id(test_id)


@router.post("/tests")
async def add_test(test_create: TestCreate, user: IAdminUser, service: TestsServiceDep):
    await service.add_test(test_create)


@router.patch("/tests/{test_id}")
async def update_test(test_id: int, test_update: TestUpdate, user: IAdminUser, service: TestsServiceDep):
    await service.update_test(test_id, test_update)


@router.delete("/tests/{test_id}")
async def delete_test(test_id: int, user: IAdminUser, service: TestsServiceDep):
    await service.delete_test(test_id)


@router.post("/tests/{test_id}/complete")
async def complete_test(test_id: int, request: UserTestResultRequest, user: ICurrentUser, service: TestsServiceDep):
    create = UserTestResultCreate(answers=request.answers, test_id=test_id, user_id=user.id)
    return await service.add_user_test_result(create)


@router.get("/me/tests")
async def get_current_user_completed_tests(user: ICurrentUser, service: TestsServiceDep):
    return await service.get_user_test_results(user.id)