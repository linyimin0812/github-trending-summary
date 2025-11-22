import sqlite3
import os
from datetime import datetime
from typing import List, Optional
from config import DB_PATH


class TrendingDatabase:
    """管理已推送项目的数据库"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS pushed_projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo_name TEXT UNIQUE NOT NULL,
                    repo_url TEXT NOT NULL,
                    stars INTEGER,
                    pushed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    description TEXT,
                    language TEXT
                )
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_repo_name 
                ON pushed_projects(repo_name)
            ''')
            conn.commit()
    
    def is_project_pushed(self, repo_name: str) -> bool:
        """检查项目是否已推送"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT COUNT(*) FROM pushed_projects WHERE repo_name = ?',
                (repo_name,)
            )
            count = cursor.fetchone()[0]
            return count > 0
    
    def add_project(self, repo_name: str, repo_url: str, 
                   stars: int, description: str = '', language: str = ''):
        """添加已推送项目记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR IGNORE INTO pushed_projects 
                (repo_name, repo_url, stars, description, language)
                VALUES (?, ?, ?, ?, ?)
            ''', (repo_name, repo_url, stars, description, language))
            conn.commit()
    
    def get_recent_projects(self, days: int = 30) -> List[str]:
        """获取最近N天推送的项目"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT repo_name FROM pushed_projects
                WHERE pushed_at >= datetime('now', '-' || ? || ' days')
                ORDER BY pushed_at DESC
            ''', (days,))
            return [row[0] for row in cursor.fetchall()]
    
    def cleanup_old_records(self, days: int = 365):
        """清理超过N天的旧记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                DELETE FROM pushed_projects
                WHERE pushed_at < datetime('now', '-' || ? || ' days')
            ''', (days,))
            conn.commit()