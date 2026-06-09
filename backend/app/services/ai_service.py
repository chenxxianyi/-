"""AI service - handles AI reading assistant with mock responses."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.repositories.document_repository import DocumentRepository


class MockAIProvider:
    """Mock AI provider for MVP development."""

    @staticmethod
    def summarize(document_content: str) -> str:
        """Generate a mock summary."""
        words = document_content.split()
        word_count = len(words)
        return (
            f"这是对文档的 AI 摘要（Mock）。文档共约 {word_count} 字。"
            f"\n\n核心内容概述：该文档主要讨论了相关主题的关键概念和方法论。"
            f"文档结构清晰，包含了必要的背景介绍、核心分析和结论部分。"
            f"建议重点阅读开头的概述章节和结尾的总结部分。"
        )

    @staticmethod
    def explain(text: str) -> str:
        """Generate a mock explanation."""
        return (
            f"这是对以下文本的 AI 解释（Mock）：\n\n"
            f"「{text[:100]}{'…' if len(text) > 100 else ''}」\n\n"
            f"解释：这段内容的核心含义是在阐述该领域的一个重要概念。"
            f"它表明在实践中需要关注关键的影响因素，并结合具体场景进行分析。"
            f"建议结合上下文理解其完整含义。"
        )

    @staticmethod
    def translate(text: str, target_language: str = "中文") -> str:
        """Generate a mock translation."""
        return (
            f"[Mock {target_language} Translation]\n\n"
            f"这是对原文的{target_language}翻译。原文内容已按照{target_language}表达习惯进行转换，"
            f"保留了原文的核心信息和逻辑结构。\n\n"
            f"翻译文本：{text[:200]}{'…' if len(text) > 200 else ''}"
        )

    @staticmethod
    def chat(question: str, document_content: str) -> str:
        """Generate a mock chat answer."""
        return (
            f"这是 AI 对您问题的回答（Mock）：\n\n"
            f"问题：{question}\n\n"
            f"回答：根据文档内容分析，这是一个值得深入探讨的问题。"
            f"从文档中可以看到，相关领域的研究表明需要综合考虑多方面因素。"
            f"建议您结合文档中的具体数据和案例进行进一步分析。"
            f"如果您需要更详细的解答，可以提供更多上下文信息。"
        )


class AIService:
    def __init__(self, db: Session):
        self.db = db
        self.doc_repo = DocumentRepository(db)

    def _get_document_content(self, user_id: int, document_id: int) -> str:
        """Get document content with ownership check."""
        doc = self.doc_repo.get_by_id_and_user_id(document_id, user_id)
        if not doc:
            raise NotFoundException("Document not found")
        return doc.parsed_content or ""

    def ask(self, user_id: int, document_id: int, question: str) -> str:
        """Ask a question about a document."""
        content = self._get_document_content(user_id, document_id)
        return MockAIProvider.chat(question, content)

    def summarize(self, user_id: int, document_id: int) -> str:
        """Summarize a document."""
        content = self._get_document_content(user_id, document_id)
        return MockAIProvider.summarize(content)

    def explain(self, user_id: int, document_id: int, text: str) -> str:
        """Explain a selected text."""
        return MockAIProvider.explain(text)

    def translate(self, user_id: int, document_id: int, text: str, target_language: str = "中文") -> str:
        """Translate a selected text."""
        return MockAIProvider.translate(text, target_language)

    def chat(self, user_id: int, document_id: int, message: str) -> str:
        """Chat about a document (same as ask)."""
        return self.ask(user_id, document_id, message)
