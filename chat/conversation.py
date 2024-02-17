#!/usr/bin/env python3
"""
Inialize the langchain with OPENAI
"""
from __future__ import annotations
from typing import Any

from dataclasses import dataclass

from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain.prompts import PromptTemplate


@dataclass
class LangChain:
    chunk_size: int = 450
    chunk_overlap: int = 50
    text_contents: str = "documents/test.json"
    embedding = OpenAIEmbeddings()

    def pdf_load(self) -> list:
        """
        This method loads the PDF and extracts every word and pastes it into
        documents, which is list.
        """
        loader = JSONLoader(
            file_path=self.text_contents,
            text_content=False,
            jq_schema=".message[]"
        )
        docs = loader.load()
        return docs

    def splitter(self) -> str:
        """
        This method splits every text with 'RecursionCharacterTextSplitter'.
        With the `chunk_size` and `chunk_overlap` parameters.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap
        )
        docs = self.pdf_load()
        doc_splits = text_splitter.split_documents(docs)
        return doc_splits

    def embedding_and_vectorstores(self) -> str:
        """
        This method embeds splitter data and stores it into vector stores.
        Search the context with the nearest vectors.
        """
        vectordb = FAISS.from_documents(
            self.splitter(),
            self.embedding
        )
        return vectordb


@dataclass
class ConversationalChain(LangChain):

    llm_name: str = "gpt-3.5-turbo-0301"
    temperature: float = 0.5
    llm = ChatOpenAI(
        model_name=llm_name,
        temperature=temperature,
    )

    @staticmethod
    def chat_history(user_id):
        """
        This method connects MongoDB to the collection of previous chat history records.
        """
        connection_string = "sqlite:///sqlite.db"

        chat_history = SQLChatMessageHistory(
            connection_string=connection_string,
            session_id=user_id
        )
        return chat_history

    def conversation_retrieval_chain(self):
        """
        This method configure with GPT with prevision message and vectoresdatabase.
        """
        vectordb = LangChain.embedding_and_vectorstores(self)
        # Retriever Database
        retriever = vectordb.as_retriever()

        general_system_template = """You will always receive contexts first. Initially, attempt to generate a response 
        using the provided context. If the context does not yield the answer, try to generate a response independently.
        {context}
        Question: {question}
        Helpful Answer: """

        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=general_system_template
        )

        conversation = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            max_tokens_limit=1300,
            chain_type="stuff",
            get_chat_history=lambda h: h,
            verbose=True,
            combine_docs_chain_kwargs={'prompt': QA_CHAIN_PROMPT}
        )
        return conversation

    def chat_conversation(
            self,
            query: str, 
            user_id: Any, 
            conversat: Any, 
            chat_history_count: int
    ) -> str:
        """
        This method conversation with LLM and return response as per the question.
        """
        chat_history = self.chat_history(user_id=user_id)

        # A single user can only use previous three commits.
        # After calling previous three commits are removed from database and new commits are added.
        if len(chat_history.messages) >= 2*chat_history_count:
            chat_history.clear()

        # GPT Conversation
        result = conversat({
            "question": query,
            "chat_history": chat_history.messages
        })
        answer = result["answer"]

        # Save Histoy
        chat_history.add_user_message(query)
        chat_history.add_ai_message(answer)

        return answer
