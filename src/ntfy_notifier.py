import requests
import json
from typing import Optional
from config import NTFY_TOPIC, NTFY_SERVER
from github_trending import TrendingProject


class NtfyNotifier:
    """Ntfy 通知推送器"""
    
    def __init__(self, server: str = NTFY_SERVER, topic: str = NTFY_TOPIC):
        self.server = server.rstrip('/')
        self.topic = topic
    
    def send_project_analysis(self, project: TrendingProject, 
                            analysis: str) -> bool:
        """发送项目分析通知"""
        title = f"🔥 {project.name} (+{project.stars_today:,} ⭐)"
        
        message = f"""{analysis}

---
📊 **统计数据**
⭐ Stars: {project.stars:,} | 🍴 Forks: {project.forks:,}
📈 今日 Stars: +{project.stars_today:,}
💻 语言: {project.language}

🔗 {project.url}
"""
        
        return self.send_notification(
            title=title,
            message=message,
            priority='default',
            tags=['github', 'trending'],
            click_url=project.url
        )
    
    def send_notification(self, title: str, message: str,
                         priority: str = 'default',
                         tags: Optional[list] = None,
                         click_url: Optional[str] = None) -> bool:
        """发送通用通知（使用 JSON 格式）"""
        url = self.server
        
        # 使用 JSON 格式，完全支持 emoji
        payload = {
            'topic': self.topic,
            'title': title,
            'message': message,
            'priority': priority
        }
        
        if tags:
            payload['tags'] = tags
        
        if click_url:
            payload['click'] = click_url
        
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            print(f"✅ Notification sent: {title}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send notification: {e}")
            return False
    
    def send_daily_summary(self, project_count: int, success_count: int):
        """发送每日总结"""
        title = "📊 GitHub Trending 每日推送完成"
        message = f"""今日共处理 {project_count} 个热门项目
成功推送 {success_count} 个新项目分析

下次推送时间: 明天同一时间
"""
        
        self.send_notification(
            title=title,
            message=message,
            priority='low',
            tags=['summary']
        )
