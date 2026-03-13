"""
独立测试脚本：消费属性功能验证

直接导入 oasis_profile_generator 模块进行测试，避免Flask依赖问题。
"""

import sys
import os
import json
import tempfile

# 添加项目路径
sys.path.insert(0, '/lhcos-data/MiroFish/backend')


def test_dataclass_fields():
    """测试 OasisAgentProfile dataclass 包含消费属性字段"""
    print("\n📋 测试1：OasisAgentProfile 消费属性字段")
    print("-" * 50)
    
    # 直接导入模块
    from app.services.oasis_profile_generator import OasisAgentProfile
    
    # 创建带消费属性的Profile
    profile = OasisAgentProfile(
        user_id=1,
        user_name="test_user_123",
        name="测试用户",
        bio="这是一个测试简介",
        persona="这是一个测试人设描述",
        consumption_level="high",
        price_sensitivity="low",
        brand_preference="偏好国际大牌，追求品质",
        shopping_habits="喜欢在高端商场购物，注重购物体验",
        decision_style="mixed"
    )
    
    # 验证字段
    assert profile.consumption_level == "high", "consumption_level 字段验证失败"
    assert profile.price_sensitivity == "low", "price_sensitivity 字段验证失败"
    assert profile.brand_preference == "偏好国际大牌，追求品质", "brand_preference 字段验证失败"
    assert profile.shopping_habits == "喜欢在高端商场购物，注重购物体验", "shopping_habits 字段验证失败"
    assert profile.decision_style == "mixed", "decision_style 字段验证失败"
    
    print("  ✅ 所有消费属性字段存在且值正确")


def test_dataclass_default_none():
    """测试消费属性字段默认为None"""
    print("\n📋 测试2：消费属性字段默认值")
    print("-" * 50)
    
    from app.services.oasis_profile_generator import OasisAgentProfile
    
    profile = OasisAgentProfile(
        user_id=1,
        user_name="test",
        name="测试",
        bio="简介",
        persona="人设"
    )
    
    assert profile.consumption_level is None, "consumption_level 默认值应为None"
    assert profile.price_sensitivity is None, "price_sensitivity 默认值应为None"
    assert profile.brand_preference is None, "brand_preference 默认值应为None"
    assert profile.shopping_habits is None, "shopping_habits 默认值应为None"
    assert profile.decision_style is None, "decision_style 默认值应为None"
    
    print("  ✅ 消费属性字段默认值正确（None）")


def test_to_reddit_format():
    """测试 to_reddit_format 方法包含消费属性"""
    print("\n📋 测试3：to_reddit_format 方法")
    print("-" * 50)
    
    from app.services.oasis_profile_generator import OasisAgentProfile
    
    profile = OasisAgentProfile(
        user_id=1,
        user_name="test_user",
        name="测试用户",
        bio="简介",
        persona="人设",
        consumption_level="medium",
        price_sensitivity="high",
        brand_preference="无品牌偏好",
        shopping_habits="货比三家",
        decision_style="rational"
    )
    
    reddit_format = profile.to_reddit_format()
    
    assert reddit_format["consumption_level"] == "medium"
    assert reddit_format["price_sensitivity"] == "high"
    assert reddit_format["brand_preference"] == "无品牌偏好"
    assert reddit_format["shopping_habits"] == "货比三家"
    assert reddit_format["decision_style"] == "rational"
    
    print("  ✅ to_reddit_format 方法正确包含消费属性")


def test_to_twitter_format():
    """测试 to_twitter_format 方法包含消费属性"""
    print("\n📋 测试4：to_twitter_format 方法")
    print("-" * 50)
    
    from app.services.oasis_profile_generator import OasisAgentProfile
    
    profile = OasisAgentProfile(
        user_id=1,
        user_name="test_user",
        name="测试用户",
        bio="简介",
        persona="人设",
        consumption_level="low",
        price_sensitivity="high",
        brand_preference="追求性价比",
        shopping_habits="电商购物为主",
        decision_style="rational"
    )
    
    twitter_format = profile.to_twitter_format()
    
    assert twitter_format["consumption_level"] == "low"
    assert twitter_format["price_sensitivity"] == "high"
    assert twitter_format["brand_preference"] == "追求性价比"
    assert twitter_format["shopping_habits"] == "电商购物为主"
    assert twitter_format["decision_style"] == "rational"
    
    print("  ✅ to_twitter_format 方法正确包含消费属性")


