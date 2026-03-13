"""
消费者画像数据模型
用于电商爆品预测系统中的消费者 Agent 属性定义
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class PurchasingPower(str, Enum):
    """消费能力等级"""

    HIGH = "high"  # 月消费 > 5000
    MEDIUM = "medium"  # 月消费 1000-5000
    LOW = "low"  # 月消费 < 1000


class ShoppingFrequency(str, Enum):
    """购物频率"""

    DAILY = "daily"  # 每天购物
    WEEKLY = "weekly"  # 每周购物
    MONTHLY = "monthly"  # 每月购物
    RARELY = "rarely"  # 很少购物


@dataclass
class ConsumerProfile:
    """
    消费者画像数据模型

    包含消费者的基础属性和消费相关属性
    """

    # 基础标识
    user_id: int
    username: str
    name: str
    bio: str
    persona: str

    # 消费能力属性
    purchasing_power: PurchasingPower
    price_sensitivity: float  # 0.0-1.0 价格敏感度
    brand_loyalty: float  # 0.0-1.0 品牌忠诚度
    shopping_frequency: ShoppingFrequency

    # 兴趣偏好
    preferred_categories: List[str] = field(default_factory=list)  # 偏好品类
    platform_preference: List[str] = field(
        default_factory=list
    )  # 偏好平台 ["taobao", "jd", "pdd"]

    # 决策因素权重
    decision_factors: Dict[str, float] = field(
        default_factory=lambda: {
            "price": 0.3,
            "quality": 0.25,
            "brand": 0.2,
            "reviews": 0.15,
            "trend": 0.1,
        }
    )

    # 扩展属性
    age: Optional[int] = None
    gender: Optional[str] = None
    mbti: Optional[str] = None
    city: Optional[str] = None
    profession: Optional[str] = None

    def __post_init__(self):
        """初始化后验证数据"""
        # 验证价格敏感度范围
        if not 0.0 <= self.price_sensitivity <= 1.0:
            raise ValueError(
                f"price_sensitivity 必须在 0.0-1.0 之间，当前值: {self.price_sensitivity}"
            )

        # 验证品牌忠诚度范围
        if not 0.0 <= self.brand_loyalty <= 1.0:
            raise ValueError(
                f"brand_loyalty 必须在 0.0-1.0 之间，当前值: {self.brand_loyalty}"
            )

        # 验证决策因素权重总和为 1.0
        if self.decision_factors:
            total = sum(self.decision_factors.values())
            if abs(total - 1.0) > 0.01:  # 允许 1% 误差
                # 自动归一化
                if total > 0:
                    self.decision_factors = {
                        k: v / total for k, v in self.decision_factors.items()
                    }

    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "name": self.name,
            "bio": self.bio,
            "persona": self.persona,
            "purchasing_power": self.purchasing_power.value
            if isinstance(self.purchasing_power, PurchasingPower)
            else self.purchasing_power,
            "price_sensitivity": self.price_sensitivity,
            "brand_loyalty": self.brand_loyalty,
            "shopping_frequency": self.shopping_frequency.value
            if isinstance(self.shopping_frequency, ShoppingFrequency)
            else self.shopping_frequency,
            "preferred_categories": self.preferred_categories,
            "platform_preference": self.platform_preference,
            "decision_factors": self.decision_factors,
            "age": self.age,
            "gender": self.gender,
            "mbti": self.mbti,
            "city": self.city,
            "profession": self.profession,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "ConsumerProfile":
        """从字典创建 ConsumerProfile"""
        # 处理枚举类型
        purchasing_power = data.get("purchasing_power", "medium")
        if isinstance(purchasing_power, str):
            purchasing_power = PurchasingPower(purchasing_power)

        shopping_frequency = data.get("shopping_frequency", "weekly")
        if isinstance(shopping_frequency, str):
            shopping_frequency = ShoppingFrequency(shopping_frequency)

        return cls(
            user_id=data.get("user_id", 0),
            username=data.get("username", ""),
            name=data.get("name", ""),
            bio=data.get("bio", ""),
            persona=data.get("persona", ""),
            purchasing_power=purchasing_power,
            price_sensitivity=data.get("price_sensitivity", 0.5),
            brand_loyalty=data.get("brand_loyalty", 0.5),
            shopping_frequency=shopping_frequency,
            preferred_categories=data.get("preferred_categories", []),
            platform_preference=data.get("platform_preference", []),
            decision_factors=data.get(
                "decision_factors",
                {
                    "price": 0.3,
                    "quality": 0.25,
                    "brand": 0.2,
                    "reviews": 0.15,
                    "trend": 0.1,
                },
            ),
            age=data.get("age"),
            gender=data.get("gender"),
            mbti=data.get("mbti"),
            city=data.get("city"),
            profession=data.get("profession"),
        )

    def get_decision_weight(self, factor: str) -> float:
        """获取特定决策因素的权重"""
        return self.decision_factors.get(factor, 0.0)

    def is_price_sensitive(self, threshold: float = 0.6) -> bool:
        """判断是否价格敏感"""
        return self.price_sensitivity >= threshold

    def is_brand_loyal(self, threshold: float = 0.6) -> bool:
        """判断是否品牌忠诚"""
        return self.brand_loyalty >= threshold

    def get_summary(self) -> str:
        """获取消费者画像摘要"""
        return (
            f"{self.name} ({self.age}岁, {self.city or '未知城市'}) - "
            f"消费能力: {self.purchasing_power.value}, "
            f"购物频率: {self.shopping_frequency.value}, "
            f"偏好品类: {', '.join(self.preferred_categories[:3]) or '无'}"
        )
