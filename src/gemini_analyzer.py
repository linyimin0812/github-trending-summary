import google.generativeai as genai
from typing import Optional
from config import GEMINI_API_KEY
from github_trending import TrendingProject


class GeminiAnalyzer:
    """使用 Gemini 分析 GitHub 项目"""
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-pro')
    
    def analyze_project(self, project: TrendingProject, 
                       readme_content: Optional[str] = None) -> str:
        """分析项目并生成总结
        
        Args:
            project: TrendingProject 对象
            readme_content: 可选的 README 内容
            
        Returns:
            分析总结文本
        """
        prompt = self._build_prompt(project, readme_content)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error analyzing project with Gemini: {e}")
            return self._generate_fallback_summary(project)
    
    def _build_prompt(self, project: TrendingProject, 
                     readme_content: Optional[str]) -> str:
        """构建分析提示词"""
        prompt = f"""请分析这个 GitHub 热门项目，并提供简洁专业的总结：

项目名称: {project.name}
项目链接: {project.url}
项目描述: {project.description}
编程语言: {project.language}
Stars: {project.stars:,}
今日 Stars: {project.stars_today:,}
"""
        
        if readme_content:
            prompt += f"\n项目 README 摘要:\n{readme_content[:2000]}\n"
        
        prompt += """
请提供以下内容（使用中文，简洁明了）：

1. **功能介绍** (2-3句话概括核心功能)
2. **实现原理** (技术栈和核心实现思路)
3. **架构设计** (主要架构模式和设计亮点)
4. **适用场景** (什么场景下适合使用)
5. **推荐理由** (为什么值得关注)

请以 Markdown 格式输出，每部分简洁有力，总字数控制在 500 字以内。
"""
        return prompt
    
    def _generate_fallback_summary(self, project: TrendingProject) -> str:
        """生成备用总结（API 失败时使用）"""
        return f"""## {project.name}

**项目描述**: {project.description}

**基本信息**:
- 编程语言: {project.language}
- Stars: {project.stars:,}
- 今日 Stars: {project.stars_today:,}
- 项目链接: {project.url}

*注: 详细分析生成失败，请访问项目链接了解更多信息。*
"""
