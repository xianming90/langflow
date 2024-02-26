from typing import Optional

from langchain.chains import create_sql_query_chain
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.prompts import PromptTemplate

from langflow import CustomComponent
from langflow.field_typing import BaseLanguageModel, Text


class SQLGeneratorComponent(CustomComponent):
    display_name = "Natural Language to SQL"
    description = "Generate SQL from natural language."

    def build_config(self):
        return {
            "db": {"display_name": "Database"},
            "llm": {"display_name": "LLM"},
            "prompt": {
                "display_name": "Prompt",
                "info": "The prompt must contain `{question}`.",
            },
            "top_k": {
                "display_name": "Top K",
                "info": "The number of results per select statement to return. If 0, no limit.",
            },
        }

    def build(
        self,
        inputs: Text,
        db: SQLDatabase,
        llm: BaseLanguageModel,
        top_k: int = 5,
        prompt: Optional[PromptTemplate] = None,
    ) -> Text:
        if top_k > 0:
            kwargs = {
                "k": top_k,
            }
        if not prompt:
            sql_query_chain = create_sql_query_chain(llm=llm, db=db, **kwargs)
        else:
            template = prompt.template if hasattr(prompt, "template") else prompt
            # Check if {question} is in the prompt
            if "{question}" not in template or "question" not in template.input_variables:
                raise ValueError("Prompt must contain `{question}` to be used with Natural Language to SQL.")
            sql_query_chain = create_sql_query_chain(llm=llm, db=db, prompt=prompt, **kwargs)
        query_writer = sql_query_chain | {"query": lambda x: x.replace("SQLQuery:", "").strip()}
        response = query_writer.invoke({"question": inputs})
        query = response.get("query")
        self.status = query
        return query