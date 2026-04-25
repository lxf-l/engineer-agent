from fastapi import Header, HTTPException, Depends
from app.core.config import settings


async def verify_api_key(x_api_key: str = Header(...)):
    """
    API Key认证依赖函数
    
    Args:
        x_api_key: 请求头中的API Key
        
    Returns:
        str: 验证通过的API Key
        
    Raises:
        HTTPException: 当API Key无效时抛出401错误
    """
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )
    return x_api_key


# 可选认证的依赖（某些路由不需要认证）
def get_api_key_dependency(require_auth: bool = True):
    """
    获取API Key依赖
    
    Args:
        require_auth: 是否需要认证
        
    Returns:
        依赖函数或None
    """
    if require_auth:
        return Depends(verify_api_key)
    return None
