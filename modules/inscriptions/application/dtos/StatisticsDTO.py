from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

class BarChartDataDTO(BaseModel):
    labels: List[str]
    datasets: List[dict]

class LineChartDataDTO(BaseModel):
    labels: List[str]
    datasets: List[dict]

class PieChartDataDTO(BaseModel):
    labels: List[str]
    datasets: List[dict]

class FunnelChartDataDTO(BaseModel):
    stages: List[str]
    values: List[int]

class StackedBarDataDTO(BaseModel):
    events: List[str]
    datasets: List[dict]

class StatisticsResponseDTO(BaseModel):
    bar_chart: BarChartDataDTO
    line_chart: LineChartDataDTO
    pie_chart: PieChartDataDTO
    funnel_chart: FunnelChartDataDTO
    stacked_bar: StackedBarDataDTO
