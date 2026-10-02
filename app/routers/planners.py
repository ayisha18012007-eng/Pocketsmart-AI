from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
)

from app.models.schemas import (
    HomePlannerRequest,
    JewelryPlannerRequest,
    PartyPlannerRequest,
)
from app.routers.auth import get_current_user
from app.services.db import (
    get_recommendation,
    get_user_recommendations,
    save_recommendation,
)
from app.services.recommender import (
    generate_recommendation,
)


router = APIRouter(
    tags=["AI Planners"]
)


@router.post("/generate-home")
def generate_home(
    data: HomePlannerRequest,
    user=Depends(get_current_user)
):

    input_data = data.model_dump()

    result = generate_recommendation(
        "home",
        input_data
    )

    recommendation_id = save_recommendation(
        user_id=user["id"],
        planner_type="home",
        input_data=input_data,
        result_data=result
    )

    return {
        "id": recommendation_id,
        "planner_type": "home",
        "result": result
    }


@router.post("/generate-party")
def generate_party(
    data: PartyPlannerRequest,
    user=Depends(get_current_user)
):

    input_data = data.model_dump()

    result = generate_recommendation(
        "party",
        input_data
    )

    recommendation_id = save_recommendation(
        user_id=user["id"],
        planner_type="party",
        input_data=input_data,
        result_data=result
    )

    return {
        "id": recommendation_id,
        "planner_type": "party",
        "result": result
    }


@router.post("/generate-jewelry")
async def generate_jewelry(
    occasion: str,
    outfit: str,
    metal: str,
    budget: float,
    style: str,
    requirements: str = "",
    image: Optional[UploadFile] = File(None),
    user=Depends(get_current_user)
):

    if budget <= 0:

        raise HTTPException(
            status_code=400,
            detail="Budget must be greater than zero."
        )

    image_name = None

    if image:

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp"
        }

        if image.content_type not in allowed_types:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPG, PNG and WEBP "
                    "images are supported."
                )
            )

        content = await image.read()

        if len(content) > 5 * 1024 * 1024:

            raise HTTPException(
                status_code=400,
                detail="Image must be smaller than 5 MB."
            )

        image_name = image.filename

    input_data = {
        "occasion": occasion,
        "outfit": outfit,
        "metal": metal,
        "budget": budget,
        "style": style,
        "requirements": requirements,
        "image": image_name
    }

    result = generate_recommendation(
        "jewelry",
        input_data
    )

    recommendation_id = save_recommendation(
        user_id=user["id"],
        planner_type="jewelry",
        input_data=input_data,
        result_data=result
    )

    return {
        "id": recommendation_id,
        "planner_type": "jewelry",
        "result": result
    }


@router.get("/recommendations-details/{rid}")
def recommendation_details(
    rid: int,
    user=Depends(get_current_user)
):

    recommendation = get_recommendation(
        rid,
        user["id"]
    )

    if not recommendation:

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found."
        )

    return recommendation


@router.get("/api/history")
def api_history(
    user=Depends(get_current_user)
):

    recommendations = get_user_recommendations(
        user["id"]
    )

    return {
        "recommendations": recommendations
    }