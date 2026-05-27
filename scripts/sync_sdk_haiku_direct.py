import os
import json
import requests
from pathlib import Path
import re

GITHUB_MODELS_HOST = os.getenv('GITHUB_MODELS_HOST', 'https://models.github.ai')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Claude Haiku 4.5模型
HAIKU_MODEL = "claude-haiku-4-5-20251001"

def call_haiku(prompt: str, system_prompt: str = "") -> str:
    """调用Claude Haiku 4.5"""
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    messages = []
    
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    
    messages.append({
        "role": "user",
        "content": prompt
    })
    
    payload = {
        "model": HAIKU_MODEL,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 4096
    }
    
    try:
        print(f"  🤖 调用Haiku 4.5...")
        response = requests.post(
            f"{GITHUB_MODELS_HOST}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            print(f"  ✅ Haiku响应成功")
            return content
        else:
            print(f"  ❌ API错误 ({response.status_code}): {response.text[:200]}")
            return ""
    
    except Exception as e:
        print(f"  ❌ 调用失败: {e}")
        return ""

def extract_patches_summary(changes_info):
    """从变更信息中生成补丁摘要"""
    
    summary = f"""
微信支付API文档变更: {changes_info['commit_sha'][:8]}
提交信息: {changes_info['message']}
作者: {changes_info['author']}
统计: {changes_info['files_changed']} 个文件，+{changes_info['total_additions']} -{changes_info['total_deletions']}

文件变更详情:
"""
    
    for file_info in changes_info['files']:
        summary += f"\n{'='*60}\n"
        summary += f"文件: {file_info['filename']} ({file_info['status']})\n"
        summary += f"变更: +{file_info['additions']} -{file_info['deletions']}\n"
        
        if file_info['patch']:
            # 限制patch大小以避免token溢出
            patch = file_info['patch']
            if len(patch) > 2000:
                patch = patch[:2000] + "\n... (补丁过长，已截断)"
            summary += f"\n补丁内容:\n{patch}\n"
    
    return summary

def sync_sdk_with_haiku():
    """使用Haiku直接处理变更并更新SDK"""
    
    # 读取API变更信息
    if not Path('api_changes_full.json').exists():
        print("❌ 未找到API变更信息")
        return False
    
    with open('api_changes_full.json', 'r', encoding='utf-8') as f:
        changes_info = json.load(f)
    
    print("\n🔍 分析API变更...")
    
    # 生成补丁摘要（限制大小以适应token限制）
    patches_summary = extract_patches_summary(changes_info)
    
    # 限制摘要大小
    if len(patches_summary) > 6000:
        patches_summary = patches_summary[:6000] + "\n... (摘要过长，已截断)"
    
    # 系统提示 - 定义Haiku的角色和任务
    system_prompt = """你是一个专业的Python SDK开发者和API集成专家。

你的任务:
1. 分析上游API的变更
2. 理解变更对SDK的影响
3. 更新Python SDK代码以适应API变更
4. 保持代码风格和结构的一致性

当前项目: 微信支付 API v3 Python SDK

要求:
- 生成的代码必须是完整可运行的Python代码
- 使用类型提示 (typing module)
- 添加详细的docstring
- 支持async/await异步调用
- 遵循RESTful API最佳实践
- 包含参数验证和错误处理

输出格式要求:
- 对于新增或修改的代码，用 FILE_PATH: 标记文件路径
- 在 ```python 代码块中给出完整代码
- 对于删除的代码，明确说明要删除的方法/类
"""
    
    # 第一步：分析变更
    analysis_prompt = f"""
以下是微信支付API文档的最新变更记录:

{patches_summary}

请分析这些变更，回答以下问题（用中文，控制在200字以内）:
1. API有什么主要变更?
2. 这些变更对SDK的影响是什么?
3. SDK需要进行哪些更新?
"""
    
    print("\n📋 第一步: Haiku分析API变更...")
    analysis = call_haiku(analysis_prompt, system_prompt)
    
    if not analysis:
        print("❌ 分析失败")
        return False
    
    print(f"\n分析结果:\n{analysis}\n")
    
    # 第二步：生成SDK更新代码
    generation_prompt = f"""
基于以上分析结果，生成SDK的完整更新代码。

现有SDK结构:
- wechatpayv3/__init__.py - 包导出
- wechatpayv3/core.py - 核心功能和公共方法
- wechatpayv3/utils.py - 工具函数
- wechatpayv3/exceptions.py - 自定义异常类
- wechatpayv3/type.py - 类型定义
- wechatpayv3/... - API接口文件
- wechatpayv3/async_/ - 异步API实现

API变更摘要:
{patches_summary[:3000]}

请按照以下格式生成需要更新的代码:

对于每个需要添加或修改的文件，使用:
FILE_PATH: <文件路径>
```python
<完整的Python代码>
```

对于删除的内容，使用: DELETE_METHOD: <类名.方法名> 或 DELETE_CLASS: <类名>

要求:

只输出需要新增或修改的部分

代码必须完整可运行

包含完整的类型提示和docstring

提供__init__导出声明 
"""

    print("💻 第二步: Haiku生成SDK更新代码...") 
    sdk_updates = call_haiku(generation_prompt, system_prompt)

    if not sdk_updates: 
        print("❌ 代码生成失败") 
        return False

def apply_sdk_updates(updates: str): 
    """应用Haiku生成的SDK更新"""
    lines = updates.split('\n')
    current_file = None
    current_code = []
    in_code_block = False
    deletions = []

    changes_applied = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 处理新增/修改文件
        if line.startswith('FILE_PATH:'):
            # 保存之前的文件
            if current_file and current_code:
                if save_sdk_file(current_file, '\n'.join(current_code)):
                    changes_applied += 1
            
            current_file = line.replace('FILE_PATH:', '').strip()
            current_code = []
            in_code_block = False
            print(f"  准备更新: {current_file}")
        
        # 处理删除操作
        elif line.startswith('DELETE_METHOD:'):
            method_path = line.replace('DELETE_METHOD:', '').strip()
            deletions.append(('method', method_path))
            print(f"  标记删除方法: {method_path}")
        
        elif line.startswith('DELETE_CLASS:'):
            class_name = line.replace('DELETE_CLASS:', '').strip()
            deletions.append(('class', class_name))
            print(f"  标记删除类: {class_name}")
        
        # 处理代码块
        elif line.startswith('```python'):
            in_code_block = True
        
        elif line.startswith('```') and in_code_block:
            # 代码块结束，保存文件
            in_code_block = False
            if current_file and current_code:
                if save_sdk_file(current_file, '\n'.join(current_code)):
                    changes_applied += 1
                current_file = None
                current_code = []
        
        elif in_code_block:
            current_code.append(line)
        
        i += 1

    # 保存最后一个文件
    if current_file and current_code:
        if save_sdk_file(current_file, '\n'.join(current_code)):
            changes_applied += 1

    print(f"\n✅ 应用了 {changes_applied} 个文件更新")

    if deletions:
        print(f"\n⚠️  需要手动删除:")
        for del_type, del_name in deletions:
            print(f"  - [{del_type}] {del_name}")

    return changes_applied > 0    

def save_sdk_file(filepath: str, content: str) -> bool: 
    """保存SDK文件"""
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # 清理代码
        content = content.strip()
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"    ✓ 已保存: {filepath}")
        return True

    except Exception as e:
        print(f"    ✗ 保存失败 {filepath}: {e}")
        return False    

if __name__ == '__main__':
    print("🚀 使用Haiku 4.5同步SDK...\n")
    try:
        success = sync_sdk_with_haiku()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        exit(1)
