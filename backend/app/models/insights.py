"""Pydantic v2 models for AI-generated carbon reduction insights."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.models.carbon import CarbonResult, InsightItem


class InsightsRequest(BaseModel):
    """Request body for the /api/insights endpoint."""

    carbon_result: CarbonResult = Field(description="Previously calculated carbon result")
    device_id: str = Field(
        min_length=8,
        max_length=64,
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Opaque anonymous device identifier",
    )


class InsightsResponse(BaseModel):
    """Response from the /api/insights endpoint."""

    insights: list[InsightItem] = Field(description="List of exactly 3 prioritised insights")
    source: Literal["gemini", "rules"] = Field(
        description="Which engine generated the insights: Gemini AI or deterministic rule engine"
    )
    total_potential_saving_kg: float = Field(
        description="Sum of estimated_saving_kg across all insights"
    )
