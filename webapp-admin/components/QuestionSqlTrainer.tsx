'use client';

import React, { useState, useEffect } from 'react';
import WorkspaceSelector from './WorkspaceSelector';
import { fetchQuestionSqlPairs, buildQuestionSqlPairs, fetchWorkspaces, Workspace } from '../lib/api';
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "@/components/ui/use-toast";

interface QuestionSqlPair {
  id?: string;
  question: string;
  sql: string;
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

  const formatPairsToText = (pairs: QuestionSqlPair[]): string => {
    return pairs.map(pair => `question: ${pair.question}\nsql: ${pair.sql}`).join('\n\n');
  };

  const parsePairsFromText = (text: string): QuestionSqlPair[] => {
    const pairs: QuestionSqlPair[] = [];
    const lines = text.split('\n');
    let currentPair: Partial<QuestionSqlPair> = {};

    for (const line of lines) {
      if (line.startsWith('question:')) {
        if (currentPair.question) {
          pairs.push(currentPair as QuestionSqlPair);
          currentPair = {};
        }
        currentPair.question = line.substring('question:'.length).trim();
      } else if (line.startsWith('sql:')) {
        currentPair.sql = line.substring('sql:'.length).trim();
      }
    }

    if (currentPair.question && currentPair.sql) {
      pairs.push(currentPair as QuestionSqlPair);
    }

    return pairs;
  };

  const handleTrain = async () => {
    const pairs = parsePairsFromText(textAreaContent);
    if (pairs.length === 0) {
      toast({
        title: "错误",
        description: "无效的输入格式",
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
        description: "构建问题-SQL对失败",
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
      <WorkspaceSelector
        workspaces={workspaces}
        selectedWorkspace={selectedWorkspace}
        onSelect={setSelectedWorkspace}
      />
      <Textarea
        value={textAreaContent}
        onChange={(e) => setTextAreaContent(e.target.value)}
        className="min-h-[400px]"
        placeholder={`请输入问题-SQL对，并遵循下面格式（question sql对之间用空行隔开）：
question: How many customers do we have?
sql: SELECT COUNT(*) FROM customers;

question: What is the total sales for the year 2023?
sql: SELECT SUM(sales) FROM transactions WHERE YEAR(date) = 2023;
        `}
        disabled={isLoading}
      />
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