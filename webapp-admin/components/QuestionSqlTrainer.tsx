'use client';

import React, { useState, useEffect } from 'react';
import WorkspaceSelector from './WorkspaceSelector';
import { fetchQuestionSqlPairs, buildQuestionSqlPairs, fetchWorkspaces, Workspace } from '../lib/api';
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "@/components/ui/use-toast";
import { Label } from "@/components/ui/label";


interface QuestionSqlPair {
  id?: string;
  question: string;
  sql: string;
}

interface ParseError {
  line: number;
  message: string;
}

const QuestionSqlTrainer: React.FC = () => {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [selectedWorkspace, setSelectedWorkspace] = useState<string>('');
  const [textAreaContent, setTextAreaContent] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    const loadWorkspaces = async () => {
      setIsLoading(true);
      try {
        const fetchedWorkspaces = await fetchWorkspaces();
        setWorkspaces(fetchedWorkspaces);
        if (fetchedWorkspaces.length > 0) {
          setSelectedWorkspace(fetchedWorkspaces[0].id);
        }
      } catch (error) {
        console.error('Error fetching workspaces:', error);
        toast({
          title: "错误",
          description: "获取工作空间列表失败",
          variant: "destructive",
        });
      } finally {
        setIsLoading(false);
      }
    };
    loadWorkspaces();
  }, []);

  useEffect(() => {
    if (selectedWorkspace) {
      fetchQuestionSqlPairsForWorkspace();
    }
  }, [selectedWorkspace]);

  const fetchQuestionSqlPairsForWorkspace = async () => {
    setIsLoading(true);
    try {
      const pairs = await fetchQuestionSqlPairs(selectedWorkspace);
      setTextAreaContent(formatPairsToText(pairs));
    } catch (error) {
      console.error('Error fetching question-sql pairs:', error);
      toast({
        title: "错误",
        description: "获取问题-SQL对失败",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const parsePairsFromText = (text: string): { pairs: QuestionSqlPair[], errors: ParseError[] } => {
    const pairs: QuestionSqlPair[] = [];
    const errors: ParseError[] = [];
    const lines = text.split('\n');
    let currentPair: Partial<QuestionSqlPair> = {};
    let currentField: 'question' | 'sql' | null = null;
    let lineNumber = 0;
  
    for (const line of lines) {
      lineNumber++;
      const trimmedLine = line.trim();
  
      if (trimmedLine === '') {
        if (currentPair.question && currentPair.sql) {
          pairs.push(currentPair as QuestionSqlPair);
          currentPair = {};
          currentField = null;
        }
      } else if (/^question:\s*/i.test(trimmedLine)) {
        if (currentPair.question || currentPair.sql) {
          pairs.push(currentPair as QuestionSqlPair);
          currentPair = {};
        }
        currentField = 'question';
        currentPair.question = line.substring(line.indexOf(':') + 1).trim();
      } else if (/^sql:\s*/i.test(trimmedLine)) {
        if (!currentPair.question) {
          errors.push({ line: lineNumber, message: 'SQL found without a preceding question' });
        }
        currentField = 'sql';
        currentPair.sql = line.substring(line.indexOf(':') + 1).trim();
      } else if (currentField) {
        currentPair[currentField] += '\n' + line;
      } else {
        errors.push({ line: lineNumber, message: 'Invalid format' });
      }
    }
  
    if (currentPair.question && currentPair.sql) {
      pairs.push(currentPair as QuestionSqlPair);
    }
  
    return { pairs, errors };
  };

  const formatPairsToText = (pairs: QuestionSqlPair[]): string => {
    return pairs.map(pair => 
      `Question: ${pair.question.trim()}\nSQL: ${pair.sql.trim()}`
    ).join('\n\n');
  };

  const handleTrain = async () => {
    const { pairs, errors } = parsePairsFromText(textAreaContent);

    if (errors.length > 0) {
      const errorMessage = errors.map(e => `行 ${e.line}: ${e.message}`).join('\n');
      toast({
        title: "格式错误",
        description: `请修正以下错误:\n${errorMessage}`,
        variant: "destructive",
      });
      return;
    }

    if (pairs.length === 0) {
      toast({
        title: "错误",
        description: "没有找到有效的问题-SQL对",
        variant: "destructive",
      });
      return;
    }

    // 验证每个pair
    const invalidPairs = pairs.filter(pair => !pair.question.trim() || !pair.sql.trim());
    if (invalidPairs.length > 0) {
      toast({
        title: "错误",
        description: `发现 ${invalidPairs.length} 个无效的问题-SQL对（问题或SQL为空）`,
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    try {
      const result = await buildQuestionSqlPairs(selectedWorkspace, { question_sql_list: pairs });
      toast({
        title: "成功",
        description: `成功构建 ${result.count} 个问题-SQL对`,
      });
    } catch (error) {
      console.error('Error building question-sql pairs:', error);
      toast({
        title: "错误",
        description: error instanceof Error ? error.message : "构建问题-SQL对失败",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleFinetuning = () => {
    toast({
      title: "提示",
      description: "该功能需要单独定制，请联系我们",
    });
  };

  return (
    <div className="space-y-4">
      <div>
        <p className="text-lg font-bold">选择 workspace</p>
        <WorkspaceSelector
          workspaces={workspaces}
          selectedWorkspace={selectedWorkspace}
          onSelect={setSelectedWorkspace}
        />
      </div>
      
      <div>
        <p className="text-lg font-bold">问题-SQL样本</p>
        <p className="text-sm text-gray-600 mb-2">
          • 每个"问题-SQL"样本之间用空行分隔； 问题以"Question:"开头，SQL内容以"SQL:"开头；都支持跨行
          <br />• 可在SQL内容中包含其他上下文信息，如名词解释，指标口径
        </p>
        <Textarea
          value={textAreaContent}
          onChange={(e) => setTextAreaContent(e.target.value)}
          className="min-h-[400px]"
          placeholder={`示例格式：
Question: How many customers do we have?
SQL: SELECT COUNT(*) FROM customers;

Question: What is the total sales for the year 2023?
SQL: SELECT SUM(sales) FROM transactions WHERE YEAR(date) = 2023;
-- 上下文：sales字段表示每笔交易的销售额
-- transactions表包含所有交易记录，date字段为交易日期
`}
          disabled={isLoading}
        />
      </div>
      <div className="flex space-x-2">
        <Button onClick={handleTrain} disabled={isLoading}>
          训练（RAG）
        </Button>
        <Button onClick={handleFinetuning} variant="outline" disabled={isLoading}>
          训练（fine tuning）
        </Button>
      </div>
    </div>
  );

};

export default QuestionSqlTrainer;