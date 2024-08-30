import React, { useMemo } from 'react'
import ReactMarkdown from 'react-markdown'
import 'katex/dist/katex.min.css'
import RemarkMath from 'remark-math'
import RemarkBreaks from 'remark-breaks'
import RehypeKatex from 'rehype-katex'
import RemarkGfm from 'remark-gfm'
import SyntaxHighlighter from 'react-syntax-highlighter'
import { atelierHeathLight } from 'react-syntax-highlighter/dist/esm/styles/hljs'
import ChartComponent from '@/app/components/base/chart'

export function Markdown(props: { content: string }) {
  const components = useMemo(() => ({
    code({ node, inline, className, children, ...props }: any) {
      const match = /language-(\w+)/.exec(className || '')
      if (match && match[1] === 'chart') {
        try {
          //const chartOptions = JSON.parse(String(children).replace(/\n$/, ''))
          //there is risk using eval
          const chartOptions = eval('(' + String(children).replace(/\n$/, '') + ')');
          return <ChartComponent chartOptions={chartOptions} />
        } catch (error) {
          console.log('Error parsing chart options', error)
          return <code>{String(children)}</code>
        }
      }

      return (!inline && match) ? (
        <SyntaxHighlighter
          {...props}
          children={String(children).replace(/\n$/, '')}
          style={atelierHeathLight}
          language={match[1]}
          showLineNumbers
          PreTag="div"
        />
      ) : (
        <code {...props} className={className}>
          {children}
        </code>
      )
    },
  }), [])

  return (
    <div className="markdown-body">
      <ReactMarkdown
        remarkPlugins={[RemarkMath, RemarkGfm, RemarkBreaks]}
        rehypePlugins={[RehypeKatex]}
        components={components}
        linkTarget={'_blank'}
      >
        {props.content}
      </ReactMarkdown>
    </div>
  )
}