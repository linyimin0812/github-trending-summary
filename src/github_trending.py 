import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from dataclasses import dataclass
import re


@dataclass
class TrendingProject:
    """GitHub trending 项目数据类"""
    name: str
    url: str
    description: str
    language: str
    stars: int
    forks: int
    stars_today: int


class GitHubTrending:
    """GitHub Trending 爬取器"""
    
    BASE_URL = 'https://github.com/trending'
    
    def __init__(self, language: str = '', since: str = 'daily'):
        """
        Args:
            language: 编程语言过滤 (如 'python', 'javascript')
            since: 时间范围 ('daily', 'weekly', 'monthly')
        """
        self.language = language
        self.since = since
    
    def get_trending_projects(self, max_count: int = 10) -> List[TrendingProject]:
        """获取 trending 项目列表"""
        url = self._build_url()
        
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
            }, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article', class_='Box-row')
            
            projects = []
            for article in articles[:max_count]:
                project = self._parse_project(article)
                if project:
                    projects.append(project)
            
            return projects
            
        except Exception as e:
            print(f"Error fetching trending projects: {e}")
            return []
    
    def _build_url(self) -> str:
        """构建 trending URL"""
        url = self.BASE_URL
        if self.language:
            url += f'/{self.language}'
        url += f'?since={self.since}'
        return url
    
    def _parse_project(self, article) -> Optional[TrendingProject]:
        """解析单个项目信息"""
        try:
            # 项目名称和URL
            h2 = article.find('h2', class_='h3')
            if not h2:
                return None
            
            link = h2.find('a')
            if not link:
                return None
            
            name = link.get('href', '').strip('/')
            url = f"https://github.com{link.get('href', '')}"
            
            # 描述
            desc_elem = article.find('p', class_='col-9')
            description = desc_elem.get_text(strip=True) if desc_elem else ''
            
            # 编程语言
            lang_elem = article.find('span', itemprop='programmingLanguage')
            language = lang_elem.get_text(strip=True) if lang_elem else 'Unknown'
            
            # Stars
            stars_elem = article.find('a', href=re.compile(r'/stargazers$'))
            stars_text = stars_elem.get_text(strip=True) if stars_elem else '0'
            stars = self._parse_number(stars_text)
            
            # Forks
            forks_elem = article.find('a', href=re.compile(r'/forks$'))
            forks_text = forks_elem.get_text(strip=True) if forks_elem else '0'
            forks = self._parse_number(forks_text)
            
            # Stars today
            stars_today_elem = article.find('span', class_='d-inline-block float-sm-right')
            stars_today_text = stars_today_elem.get_text(strip=True) if stars_today_elem else '0'
            stars_today = self._parse_number(stars_today_text.split()[0])
            
            return TrendingProject(
                name=name,
                url=url,
                description=description,
                language=language,
                stars=stars,
                forks=forks,
                stars_today=stars_today
            )
            
        except Exception as e:
            print(f"Error parsing project: {e}")
            return None
    
    def _parse_number(self, text: str) -> int:
        """解析数字 (处理 1k, 1.5k 等格式)"""
        text = text.strip().replace(',', '')
        if 'k' in text.lower():
            return int(float(text.lower().replace('k', '')) * 1000)
        return int(text) if text.isdigit() else 0