def test_to_dict():
    """测试 to_dict 方法包含消费属性"""
    print("\n📋 测试5：to_dict 方法")
    print("-" * 50)
    
    from app.services.oasis_profile_generator import OasisAgentProfile
    
    profile = OasisAgentProfile(
        user_id=1,
        user_name="test_user",
        name="测试用户",
        bio="简介",
        persona="人设",
        consumption_level="high",
        price_sensitivity="medium",
        brand_preference="品牌忠诚度高",
        shopping_habits="线下购物为主",
        decision_style="emotional"
    )
    
    dict_format = profile.to_dict()
    
    assert dict_format["consumption_level"] == "high"
    assert dict_format["price_sensitivity"] == "medium"
    assert dict_format["brand_preference"] == "品牌忠诚度高"
    assert dict_format["shopping_habits"] == "线下购物为主"
    assert dict_format["decision_style"] == "emotional"
    
    print("  ✅ to_dict 方法正确包含消费属性")


def test_rule_based_student():
    """测试规则生成：学生类型实体"""
    print("\n📋 测试6：规则生成 - 学生类型")
    print("-" * 50)
    
    from app.services.oasis_profile_generator import OasisProfileGenerator
    from unittest.mock import Mock, patch
    
    # 模拟配置
    with patch('app.services.oasis_profile_generator.Config') as mock_config:
        mock_config.LLM_API_KEY = "test_key"
        mock_config.LLM_BASE_URL = "https://test.com"
        mock_config.LLM_MODEL_NAME = "test_model"
        mock_config.ZEP_API_KEY = None
        
        generator = OasisProfileGenerator()
        
        profile_data = generator._generate_profile_rule_based(
            entity_name="张三",
            entity_type="student",
            entity_summary="一个大学生",
            entity_attributes={}
        )
        
        assert "consumption_level" in profile_data
        assert "price_sensitivity" in profile_data
        assert "brand_preference" in profile_data
        assert "shopping_habits" in profile_data
        assert "decision_style" in profile_data
        
        print(f"  consumption_level: {profile_data['consumption_level']}")
        print(f"  price_sensitivity: {profile_data['price_sensitivity']}")
        print(f"  brand_preference: {profile_data['brand_preference'][:30]}...")
        print(f"  decision_style: {profile_data['decision_style']}")
        print("  ✅ 学生类型消费属性生成正确")


def test_rule_based_expert():
    """测试规则生成：专家类型实体"""
    print("\n📋 测试7：规则生成 - 专家类型")
    print("-" * 50)
    
    from app.services.oasis_profile_generator import OasisProfileGenerator
    from unittest.mock import patch
    
    with patch('app.services.oasis_profile_generator.Config') as mock_config:
        mock_config.LLM_API_KEY = "test_key"
        mock_config.LLM_BASE_URL = "https://test.com"
        mock_config.LLM_MODEL_NAME = "test_model"
        mock_config.ZEP_API_KEY = None
        
        generator = OasisProfileGenerator()
        
        profile_data = generator._generate_profile_rule_based(
            entity_name="李教授",
            entity_type="professor",
            entity_summary="知名教授",
            entity_attributes={}
        )
        
        assert "consumption_level" in profile_data
        assert profile_data["consumption_level"] in ["medium", "high"]
        
        print(f"  consumption_level: {profile_data['consumption_level']}")
        print(f"  price_sensitivity: {profile_data['price_sensitivity']}")
        print(f"  decision_style: {profile_data['decision_style']}")
        print("  ✅ 专家类型消费属性生成正确")


