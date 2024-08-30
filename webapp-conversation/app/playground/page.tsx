'use client'
import React, { useState, useEffect, useMemo } from 'react';
import ReactMarkdown from 'react-markdown';

// 模拟 ECharts 组件
const ECharts: React.FC<{ option: any }> = ({ option }) => {
  console.log('ECharts rendering with option:', option);
  return <div>ECharts Component (模拟)</div>;
};

// 优化的图表组件
const ChartComponent: React.FC<{ content: string }> = React.memo(({ content }) => {
  const option = useMemo(() => {
    console.log('Parsing chart content');
    // 这里应该是实际的解析逻辑
    return JSON.parse(content);
  }, [content]);

  return <ECharts option={option} />;
});

// 自定义的代码块渲染组件
const CodeBlock: React.FC<{
  node?: any;
  inline?: boolean;
  className?: string;
  children: React.ReactNode;
}> = ({ inline, className, children }) => {
  if (inline) {
    return <code className={className}>{children}</code>;
  }

  if (className === 'language-chart') {
    return <ChartComponent content={children.toString()} />;
  }

  return <pre className={className}><code>{children}</code></pre>;
};

// 主应用组件
const App: React.FC = () => {
  const [markdown, setMarkdown] = useState('');

  // 模拟流式输出
  useEffect(() => {
    const content = [
      '# Streaming Markdown Example\n\n',
      'This is a paragraph.\n\n',
      '```chart\n{"type":"bar","data":{"labels":["A","B","C"],"datasets":[{"data":[1,2,3]}]}}\n```\n\n',
      'Another paragraph.\n\n',
      '```chart\n{"type":"line","data":{"labels":["X","Y","Z"],"datasets":[{"data":[4,5,6]}]}}\n```\n\n',
      'Final paragraph.',
      'Final paragraph.',
      'Final paragraph.',
      'Final paragraph.',
      'Final paragraph.'
    ];

    let index = 0;
    const interval = setInterval(() => {
      if (index < content.length) {
        setMarkdown(prev => prev + content[index]);
        index++;
      } else {
        clearInterval(interval);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>Streaming Markdown with Optimized Chart Rendering</h1>
      <ReactMarkdown components={{ code: CodeBlock }}>{markdown}</ReactMarkdown>
    </div>
  );
};

export default App;