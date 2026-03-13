"""
测试消费属性功能

测试内容：
1. OasisAgentProfile dataclass 新字段的正确性
2. to_reddit_format/to_twitter_format/to_dict 方法包含消费属性
3. 规则生成方法的消费属性默认值
4. [待确认] LLM 生成消费属性测试（需要大模型API）

⚠️ 重要：涉及调用大模型API的测试已标记为待确认，不会执行
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
import json

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.oasis_profile_generator import (
    OasisAgentProfile,
    OasisProfileGenerator
)
from app.services.zep_entity_reader import EntityNode


class TestOasisAgentProfileConsumptionAttributes(unittest.TestCase):
    """测试 OasisAgentProfile 消费属性字段"""
    
    def test_profile_has_consumption_attributes(self):
        """测试 Profile 包含所有消费属性字段"""
        profile = OasisAgentProfile(
            user_id=1,
            user_name="test_user_123",
            name="测试用户",
            bio="这是一个测试简介",
            persona="这是一个测试人设描述",
            # 消费属性
            consumption_level="high",
            price_sensitivity="low",
            brand_preference="偏好国际大牌，追求品质",
            shopping_habits="喜欢在高端商场购物，注重购物体验",
            decision_style="mixed"
        )
        
        # 验证消费属性字段存在且值正确
        self.assertEqual(profile.consumption_level, "high")
        self.assertEqual(profile.price_sensitivity, "low")
        self.assertEqual(profile.brand_preference, "偏好国际大牌，追求品质")
        self.assertEqual(profile.shopping_habits, "喜欢在高端商场购物，注重购物体验")
        self.assertEqual(profile.decision_style, "mixed")
    
    def test_profile_consumption_attributes_can_be_none(self):
        """测试消费属性字段可以为None"""
        profile = OasisAgentProfile(
            user_id=1,
            user_name="test_user_123",
            name="测试用户",
            bio="这是一个测试简介",
            persona="这是一个测试人设描述"
        )
        
        # 验证消费属性字段默认为None
        self.assertIsNone(profile.consumption_level)
        self.assertIsNone(profile.price_sensitivity)
        self.assertIsNone(profile.brand_preference)
        self.assertIsNone(profile.shopping_habits)
        self.assertIsNone(profile.decision_style)
    
    def test_to_reddit_format_includes_consumption_attributes(self):
        """测试 to_reddit_format 方法包含消费属性"""
        profile = OasisAgentProfile(
            user_id=1,
            user_name="test_user_123",
            name="测试用户",
            bio="这是一个测试简介",
            persona="这是一个测试人设描述",
            consumption_level="medium",
            price_sensitivity="high",
            brand_preference="无品牌偏好",
            shopping_habits="货比三家",
            decision_style="rational"
        )
        
        reddit_format = profile.to_reddit_format()
        
        # 验证基础字段
        self.assertEqual(reddit_format["user_id"], 1)
        self.assertEqual(reddit_format["username"], "test_user_123")
        
        # 验证消费属性字段
        self.assertEqual(reddit_format["consumption_level"], "medium")
        self.assertEqual(reddit_format["price_sensitivity"], "high")
        self.assertEqual(reddit_format["brand_preference"], "无品牌偏好")
        self.assertEqual(reddit_format["shopping_habits"], "货比三家")
        self.assertEqual(reddit_format["decision_style"], "rational")
    
    def test_to_reddit_format_omits_none_consumption_attributes(self):
        """测试 to_reddit_format 方法省略 None 的消费属性"""
        profile = OasisAgentProfile(
            user_id=1,
            user_name="test_user_123",
            name="测试用户",
            bio="这是一个测试简介",
            persona="这是一个测试人设描述"
        )
        
        reddit_format = profile.to_reddit_format()
        
        # 验证 None 的消费属性不会被添加到字典中
        self.assertNotIn("consumption_level", reddit_format)
        self.assertNotIn("price_sensitivity", reddit_format)
        self.assertNotIn("brand_preference", reddit_format)
        self.assertNotIn("shopping_habits", reddit_format)
        self.assertNotIn("decision_style", reddit_format)
    
    def test_to_twitter_format_includes_consumption_attributes(self):
        """测试 to_twitter_format 方法包含消费属性"""
        profile = OasisAgentProfile(
            user_id=1,
            user_name="test_user_123",
            name="测试用户",
            bio="这是一个测试简介",
            persona="这是一个测试人设描述",
            consumption_level="low",
            price_sensitivity="high",
            brand_preference="追求性价比",
            shopping_habits="电商购物为主",
            decision_style="rational"
        )
        
        twitter_format = profile.to_twitter_format()
        
        # 验证消费属性字段
        self.assertEqual(twitter_format["consumption_level"], "low")
        self.assertEqual(twitter_format["price_sensitivity"], "high")
        self.assertEqual(twitter_format["brand_preference"], "追求性价比")
        self.assertEqual(twitter_format["shopping_habits"], "电商购物为主")
        self.assertEqual(twitter_format["decision_style"], "rational")
    
    def test_to_dict_includes_consumption_attributes(self):
        """测试 to_dict 方法包含消费属性"""
        profile = OasisAgentProfile(
            user_id=1,
            user_name="test_user_123",
            name="测试用户",
            bio="这是一个测试简介",
            persona="这是一个测试人设描述",
            consumption_level="high",
            price_sensitivity="medium",
            brand_preference="品牌忠诚度高",
            shopping_habits="线下购物为主",
            decision_style="emotional"
        )
        
        dict_format = profile.to_dict()
        
        # 验证消费属性字段
        self.assertEqual(dict_format["consumption_level"], "high")
        self.assertEqual(dict_format["price_sensitivity"], "medium")
        self.assertEqual(dict_format["brand_preference"], "品牌忠诚度高")
        self.assertEqual(dict_format["shopping_habits"], "线下购物为主")
        self.assertEqual(dict_format["decision_style"], "emotional")


class TestRuleBasedGenerationWithConsumptionAttributes(unittest.TestCase):
    """测试规则生成方法的消费属性"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建一个模拟的配置
        self.mock_config = Mock()
        self.mock_config.LLM_API_KEY = "test_key"
        self.mock_config.LLM_BASE_URL = "https://test.com"
        self.mock_config.LLM_MODEL_NAME = "test_model"
        self.mock_config.ZEP_API_KEY = None
        
        # 修补配置导入
        self.config_patcher = patch('app.services.oasis_profile_generator.Config', self.mock_config)
        self.config_patcher.start()
        
        # 创建生成器实例
        self.generator = OasisProfileGenerator()
    
    def tearDown(self):
        """清理测试环境"""
        self.config_patcher.stop()
    
    def test_student_profile_has_consumption_attributes(self):
        """测试学生类型实体的消费属性"""
        profile_data = self.generator._generate_profile_rule_based(
            entity_name="张三",
            entity_type="student",
            entity_summary="一个大学生",
            entity_attributes={}
        )
        
        # 验证消费属性存在
        self.assertIn("consumption_level", profile_data)
        self.assertIn("price_sensitivity", profile_data)
        self.assertIn("brand_preference", profile_data)
        self.assertIn("shopping_habits", profile_data)
        self.assertIn("decision_style", profile_data)
        
        # 验证学生消费属性的合理性
        self.assertIn(profile_data["consumption_level"], ["low", "medium"])
        self.assertIn(profile_data["price_sensitivity"], ["medium", "high"])
        self.assertIn(profile_data["decision_style"], ["rational", "mixed"])
    
    def test_expert_profile_has_consumption_attributes(self):
        """测试专家类型实体的消费属性"""
        profile_data = self.generator._generate_profile_rule_based(
            entity_name="李教授",
            entity_type="professor",
            entity_summary="知名教授",
            entity_attributes={}
        )
        
        # 验证消费属性存在
        self.assertIn("consumption_level", profile_data)
        self.assertIn("price_sensitivity", profile_data)
        self.assertIn("brand_preference", profile_data)
        self.assertIn("shopping_habits", profile_data)
        self.assertIn("decision_style", profile_data)
        
        # 验证专家消费属性的合理性
        self.assertIn(profile_data["consumption_level"], ["medium", "high"])
        self.assertIn(profile_data["price_sensitivity"], ["low", "medium"])
    
    def test_mediaoutlet_profile_has_consumption_attributes(self):
        """测试媒体机构类型实体的消费属性"""
        profile_data = self.generator._generate_profile_rule_based(
            entity_name="某报社",
            entity_type="mediaoutlet",
            entity_summary="官方媒体",
            entity_attributes={}
        )
        
        # 验证消费属性存在
        self.assertIn("consumption_level", profile_data)
        self.assertIn("price_sensitivity", profile_data)
        self.assertIn("brand_preference", profile_data)
        self.assertIn("shopping_habits", profile_data)
        self.assertIn("decision_style", profile_data)
        
        # 验证机构消费属性
        self.assertEqual(profile_data["decision_style"], "rational")
        self.assertEqual(profile_data["consumption_level"], "medium")
        self.assertEqual(profile_data["price_sensitivity"], "medium")
    
    def test_organization_profile_has_consumption_attributes(self):
        """测试机构类型实体的消费属性"""
        profile_data = self.generator._generate_profile_rule_based(
            entity_name="某大学",
            entity_type="university",
            entity_summary="知名大学",
            entity_attributes={}
        )
        
        # 验证消费属性存在
        self.assertIn("consumption_level", profile_data)
        self.assertIn("price_sensitivity", profile_data)
        self.assertIn("brand_preference", profile_data)
        self.assertIn("shopping_habits", profile_data)
        self.assertIn("decision_style", profile_data)
        
        # 验证公共机构消费属性
        self.assertEqual(profile_data["decision_style"], "rational")
        self.assertEqual(profile_data["consumption_level"], "medium")
        self.assertEqual(profile_data["price_sensitivity"], "high")