def test_rule_based_organization():
    """测试规则生成：机构类型实体"""
    print("\n📋 测试8：规则生成 - 机构类型")
    print("-" * 50)
    
    from app.services.oasis_profile_generator import OasisProfileGenerator
    from unittest.mock import patch
    
    with patch('app.services.oasis_profile_generator.Config') as mock_config:
        mock_config.LLM_API_KEY = "test_key"
        mock_config.LLM_BASE_URL = "https://test.com"
        mock_config.LLM_MODEL_NAME = "test_model"
        mock_config.ZEP_API_KEY = None
        
        generator = OasisProfileGenerator()
        
        profile_data = generator._generate_profile_rule_based(
            entity_name="某大学",
            entity_type="university",
            entity_summary="知名大学",
            entity_attributes={}
        )
        
        assert profile_data["decision_style"] == "rational"
        assert profile_data["consumption_level"] == "medium"
        assert profile_data["price_sensitivity"] == "high"
        
        print(f"  consumption_level: {profile_data['consumption_level']}")
        print(f"  price_sensitivity: {profile_data['price_sensitivity']}")
        print(f"  decision_style: {profile_data['decision_style']}")
        print("  ✅ 机构类型消费属性生成正确")


def test_save_reddit_json():
    """测试保存Reddit JSON包含消费属性"""
    print("\n📋 测试9：保存Reddit JSON格式")
    print("-" * 50)
    
    from app.services.oasis_profile_generator import OasisAgentProfile, OasisProfileGenerator
    from unittest.mock import patch
    
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
            generator.save_profiles(profiles, temp_path, platform="reddit")
            
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert len(data) == 2
            assert data[0]["consumption_level"] == "high"
            assert data[1]["consumption_level"] == "low"
            
            print(f"  保存文件: {temp_path}")
            print(f"  Profile数量: {len(data)}")
            print(f"  Profile 1 consumption_level: {data[0]['consumption_level']}")
            print(f"  Profile 2 consumption_level: {data[1]['consumption_level']}")
            print("  ✅ 保存功能正确包含消费属性")
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


def test_save_with_none_gets_defaults():
    """测试保存时None的消费属性获得默认值"""
    print("\n📋 测试10：保存时None值获得默认值")
    print("-" * 50)
    
    from app.services.oasis_profile_generator import OasisAgentProfile, OasisProfileGenerator
    from unittest.mock import patch
    
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
    
    with patch('app.services.oasis_profile_generator.Config') as mock_config:
        mock_config.LLM_API_KEY = "test_key"
        mock_config.LLM_BASE_URL = "https://test.com"
        mock_config.LLM_MODEL_NAME = "test_model"
        mock_config.ZEP_API_KEY = None
        
        generator = OasisProfileGenerator()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            generator.save_profiles(profiles, temp_path, platform="reddit")
            
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert data[0]["consumption_level"] == "medium"
            assert data[0]["price_sensitivity"] == "medium"
            assert data[0]["decision_style"] == "mixed"
            
            print(f"  默认 consumption_level: {data[0]['consumption_level']}")
            print(f"  默认 price_sensitivity: {data[0]['price_sensitivity']}")
            print(f"  默认 decision_style: {data[0]['decision_style']}")
            print("  ✅ None值正确获得默认值")
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*70)
    print("消费属性功能测试")
    print("="*70)
    
    tests = [
        test_dataclass_fields,
        test_dataclass_default_none,
        test_to_reddit_format,
        test_to_twitter_format,
        test_to_dict,
        test_rule_based_student,
        test_rule_based_expert,
        test_rule_based_organization,
        test_save_reddit_json,
        test_save_with_none_gets_defaults,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ❌ 测试失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ 测试异常: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    print(f"✅ 通过: {passed}/{len(tests)}")
    print(f"❌ 失败: {failed}/{len(tests)}")
    print("="*70)
    
    print("\n⚠️ 待确认测试（需要大模型API）:")
    print("-" * 50)
    skipped = [
        "test_llm_generates_consumption_attributes_for_individual",
        "test_llm_generates_consumption_attributes_for_group",
        "test_llm_consumption_attributes_consistency_with_persona",
        "test_llm_consumption_attributes_json_parsing",
        "test_full_pipeline_with_consumption_attributes"
    ]
    for s in skipped:
        print(f"  ⏭️  {s}")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)