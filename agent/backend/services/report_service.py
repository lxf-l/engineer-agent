from typing import Dict, Any, List
from langchain_deepseek import ChatDeepSeek
from app.core.config import settings
from app.models.schemas import ReportReference
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


# 报告模板字典
REPORT_TEMPLATES = {
    "concrete_mix": """
请根据以下参数生成混凝土配合比设计报告：

强度等级：{strength_grade}
坍落度：{slump}
使用环境：{environment}
骨料类型：{aggregate_type}

要求：
1. 给出详细的配合比计算过程
2. 列出材料用量（水泥、水、砂、石子）
3. 说明技术要点和质量控制措施
4. 引用相关规范条文
""",
    
    "structural_design": """
请根据以下参数生成结构设计报告：

结构类型：{structure_type}
荷载等级：{load_grade}
抗震设防烈度：{seismic_intensity}
地基条件：{foundation_condition}

要求：
1. 结构选型和布置说明
2. 主要构件尺寸估算
3. 荷载计算
4. 构造措施建议
5. 引用相关规范条文
""",
    
    "load_calculation": """
请根据以下参数生成荷载计算书：

建筑用途：{building_use}
楼层数：{floors}
结构形式：{structure_form}
地区风压：{wind_pressure}
地区雪压：{snow_pressure}

要求：
1. 恒荷载计算
2. 活荷载取值
3. 风荷载计算
4. 雪荷载计算
5. 荷载组合建议
6. 引用相关规范条文
""",
    
    "material_spec": """
请根据以下要求生成材料技术规范：

材料类型：{material_type}
使用部位：{usage_location}
技术要求：{technical_requirements}
环境条件：{environmental_conditions}

要求：
1. 材料性能指标
2. 检验标准和方法
3. 验收标准
4. 储存和运输要求
5. 质量控制措施
6. 引用相关规范条文
"""
}


class ReportService:
    """报告生成服务"""
    
    def __init__(self):
        self.llm = ChatDeepSeek(
            api_key=settings.DEEPSEEK_API_KEY,
            model_name="deepseek-chat",
            temperature=0.7
        )
    
    def generate_report(
        self,
        report_type: str,
        parameters: Dict[str, Any],
        collection_name: str = None
    ) -> Dict[str, Any]:
        """
        生成工程报告
        
        Args:
            report_type: 报告类型
            parameters: 报告参数
            collection_name: 集合名称（可选）
            
        Returns:
            包含content、references、generated_at的字典
        """
        try:
            # 1. 获取报告模板
            template = REPORT_TEMPLATES.get(report_type)
            if not template:
                raise ValueError(f"不支持的报告类型: {report_type}")
            
            # 2. 填充模板参数
            try:
                prompt = template.format(**parameters)
            except KeyError as e:
                raise ValueError(f"缺少必要参数: {str(e)}")
            
            # 3. 调用LLM生成报告
            logger.info(f"Generating report of type: {report_type}")
            response = self.llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            
            # 4. 提取引用的规范（简单实现，可以通过RAG增强）
            references = self._extract_references(content)
            
            return {
                "content": content,
                "references": references,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate report: {e}", exc_info=True)
            raise
    
    def _extract_references(self, content: str) -> List[ReportReference]:
        """
        从报告内容中提取引用规范
        
        Args:
            content: 报告内容
            
        Returns:
            引用规范列表
        """
        references = []
        
        # 简单的规范提取逻辑（可以根据实际情况优化）
        # 匹配常见的规范格式，如 GB 50010-2010、JGJ 55-2011 等
        import re
        
        # 匹配规范编号模式
        pattern = r'(GB|JGJ|JTJ|TB)\s*\d+[-—]\d{4}'
        matches = re.findall(pattern, content)
        
        for match in set(matches):
            references.append(ReportReference(
                standard_name=match,
                section=None,
                content="相关规范条文"
            ))
        
        return references
