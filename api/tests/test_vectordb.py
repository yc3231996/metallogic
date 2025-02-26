import unittest
from db.vectordb import WeaviateDB, QuestionSql, TermDesc

class TestWeaviateDB(unittest.TestCase):
    def setUp(self):
        self.question_sql_db = WeaviateDB(QuestionSql, workspace="testproject")
        self.term_desc_db = WeaviateDB(TermDesc, workspace="testproject")

    # def test_del(self):
    #     self.question_sql_db.delete_all()

    # def test_batch_insert(self):
    #     batch_questions = [
    #         QuestionSql(question="How many customers do we have?", sql="SELECT COUNT(*) FROM customers;"),
    #         QuestionSql(question="What's our best-selling product?", sql="SELECT product_name, SUM(quantity) as total_sold FROM sales GROUP BY product_name ORDER BY total_sold DESC LIMIT 1;")
    #     ]
    #     self.question_sql_db.batch_insert(batch_questions)
    #     all_questions = self.question_sql_db.get_all()
    #     self.assertGreaterEqual(len(all_questions), 2)

    # def test_search_similar(self):
    #     similar_questions = self.question_sql_db.search_similar("What are our total sales?", limit=2)
    #     self.assertEqual(len(similar_questions), 2)


    def test_all(self):
        # 测试插入单条记录
        new_question_sql = QuestionSql(
            question="What is the total sales for the year 2023?",
            sql="SELECT SUM(sales) FROM transactions WHERE YEAR(date) = 2023;"
        )
        self.question_sql_db.insert(new_question_sql)
        print(f"Inserted a new QuestionSql record with id: {new_question_sql.id}")

        new_term_desc = TermDesc(
            term="SQL",
            desc="Structured Query Language, a domain-specific language used for managing and querying relational databases."
        )
        self.term_desc_db.insert(new_term_desc)
        print(f"Inserted a new TermDesc record with id: {new_term_desc.id}")

        # 测试批量插入
        batch_questions = [
            QuestionSql(question="How many customers do we have?", sql="SELECT COUNT(*) FROM customers;"),
            QuestionSql(question="What's our best-selling product?", sql="SELECT product_name, SUM(quantity) as total_sold FROM sales GROUP BY product_name ORDER BY total_sold DESC LIMIT 1;")
        ]
        self.question_sql_db.batch_insert(batch_questions)
        print("Batch inserted QuestionSql records")

        # 测试查询所有记录
        all_questions = self.question_sql_db.get_all()
        print(f"Total QuestionSql records: {len(all_questions)}")

        # 测试相似性搜索
        similar_questions = self.question_sql_db.search_similar("What are our total sales?", limit=2)
        print("Similar questions found:")
        for q in similar_questions:
            print(f"- Question: {q.question}")
            print(f"  SQL: {q.sql}")
            print(f"  ID: {q.id}")

        # 测试精确匹配搜索
        exact_terms = self.term_desc_db.search_exact("term", "SQL")
        if exact_terms:
            print(f"Found exact match for 'SQL': {exact_terms[0].desc}")
            print(f"ID: {exact_terms[0].id}")

        # 测试更新记录
        if exact_terms:
            updated_term = exact_terms[0]
            updated_term.desc += " It is widely used in database management and data analysis."
            self.term_desc_db.update(updated_term)
            print(f"Updated TermDesc record for 'SQL' with ID: {updated_term.id}")

        # 测试删除记录
        if all_questions:
            question_to_delete = all_questions[0]
            self.question_sql_db.delete(question_to_delete)
            print(f"Deleted QuestionSql record with ID: {question_to_delete.id}")

        # 测试重建集合
        new_terms = [
            TermDesc(term="Database", desc="An organized collection of structured information or data."),
            TermDesc(term="Query", desc="A request for data or information from a database.")
        ]
        self.term_desc_db.rebuild_collection(new_terms)
        print("Rebuilt TermDesc collection")

        # 最后，获取并打印所有记录以验证操作
        final_questions = self.question_sql_db.get_all()
        final_terms = self.term_desc_db.get_all()
        print(f"Final QuestionSql count: {len(final_questions)}")
        print(f"Final TermDesc count: {len(final_terms)}")


if __name__ == '__main__':
    unittest.main()