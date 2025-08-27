#!/usr/bin/env python3
"""
测试完整的推荐流程
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_planning import TravelPlanningSession
from travel_recommendation_engine import TravelRecommendationEngine

def test_full_flow():
    """测试完整流程"""
    print("🧪 测试完整推荐流程...")
    
    # 创建会话并手动设置数据
    session = TravelPlanningSession("test_session")
    
    # 手动更新信息
    print("📝 手动设置会话数据...")
    session.update_collected_info("destination", "Toronto")
    session.update_collected_info("group_size", "2个人")
    session.update_collected_info("budget_range", 200)
    
    print(f"✅ 会话信息: {session.collected_info}")
    print(f"✅ 步骤完成: {session.step_completion}")
    print(f"✅ 是否足够信息: {session.has_sufficient_information()}")
    print(f"✅ 完成度: {session.get_completion_percentage():.1f}%")
    print()
    
    if session.has_sufficient_information():
        print("🎯 生成推荐...")
        engine = TravelRecommendationEngine()
        recommendations = engine.generate_travel_recommendations(session)
        
        print(f"📊 推荐类型: {recommendations.get('type')}")
        if recommendations.get('type') == 'recommendations':
            print(f"🏠 推荐房源数量: {len(recommendations.get('properties', []))}")
            print(f"📝 推荐文本长度: {len(recommendations.get('recommendation_text', ''))} 字符")
            
            print("\n💡 推荐文本:")
            text = recommendations.get('recommendation_text', '')
            lines = text.split('\n')[:15]  # 显示前15行
            for line in lines:
                print(f"  {line}")
            if len(text.split('\n')) > 15:
                print("  ...")
        else:
            print(f"❌ 推荐失败: {recommendations.get('message', '')}")
    else:
        print("❌ 信息不足，无法生成推荐")

if __name__ == "__main__":
    test_full_flow()

