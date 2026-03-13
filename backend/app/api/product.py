"""
商品爆品评估 API
提供商品爆款潜力评估接口
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any, Optional

from ..services.viral_evaluator import ViralEvaluator, ViralEvaluationResult
from ..models.consumer_profile import ConsumerProfile, PurchasingPower, ShoppingFrequency
from ..utils.logger import get_logger

logger = get_logger('mirofish.api.product')

product_bp = Blueprint('product', __name__)


@product_bp.route('/evaluate', methods=['POST'])
def evaluate_product():
    """
    评估商品爆款潜力
    
    Request Body:
        {
            "simulation_id": "xxx",
            "graph_id": "xxx",
            "product_info": {
                "name": "商品名称",
                "category": "品类",
                "price": 99.9,
                "brand": "品牌",
                "features": ["特点1", "特点2"],
                "cost": 50.0,
                "marketing_cost": 1000
            },
            "simulation_data": {
                "actions": [...],
                "total_agents": 100,
                "simulation_hours": 72
            },
            "agent_profiles": [...]  // 可选
        }
    
    Response:
        {
            "evaluation_id": "xxx",
            "product_id": "xxx",
            "predicted_sales": 10000,
            "viral_probability": 0.75,
            "peak_time": "2026-03-20",
            "roi_estimate": 2.5,
            "sales_by_platform": {...},
            "key_factors": [...],
            "risk_alerts": [...],
            "recommendations": [...]
        }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                "error": "请求体不能为空",
                "code": "INVALID_REQUEST"
            }), 400
        
        product_info = data.get("product_info", {})
        simulation_data = data.get("simulation_data", {})
        agent_profiles_data = data.get("agent_profiles", [])
        
        # 验证必要字段
        if not product_info:
            return jsonify({
                "error": "product_info 不能为空",
                "code": "MISSING_PRODUCT_INFO"
            }), 400
        
        # 转换 agent_profiles
        agent_profiles = None
        if agent_profiles_data:
            agent_profiles = []
            for profile_data in agent_profiles_data:
                try:
                    profile = ConsumerProfile.from_dict(profile_data)
                    agent_profiles.append(profile)
                except Exception as e:
                    logger.warning(f"解析消费者画像失败: {e}")
        
        # 创建评估器并执行评估
        evaluator = ViralEvaluator()
        result = evaluator.evaluate_product(
            product_info=product_info,
            simulation_data=simulation_data,
            agent_profiles=agent_profiles
        )
        
        logger.info(f"商品评估完成: {result.product_id}, 爆款概率: {result.viral_probability}")
        
        return jsonify({
            "success": True,
            "data": result.to_dict()
        })
        
    except Exception as e:
        logger.error(f"商品评估失败: {str(e)}")
        return jsonify({
            "error": str(e),
            "code": "EVALUATION_FAILED"
        }), 500


@product_bp.route('/evaluate/quick', methods=['POST'])
def quick_evaluate():
    """
    快速评估商品爆款潜力（简化版）
    
    仅基于商品信息进行快速评估，不需要模拟数据
    
    Request Body:
        {
            "product_info": {
                "name": "商品名称",
                "category": "品类",
                "price": 99.9,
                "brand": "品牌",
                "features": ["特点1", "特点2"]
            }
        }
    
    Response:
        {
            "viral_score": 0.65,
            "category_fit": "high",
            "price_range_fit": "optimal",
            "quick_recommendations": [...]
        }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                "error": "请求体不能为空",
                "code": "INVALID_REQUEST"
            }), 400
        
        product_info = data.get("product_info", {})
        
        if not product_info:
            return jsonify({
                "error": "product_info 不能为空",
                "code": "MISSING_PRODUCT_INFO"
            }), 400
        
        # 快速评估逻辑
        evaluator = ViralEvaluator()
        
        # 使用默认模拟数据进行快速评估
        default_simulation = {
            "actions": [],
            "total_agents": 100,
            "simulation_hours": 72
        }
        
        result = evaluator.evaluate_product(
            product_info=product_info,
            simulation_data=default_simulation,
            agent_profiles=None
        )
        
        # 生成快速建议
        quick_recommendations = []
        price = product_info.get("price", 0)
        category = product_info.get("category", "").lower()
        
        if price > 0 and price <= 200:
            quick_recommendations.append("价格区间适合大众消费，利于转化")
        elif price > 500:
            quick_recommendations.append("单价较高，建议强化品质和品牌宣传")
        
        viral_categories = ["数码", "美妆", "服饰", "家居", "食品"]
        category_fit = "medium"
        for vc in viral_categories:
            if vc in category:
                category_fit = "high"
                quick_recommendations.append(f"品类 '{vc}' 属于高爆款潜力品类")
                break
        
        if product_info.get("features") and len(product_info["features"]) >= 3:
            quick_recommendations.append("产品特点丰富，建议在营销中突出差异化卖点")
        
        return jsonify({
            "success": True,
            "data": {
                "viral_score": result.viral_probability,
                "category_fit": category_fit,
                "price_range_fit": "optimal" if 50 <= price <= 200 else "high" if price < 50 else "premium",
                "quick_recommendations": quick_recommendations,
                "full_evaluation": result.to_dict()
            }
        })
        
    except Exception as e:
        logger.error(f"快速评估失败: {str(e)}")
        return jsonify({
            "error": str(e),
            "code": "QUICK_EVALUATION_FAILED"
        }), 500


@product_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "service": "product-evaluation"
    })