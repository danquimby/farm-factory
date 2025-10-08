from fastapi import APIRouter, Depends

from app.core.exceptions import HTTPException
from app.features.dependencies import get_struct_repository
from app.features.structure.repository import StructureRepository
from app.features.structure.schemas import StructureDetails

router = APIRouter(prefix="/structure", tags=["structure"])


@router.get("/", response_model=StructureDetails)
async def get_structure(
    id: int,
    structure_repository: StructureRepository = Depends(get_struct_repository),
):
    if result := await structure_repository.get_by_id(id):
        return StructureDetails.model_validate(result)
    raise HTTPException(404, f"not found structure {id=}")


@router.get("/all", response_model=list[StructureDetails])
async def get_structure(
    structure_repository: StructureRepository = Depends(get_struct_repository),
):
    if result := await structure_repository.get_all():
        return [StructureDetails.model_validate(r) for r in result]
    raise HTTPException(501, f"error get all")
