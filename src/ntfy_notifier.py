import requests
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
        """发送项目分析通知
        
        Args:
            project: TrendingProject 对象
            analysis: Gemini 分析结果
            
        Returns:
            发送是否成功
        """
        title = f"{project.name} (+{project.stars_today:,} stars)"
        print(f"✅ Notification content: {analysis}")
        
        # 构建消息内容
        message = f"""
{analysis}

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
        """发送通用通知
        
        Args:
            title: 通知标题
            message: 通知内容
            priority: 优先级 (min, low, default, high, urgent)
            tags: 标签列表
            click_url: 点击链接
            
        Returns:
            发送是否成功
        """
        url = f"{self.server}/{self.topic}"
        
        headers = {
            'Title': title,
            'Priority': priority,
            'Content-Type': 'text/plain; charset=utf-8',
            "Markdown": "yes"
        }
        
        if tags:
            headers['Tags'] = ','.join(tags)
        
        if click_url:
            headers['Click'] = click_url
        
        try:
            response = requests.post(
                url,
                data=message.encode('utf-8'),
                headers=headers,
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
        title = "GitHub Trending 每日推送完成"
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