class TestConsumptionAttributeValidValues(unittest.TestCase):
    """测试消费属性字段的有效值"""
    
    def test_consumption_level_valid_values(self):
        """测试消费能力等级的有效值"""
        valid_values = ["high", "medium", "low"]
        
        for value in valid_values:
            profile = OasisAgentProfile(
                user_id=1,
                user_name="test",
                name="测试",
                bio="简介",
                persona="人设",
                consumption_level=value
            )
            self.assertEqual(profile.consumption_level, value)
    
    def test_price_sensitivity_valid_values(self):
        """测试价格敏感度的有效值"""
        valid_values = ["high", "medium", "low"]
        
        for value in valid_values:
            profile = OasisAgentProfile(
                user_id=1,
                user_name="test",
                name="测试",
                bio="简介",
                persona="人设",
                price_sensitivity=value
            )
            self.assertEqual(profile.price_sensitivity, value)
    
    def test_decision_style_valid_values(self):
        """测试决策风格的有效值"""
        valid_values = ["rational", "emotional", "mixed"]
        
        for value in valid_values:
            profile = OasisAgentProfile(
                user_id=1,
                user_name="test",
                name="测试",
                bio="简介",
                persona="人设",
                decision_style=value
            )
            self.assertEqual(profile.decision_style, value)


