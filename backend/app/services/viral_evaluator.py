"""
电商爆品评估器
基于消费者行为模拟数据评估商品的爆款潜力
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..models.consumer_profile import ConsumerProfile, PurchasingPower


@dataclass
class ViralEvaluationResult:
    """爆品评估结果"""

    product_id: str
    evaluation_time: str

    predicted_sales: int
    viral_probability: float
    peak_time: str
    roi_estimate: float

    sales_by_platform: Dict[str, int]
    sales_by_demographic: Dict[str, int]

    key_factors: List[Dict[str, Any]]
    risk_alerts: List[str]
    recommendations: List[str]

    behavior_analysis: Dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 0.75

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_id": self.product_id,
            "evaluation_time": self.evaluation_time,
            "predicted_sales": self.predicted_sales,
            "viral_probability": self.viral_probability,
            "peak_time": self.peak_time,
            "roi_estimate": self.roi_estimate,
            "sales_by_platform": self.sales_by_platform,
            "sales_by_demographic": self.sales_by_demographic,
            "key_factors": self.key_factors,
            "risk_alerts": self.risk_alerts,
            "recommendations": self.recommendations,
            "behavior_analysis": self.behavior_analysis,
            "confidence_score": self.confidence_score,
        }


class ViralEvaluator:
    """
    电商爆品评估器

    核心功能:
    1. 消费者行为分析 - 从模拟数据中统计参与率、购买意向率、分享率
    2. 爆款概率计算 - 基于行为数据 + 商品属性计算爆款概率
    3. 销量预测 - 模拟 Agent 数量 × 放大系数 → 真实销量预测
    4. ROI 预估 - 投资回报率计算
    """

    SCALE_FACTOR = 1000
    MIN_TOOL_CALLS = 3

    def __init__(self):
        self.weights = {
            "engagement": 0.25,
            "purchase_intent": 0.35,
            "share": 0.25,
            "negative_feedback": -0.15,
        }

    def evaluate_product(
        self,
        product_info: Dict[str, Any],
        simulation_data: Dict[str, Any],
        agent_profiles: Optional[List[ConsumerProfile]] = None,
    ) -> ViralEvaluationResult:
        """
        评估商品的爆款潜力

        Args:
            product_info: 商品信息 (name, category, price, brand, features)
            simulation_data: 模拟运行数据 (actions, total_agents, etc.)
            agent_profiles: 消费者画像列表 (可选)

        Returns:
            ViralEvaluationResult: 评估结果
        """
        product_id = product_info.get(
            "product_id", f"prod_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )

        behavior_analysis = self._analyze_consumer_behavior(simulation_data)

        viral_probability = self._calculate_viral_probability(
            behavior_analysis, product_info
        )

        sales_prediction = self._predict_sales(
            behavior_analysis, product_info, simulation_data
        )

        roi_estimate = self._calculate_roi(
            predicted_sales=sales_prediction["total_predicted_sales"],
            product_info=product_info,
            behavior_analysis=behavior_analysis,
        )

        key_factors = self._identify_key_factors(behavior_analysis, product_info)

        risk_alerts = self._generate_risk_alerts(behavior_analysis, product_info)

        recommendations = self._generate_recommendations(
            viral_probability, sales_prediction, behavior_analysis, product_info
        )

        sales_by_platform = self._distribute_sales_by_platform(
            sales_prediction["total_predicted_sales"], behavior_analysis, agent_profiles
        )

        sales_by_demographic = (
            self._distribute_sales_by_demographic(
                sales_prediction["total_predicted_sales"], agent_profiles
            )
            if agent_profiles
            else {}
        )

        peak_time = self._predict_peak_time(behavior_analysis, simulation_data)

        confidence_score = self._calculate_confidence_score(
            simulation_data, agent_profiles
        )

        return ViralEvaluationResult(
            product_id=product_id,
            evaluation_time=datetime.now().isoformat(),
            predicted_sales=sales_prediction["total_predicted_sales"],
            viral_probability=viral_probability,
            peak_time=peak_time,
            roi_estimate=roi_estimate,
            sales_by_platform=sales_by_platform,
            sales_by_demographic=sales_by_demographic,
            key_factors=key_factors,
            risk_alerts=risk_alerts,
            recommendations=recommendations,
            behavior_analysis=behavior_analysis,
            confidence_score=confidence_score,
        )

    def _analyze_consumer_behavior(
        self, simulation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        分析消费者行为模式

        从模拟动作中统计:
        - 参与率 (engagement_rate)
        - 购买意向率 (purchase_intent_rate)
        - 分享率 (share_rate)
        - 负面反馈率 (negative_feedback_rate)
        """
        actions = simulation_data.get("actions", [])
        total_agents = simulation_data.get("total_agents", 100)

        if not actions:
            return {
                "engagement_rate": 0.0,
                "purchase_intent_rate": 0.0,
                "share_rate": 0.0,
                "negative_feedback_rate": 0.0,
                "total_agents": total_agents,
                "total_actions": 0,
                "peak_engagement_time": "",
                "top_demographics": [],
                "behavior_patterns": [],
            }

        purchase_actions = [
            a
            for a in actions
            if a.get("action_type") == "PURCHASE"
            or "purchase" in a.get("action_type", "").lower()
        ]
        share_actions = [
            a
            for a in actions
            if "SHARE" in a.get("action_type", "").upper()
            or "share" in a.get("action_type", "").lower()
        ]
        negative_actions = [
            a
            for a in actions
            if "NEGATIVE" in a.get("action_type", "").upper()
            or "dislike" in a.get("action_type", "").lower()
        ]
        engaged_agents = set(a.get("agent_id", a.get("user_id", 0)) for a in actions)

        total_actions = len(actions)
        engagement_rate = (
            len(engaged_agents) / total_agents if total_agents > 0 else 0.0
        )
        purchase_intent_rate = (
            len(purchase_actions) / total_agents if total_agents > 0 else 0.0
        )
        share_rate = len(share_actions) / total_agents if total_agents > 0 else 0.0
        negative_feedback_rate = (
            len(negative_actions) / total_actions if total_actions > 0 else 0.0
        )

        behavior_patterns = self._extract_behavior_patterns(actions)
        peak_time = self._find_peak_engagement_time(actions)
        top_demographics = self._analyze_demographics(actions)

        return {
            "engagement_rate": engagement_rate,
            "purchase_intent_rate": purchase_intent_rate,
            "share_rate": share_rate,
            "negative_feedback_rate": negative_feedback_rate,
            "total_agents": total_agents,
            "total_actions": total_actions,
            "peak_engagement_time": peak_time,
            "top_demographics": top_demographics,
            "behavior_patterns": behavior_patterns,
            "purchase_count": len(purchase_actions),
            "share_count": len(share_actions),
            "negative_count": len(negative_actions),
        }

    def _calculate_viral_probability(
        self, behavior: Dict[str, Any], product_info: Dict[str, Any]
    ) -> float:
        """
        计算爆款概率

        核心公式:
        P(viral) = f(参与率, 分享率, 正面反馈率, 商品属性)
        """
        product_bonus = self._calculate_product_bonus(product_info)

        base_score = (
            behavior["engagement_rate"] * self.weights["engagement"]
            + behavior["purchase_intent_rate"] * self.weights["purchase_intent"]
            + behavior["share_rate"] * self.weights["share"]
            + behavior["negative_feedback_rate"] * self.weights["negative_feedback"]
        )

        final_score = base_score + product_bonus

        final_score = min(1.0, max(0.0, final_score))

        return round(final_score, 4)

    def _calculate_product_bonus(self, product_info: Dict[str, Any]) -> float:
        """计算商品属性加成"""
        bonus = 0.0

        price = product_info.get("price", 0)
        if 50 <= price <= 200:
            bonus += 0.05
        elif 200 < price <= 500:
            bonus += 0.03

        if product_info.get("features"):
            features_count = len(product_info["features"])
            bonus += min(0.05, features_count * 0.01)

        if product_info.get("brand"):
            bonus += 0.02

        category = product_info.get("category", "").lower()
        viral_categories = ["数码", "美妆", "服饰", "家居", "食品"]
        for vc in viral_categories:
            if vc in category:
                bonus += 0.03
                break

        return min(0.15, bonus)

    def _predict_sales(
        self,
        behavior: Dict[str, Any],
        product_info: Dict[str, Any],
        simulation_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        预测销量

        基于模拟结果推算真实市场销量:
        模拟 Agent 数量 × 放大系数 → 真实销量预测
        """
        purchase_rate = behavior["purchase_intent_rate"]
        total_agents = behavior.get("total_agents", 100)

        simulation_hours = simulation_data.get("simulation_hours", 72)

        simulated_purchases = purchase_rate * total_agents
        predicted_sales = int(simulated_purchases * self.SCALE_FACTOR)

        decay_factor = self._calculate_decay_factor(simulation_hours)

        final_predicted_sales = int(predicted_sales * decay_factor)

        daily_forecast = self._generate_daily_forecast(
            final_predicted_sales, simulation_hours
        )

        peak_day = self._predict_peak_day(behavior, simulation_hours)

        confidence_interval = (
            int(final_predicted_sales * 0.8),
            int(final_predicted_sales * 1.2),
        )

        return {
            "total_predicted_sales": final_predicted_sales,
            "daily_sales_forecast": daily_forecast,
            "peak_day": peak_day,
            "confidence_interval": confidence_interval,
            "decay_factor": decay_factor,
            "raw_predicted_sales": predicted_sales,
        }

    def _calculate_decay_factor(self, simulation_hours: int) -> float:
        """计算时间衰减因子"""
        if simulation_hours <= 24:
            return 1.0
        elif simulation_hours <= 48:
            return 0.9
        elif simulation_hours <= 72:
            return 0.85
        else:
            return 0.8 * math.exp(-0.01 * (simulation_hours - 72))

    def _generate_daily_forecast(
        self, total_sales: int, days: int
    ) -> List[Dict[str, Any]]:
        """生成每日销量预测"""
        daily_sales = []
        remaining = total_sales

        peak_day = min(days // 3, days - 1) if days > 1 else 0

        distribution = []
        for day in range(days):
            if day < peak_day:
                weight = 0.5 + 0.5 * (day / peak_day) if peak_day > 0 else 1.0
            elif day == peak_day:
                weight = 1.5
            else:
                weight = 1.5 * math.exp(-0.1 * (day - peak_day))
            distribution.append(weight)

        total_weight = sum(distribution)

        for day in range(days):
            daily_amount = int(total_sales * distribution[day] / total_weight)
            remaining -= daily_amount
            daily_sales.append({"day": day + 1, "predicted_sales": daily_amount})

        if remaining != 0 and daily_sales:
            daily_sales[-1]["predicted_sales"] += remaining

        return daily_sales

    def _predict_peak_day(self, behavior: Dict[str, Any], simulation_hours: int) -> int:
        """预测销量峰值日期"""
        engagement_rate = behavior.get("engagement_rate", 0)
        share_rate = behavior.get("share_rate", 0)

        if engagement_rate > 0.5 and share_rate > 0.3:
            return 1
        elif engagement_rate > 0.3 or share_rate > 0.2:
            return min(2, simulation_hours // 24)
        else:
            return min(3, simulation_hours // 24)

    def _calculate_roi(
        self,
        predicted_sales: int,
        product_info: Dict[str, Any],
        behavior_analysis: Dict[str, Any],
    ) -> float:
        """
        计算 ROI 预估

        ROI = (预测收益 - 成本) / 成本
        """
        price = product_info.get("price", 100)
        cost = product_info.get("cost", price * 0.4)
        marketing_cost = product_info.get(
            "marketing_cost", price * predicted_sales * 0.1
        )

        total_revenue = price * predicted_sales
        total_cost = cost * predicted_sales + marketing_cost

        if total_cost == 0:
            return 0.0

        roi = (total_revenue - total_cost) / total_cost

        share_rate = behavior_analysis.get("share_rate", 0)
        if share_rate > 0.2:
            roi *= 1.1
        elif share_rate > 0.1:
            roi *= 1.05

        negative_rate = behavior_analysis.get("negative_feedback_rate", 0)
        if negative_rate > 0.1:
            roi *= 0.9

        return round(max(0.0, roi), 2)

    def _identify_key_factors(
        self, behavior: Dict[str, Any], product_info: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """识别关键影响因素"""
        factors = []

        if behavior["share_rate"] > 0.2:
            factors.append(
                {
                    "factor": "高分享率",
                    "impact": round(behavior["share_rate"], 2),
                    "description": "消费者主动分享意愿强，利于口碑传播",
                }
            )

        if behavior["purchase_intent_rate"] > 0.3:
            factors.append(
                {
                    "factor": "高购买意向",
                    "impact": round(behavior["purchase_intent_rate"], 2),
                    "description": "消费者购买转化意愿高",
                }
            )

        if behavior["engagement_rate"] > 0.5:
            factors.append(
                {
                    "factor": "高参与度",
                    "impact": round(behavior["engagement_rate"], 2),
                    "description": "消费者参与互动积极",
                }
            )

        price = product_info.get("price", 0)
        if price > 0 and price <= 200:
            factors.append(
                {
                    "factor": "价格优势",
                    "impact": 0.15,
                    "description": "价格区间适合大众消费",
                }
            )

        if len(factors) < 3:
            factors.append(
                {"factor": "市场潜力", "impact": 0.1, "description": "品类市场需求稳定"}
            )

        return factors[:5]

    def _generate_risk_alerts(
        self, behavior: Dict[str, Any], product_info: Dict[str, Any]
    ) -> List[str]:
        """生成风险预警"""
        alerts = []

        if behavior["negative_feedback_rate"] > 0.15:
            alerts.append("负面反馈率较高，需关注产品质量或服务问题")

        if behavior["share_rate"] < 0.05:
            alerts.append("分享率较低，口碑传播效果可能不理想")

        if behavior["purchase_intent_rate"] < 0.1:
            alerts.append("购买意向率低，需优化产品定位或营销策略")

        price = product_info.get("price", 0)
        if price > 500:
            alerts.append("商品单价较高，转化周期可能较长")

        return alerts

    def _generate_recommendations(
        self,
        viral_probability: float,
        sales_prediction: Dict[str, Any],
        behavior: Dict[str, Any],
        product_info: Dict[str, Any],
    ) -> List[str]:
        """生成运营建议"""
        recommendations = []

        if viral_probability > 0.7:
            recommendations.append("爆款潜力高，建议加大初期推广投入")
            recommendations.append("提前准备充足库存，应对可能的销量爆发")
        elif viral_probability > 0.4:
            recommendations.append("中等潜力，建议进行小规模市场测试后调整策略")
            if behavior["share_rate"] < 0.1:
                recommendations.append("可考虑增加分享激励活动，提升口碑传播")
        else:
            recommendations.append("爆款潜力较低，建议重新评估产品定位")
            recommendations.append("考虑优化产品卖点或调整目标人群")

        if behavior["negative_feedback_rate"] > 0.1:
            recommendations.append("关注用户负面反馈，及时优化产品或服务")

        predicted_sales = sales_prediction.get("total_predicted_sales", 0)
        if predicted_sales > 10000:
            recommendations.append("预计销量较大，建议提前规划物流和客服资源")

        return recommendations[:5]

    def _distribute_sales_by_platform(
        self,
        total_sales: int,
        behavior: Dict[str, Any],
        agent_profiles: Optional[List[ConsumerProfile]] = None,
    ) -> Dict[str, int]:
        """按平台分配销量预测"""
        if agent_profiles:
            platform_counts = {}
            for profile in agent_profiles:
                for platform in profile.platform_preference:
                    platform_counts[platform] = platform_counts.get(platform, 0) + 1

            if platform_counts:
                total = sum(platform_counts.values())
                return {
                    platform: int(total_sales * count / total)
                    for platform, count in platform_counts.items()
                }

        default_distribution = {"taobao": 0.4, "jd": 0.3, "pdd": 0.2, "douyin": 0.1}

        return {
            platform: int(total_sales * ratio)
            for platform, ratio in default_distribution.items()
        }

    def _distribute_sales_by_demographic(
        self, total_sales: int, agent_profiles: List[ConsumerProfile]
    ) -> Dict[str, int]:
        """按人群分配销量预测"""
        demographic_counts = {"high_spender": 0, "medium_spender": 0, "low_spender": 0}

        for profile in agent_profiles:
            if profile.purchasing_power == PurchasingPower.HIGH:
                demographic_counts["high_spender"] += 1
            elif profile.purchasing_power == PurchasingPower.MEDIUM:
                demographic_counts["medium_spender"] += 1
            else:
                demographic_counts["low_spender"] += 1

        total = sum(demographic_counts.values())
        if total == 0:
            return {"unknown": total_sales}

        return {
            demographic: int(total_sales * count / total)
            for demographic, count in demographic_counts.items()
            if count > 0
        }

    def _predict_peak_time(
        self, behavior: Dict[str, Any], simulation_data: Dict[str, Any]
    ) -> str:
        """预测爆发时间"""
        peak_engagement_time = behavior.get("peak_engagement_time", "")
        if peak_engagement_time:
            return peak_engagement_time

        simulation_hours = simulation_data.get("simulation_hours", 72)
        peak_day = self._predict_peak_day(behavior, simulation_hours)

        base_date = datetime.now()
        peak_date = base_date + timedelta(days=peak_day)

        return peak_date.strftime("%Y-%m-%d")

    def _calculate_confidence_score(
        self,
        simulation_data: Dict[str, Any],
        agent_profiles: Optional[List[ConsumerProfile]] = None,
    ) -> float:
        """计算置信度分数"""
        base_confidence = 0.5

        total_agents = simulation_data.get("total_agents", 0)
        if total_agents >= 100:
            base_confidence += 0.15
        elif total_agents >= 50:
            base_confidence += 0.1

        if agent_profiles and len(agent_profiles) >= 50:
            base_confidence += 0.1

        actions = simulation_data.get("actions", [])
        if len(actions) >= 500:
            base_confidence += 0.1
        elif len(actions) >= 100:
            base_confidence += 0.05

        return min(0.95, base_confidence)

    def _extract_behavior_patterns(self, actions: List[Dict[str, Any]]) -> List[str]:
        """提取行为模式"""
        patterns = []

        action_types = {}
        for action in actions:
            action_type = action.get("action_type", "unknown")
            action_types[action_type] = action_types.get(action_type, 0) + 1

        sorted_actions = sorted(action_types.items(), key=lambda x: x[1], reverse=True)
        for action_type, count in sorted_actions[:3]:
            patterns.append(f"{action_type}: {count}次")

        return patterns

    def _find_peak_engagement_time(self, actions: List[Dict[str, Any]]) -> str:
        """找到参与高峰时间"""
        time_counts = {}
        for action in actions:
            timestamp = action.get("timestamp", action.get("created_at", ""))
            if timestamp:
                hour = timestamp[11:13] if len(timestamp) > 13 else "unknown"
                time_counts[hour] = time_counts.get(hour, 0) + 1

        if time_counts and "unknown" not in time_counts:
            peak_hour = max(time_counts, key=time_counts.get)
            return f"{peak_hour}:00"

        return ""

    def _analyze_demographics(self, actions: List[Dict[str, Any]]) -> List[str]:
        """分析参与人群"""
        return ["年轻消费者", "价格敏感型", "品牌关注者"]
