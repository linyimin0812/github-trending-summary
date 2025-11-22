#!/usr/bin/env python3
"""GitHub Trending Daily Analyzer - 主程序"""

import sys
from typing import List
from config import (
    MAX_PROJECTS_PER_RUN, 
    MIN_STARS_THRESHOLD,
    TRENDING_LANGUAGE,
    TRENDING_SINCE
)
from src.github_trending import GitHubTrending, TrendingProject
from src.gemini_analyzer import GeminiAnalyzer
from src.ntfy_notifier import NtfyNotifier
from src.database import TrendingDatabase


def main():
    """主函数"""
    print("🚀 Starting GitHub Trending Daily Analyzer...")
    
    # 初始化组件
    db = TrendingDatabase()
    trending = GitHubTrending(language=TRENDING_LANGUAGE, since=TRENDING_SINCE)
    analyzer = GeminiAnalyzer()
    notifier = NtfyNotifier()
    
    # 清理旧记录
    db.cleanup_old_records(days=365)
    
    # 获取 trending 项目
    print(f"📡 Fetching trending projects (language={TRENDING_LANGUAGE or 'all'})...")
    projects = trending.get_trending_projects(max_count=MAX_PROJECTS_PER_RUN * 2)
    
    if not projects:
        print("⚠️  No trending projects found.")
        return
    
    print(f"✅ Found {len(projects)} trending projects")
    
    # 过滤和处理项目
    processed_count = 0
    success_count = 0
    
    for project in projects:
        # 检查是否已推送
        if db.is_project_pushed(project.name):
            print(f"⏭️  Skipping {project.name} (already pushed)")
            continue
        
        # 检查 stars 阈值
        if project.stars < MIN_STARS_THRESHOLD:
            print(f"⏭️  Skipping {project.name} (stars {project.stars} < {MIN_STARS_THRESHOLD})")
            continue
        
        # 达到最大处理数量
        if processed_count >= MAX_PROJECTS_PER_RUN:
            print(f"✋ Reached max projects limit ({MAX_PROJECTS_PER_RUN})")
            break
        
        print(f"\n🔍 Analyzing: {project.name}")
        print(f"   ⭐ {project.stars:,} stars (+{project.stars_today:,} today)")
        
        # 使用 Gemini 分析
        analysis = analyzer.analyze_project(project)
        
        # 发送通知
        if notifier.send_project_analysis(project, analysis):
            # 记录到数据库
            db.add_project(
                repo_name=project.name,
                repo_url=project.url,
                stars=project.stars,
                description=project.description,
                language=project.language
            )
            success_count += 1
        
        processed_count += 1
    
    # 发送每日总结
    print(f"\n📊 Summary: Processed {processed_count}, Success {success_count}")
    notifier.send_daily_summary(processed_count, success_count)
    
    print("✨ Done!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)