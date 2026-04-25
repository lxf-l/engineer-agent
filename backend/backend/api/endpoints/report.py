from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ReportRequest, ReportResponse
from app.services.report_service import ReportService
from app.core.security import verify_api_key
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/report",
    tags=["报告生成"],
    responses={401: {"description": "Unauthorized"}}
)


@router.post(
    "/",
    response_model=ReportResponse,
    summary="生成工程报告",
    description="基于LLM和工程规范自动生成各类技术报告"
)
async def generate_report(
    request: ReportRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    生成工程报告
    
    - **report_type**: 报告类型（concrete_mix、structural_design、load_calculation、material_spec）
    - **parameters**: 报告参数字典，根据报告类型不同而不同
    - **collection_name**: 可选的集合名称
    """
    try:
        # 初始化报告服务
        report_service = ReportService()
        
        # 生成报告
        result = report_service.generate_report(
            report_type=request.report_type,
            parameters=request.parameters,
            collection_name=request.collection_name
        )
        
        return ReportResponse(**result)
        
    except ValueError as e:
        logger.warning(f"Invalid report request: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Report generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"报告生成失败: {str(e)}"
        )
