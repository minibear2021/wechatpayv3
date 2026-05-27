import argparse
import json
import requests
from pathlib import Path
import sys

def get_commit_info(repo, sha):
    """获取提交的完整信息和diff内容"""
    
    url = f"https://api.github.com/repos/{repo}/commits/{sha}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        commit_data = response.json()
        
        # 提取变更信息
        changes_info = {
            'commit_sha': sha,
            'author': commit_data.get('commit', {}).get('author', {}).get('name', 'Unknown'),
            'date': commit_data.get('commit', {}).get('author', {}).get('date', ''),
            'message': commit_data.get('commit', {}).get('message', ''),
            'files_changed': len(commit_data.get('files', [])),
            'total_additions': commit_data.get('stats', {}).get('additions', 0),
            'total_deletions': commit_data.get('stats', {}).get('deletions', 0),
            'files': []
        }
        
        # 收集每个文件的变更详情
        for file_info in commit_data.get('files', []):
            file_changes = {
                'filename': file_info.get('filename'),
                'status': file_info.get('status'),  # added, modified, removed, renamed
                'additions': file_info.get('additions', 0),
                'deletions': file_info.get('deletions', 0),
                'changes': file_info.get('changes', 0),
                'patch': file_info.get('patch', ''),  # 实际的diff内容
                'blob_url': file_info.get('blob_url', ''),
                'contents_url': file_info.get('contents_url', '')
            }
            changes_info['files'].append(file_changes)
        
        # 保存完整的变更信息
        with open('api_changes_full.json', 'w', encoding='utf-8') as f:
            json.dump(changes_info, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 已获取API变更信息 ({sha})")
        print(f"📝 提交信息: {changes_info['message'].split(chr(10))[0][:80]}...")
        print(f"📊 统计: {changes_info['files_changed']} 个文件变更")
        print(f"   +{changes_info['total_additions']} -{changes_info['total_deletions']}")
        
        # 打印文件变更摘要
        for file_info in changes_info['files'][:10]:
            status_symbol = {
                'added': '✨',
                'modified': '📝',
                'removed': '🗑️',
                'renamed': '♻️'
            }.get(file_info['status'], '📄')
            
            print(f"  {status_symbol} {file_info['filename']} ({file_info['status']})")
        
        if len(changes_info['files']) > 10:
            print(f"  ... 还有 {len(changes_info['files']) - 10} 个文件")
        
        return changes_info
        
    except Exception as e:
        print(f"❌ 获取变更失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', required=True, help='API文档仓库 (owner/repo)')
    parser.add_argument('--sha', required=True, help='提交SHA')
    args = parser.parse_args()
    
    get_commit_info(args.repo, args.sha)