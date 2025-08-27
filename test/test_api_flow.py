#!/usr/bin/env python3
"""
测试API流程
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_planning import TravelPlanningSession, extract_information_with_ai, TRAVEL_PLANNING_STEPS

async def simulate_api_flow():
    """模拟API流程"""
    print("🧪 模拟API流程...")
    
    # 创建会话
    session = TravelPlanningSession("test_session")
    print(f"初始步骤: {session.current_step}")
    
    # 模拟第一步: initial -> destination
    current_step = "initial"
    user_message = "Toronto"
    
    print(f"\n📝 处理步骤: {current_step}, 消息: '{user_message}'")
    
    # 提取信息
    extracted_info = await extract_information_with_ai(user_message, current_step, session)
    print(f"提取的信息: {extracted_info}")
    
    # 获取目标字段
    step_info = TRAVEL_PLANNING_STEPS.get(current_step, {})
    target_field = step_info.get("field")
    print(f"目标字段: {target_field}")
    
    # 更新信息
    if target_field:
        update_success = session.update_collected_info(target_field, extracted_info)
    else:
        # 对于initial步骤，手动处理
        if current_step == "initial":
            update_success = session.update_collected_info("destination", extracted_info)
        else:
            update_success = True
    
    print(f"更新成功: {update_success}")
    
    if update_success:
        # 移动到下一步
        session.current_step = TRAVEL_PLANNING_STEPS[current_step]["next"]
        print(f"下一步: {session.current_step}")
    
    print(f"会话信息: {session.collected_info}")
    print(f"步骤完成: {session.step_completion}")
    print(f"是否足够信息: {session.has_sufficient_information()}")
    
    # 继续第二步: destination -> dates
    current_step = session.current_step
    user_message = "next weekend"
    
    print(f"\n📝 处理步骤: {current_step}, 消息: '{user_message}'")
    
    extracted_info = await extract_information_with_ai(user_message, current_step, session)
    print(f"提取的信息: {extracted_info}")
    
    step_info = TRAVEL_PLANNING_STEPS.get(current_step, {})
    target_field = step_info.get("field")
    print(f"目标字段: {target_field}")
    
    if target_field:
        update_success = session.update_collected_info(target_field, extracted_info)
        print(f"更新成功: {update_success}")
        
        if update_success:
            session.current_step = TRAVEL_PLANNING_STEPS[current_step]["next"]
            print(f"下一步: {session.current_step}")
    
    print(f"会话信息: {session.collected_info}")
    print(f"步骤完成: {session.step_completion}")
    print(f"是否足够信息: {session.has_sufficient_information()}")

if __name__ == "__main__":
    asyncio.run(simulate_api_flow())