class TestLLMGenerationWithConsumptionAttributes(unittest.TestCase):
    """
    ⚠️ 待确认测试：涉及调用大模型API
    
    以下测试需要调用大模型API，已标记为待确认状态。
    在确认API可用性和成本后，可以取消跳过标记并执行。
    """
    
    @unittest.skip("⚠️ 待确认：需要调用大模型API，请确认后取消跳过")
    def test_llm_generates_consumption_attributes_for_individual(self):
        """[待确认] 测试LLM为个人实体生成消费属性"""
        pass
    
    @unittest.skip("⚠️ 待确认：需要调用大模型API，请确认后取消跳过")
    def test_llm_generates_consumption_attributes_for_group(self):
        """[待确认] 测试LLM为群体实体生成消费属性"""
        pass
    
    @unittest.skip("⚠️ 待确认：需要调用大模型API，请确认后取消跳过")
    def test_llm_consumption_attributes_consistency_with_persona(self):
        """[待确认] 测试LLM生成的消费属性与人设的一致性"""
        pass
    
    @unittest.skip("⚠️ 待确认：需要调用大模型API，请确认后取消跳过")
    def test_llm_consumption_attributes_json_parsing(self):
        """[待确认] 测试LLM返回的消费属性JSON解析"""
        pass
    
    @unittest.skip("⚠️ 待确认：需要调用大模型API，请确认后取消跳过")
    def test_full_pipeline_with_consumption_attributes(self):
        """[待确认] 测试完整流程：从实体生成带消费属性的Profile"""
        pass


class TestSaveProfilesWithConsumptionAttributes(unittest.TestCase):
    """测试保存Profile时包含消费属性"""
    
    def test_save_reddit_json_includes_consumption_attributes(self):
        """测试保存Reddit JSON格式包含消费属性"""
        import tempfile
        import os
        
        # 创建测试Profile列表
        profiles = [
            OasisAgentProfile(
                user_id=1,
                user_name="user_1",
                name="用户1",
                bio="简介1",
                persona="人设1",
                consumption_level="high",
                price_sensitivity="low",
                brand_preference="偏好高端品牌",
                shopping_habits="线下购物",
                decision_style="emotional"
            ),
            OasisAgentProfile(
                user_id=2,
                user_name="user_2",
                name="用户2",
                bio="简介2",
                persona="人设2",
                consumption_level="low",
                price_sensitivity="high",
                brand_preference="追求性价比",
                shopping_habits="电商购物",
                decision_style="rational"
            )
        ]
        
        # 模拟配置
        with patch('app.services.oasis_profile_generator.Config') as mock_config:
            mock_config.LLM_API_KEY = "test_key"
            mock_config.LLM_BASE_URL = "https://test.com"
            mock_config.LLM_MODEL_NAME = "test_model"
            mock_config.ZEP_API_KEY = None
            
            generator = OasisProfileGenerator()
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                temp_path = f.name
            
            try:
                # 保存
                generator.save_profiles(profiles, temp_path, platform="reddit")
                
                # 读取并验证
                with open(temp_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 验证数量
                self.assertEqual(len(data), 2)
                
                # 验证第一个Profile的消费属性
                self.assertEqual(data[0]["consumption_level"], "high")
                self.assertEqual(data[0]["price_sensitivity"], "low")
                self.assertEqual(data[0]["brand_preference"], "偏好高端品牌")
                self.assertEqual(data[0]["shopping_habits"], "线下购物")
                self.assertEqual(data[0]["decision_style"], "emotional")
                
                # 验证第二个Profile的消费属性
                self.assertEqual(data[1]["consumption_level"], "low")
                self.assertEqual(data[1]["price_sensitivity"], "high")
                self.assertEqual(data[1]["brand_preference"], "追求性价比")
                self.assertEqual(data[1]["shopping_habits"], "电商购物")
                self.assertEqual(data[1]["decision_style"], "rational")
                
            finally:
                # 清理临时文件
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
    
    def test_save_with_none_consumption_attributes_gets_defaults(self):
        """测试保存时None的消费属性获得默认值"""
        import tempfile
        import os
        
        # 创建没有消费属性的Profile
        profiles = [
            OasisAgentProfile(
                user_id=1,
                user_name="user_1",
                name="用户1",
                bio="简介1",
                persona="人设1"
                # 不设置消费属性
            )
        ]
        
        # 模拟配置
        with patch('app.services.oasis_profile_generator.Config') as mock_config:
            mock_config.LLM_API_KEY = "test_key"
            mock_config.LLM_BASE_URL = "https://test.com"
            mock_config.LLM_MODEL_NAME = "test_model"
            mock_config.ZEP_API_KEY = None
            
            generator = OasisProfileGenerator()
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                temp_path = f.name
            
            try:
                # 保存
                generator.save_profiles(profiles, temp_path, platform="reddit")
                
                # 读取并验证
                with open(temp_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 验证默认值被填充
                self.assertEqual(data[0]["consumption_level"], "medium")
                self.assertEqual(data[0]["price_sensitivity"], "medium")
                self.assertEqual(data[0]["brand_preference"], "综合考虑价格、质量和口碑，无特殊偏好")
                self.assertEqual(data[0]["shopping_habits"], "常规购物习惯，根据需求灵活调整")
                self.assertEqual(data[0]["decision_style"], "mixed")
                
            finally:
                # 清理临时文件
                if os.path.exists(temp_path):
                    os.unlink(temp_path)


def run_tests():
    """运行测试"""
    print("\n" + "="*70)
    print("消费属性功能测试")
    print("="*70)
    print("\n✅ 执行单元测试（不涉及大模型API）...")
    print("-"*70 + "\n")
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestOasisAgentProfileConsumptionAttributes))
    suite.addTests(loader.loadTestsFromTestCase(TestRuleBasedGenerationWithConsumptionAttributes))
    suite.addTests(loader.loadTestsFromTestCase(TestConsumptionAttributeValidValues))
    suite.addTests(loader.loadTestsFromTestCase(TestSaveProfilesWithConsumptionAttributes))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 打印跳过的测试
    print("\n" + "="*70)
    print("⚠️ 待确认测试（需要大模型API）")
    print("="*70)
    skipped_tests = [
        "test_llm_generates_consumption_attributes_for_individual",
        "test_llm_generates_consumption_attributes_for_group",
        "test_llm_consumption_attributes_consistency_with_persona",
        "test_llm_consumption_attributes_json_parsing",
        "test_full_pipeline_with_consumption_attributes"
    ]
    for test in skipped_tests:
        print(f"  ⏭️  {test} - 待确认API可用性后执行")
    
    # 总结
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    print(f"运行: {result.testsRun} 个测试")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)} 个")
    print(f"失败: {len(result.failures)} 个")
    print(f"错误: {len(result.errors)} 个")
    print(f"跳过: {len(result.skipped)} 个（待确认的大模型API测试）")
    print("="*70 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)