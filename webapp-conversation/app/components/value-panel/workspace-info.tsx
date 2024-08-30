'use client'

import type { FC } from 'react'
import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/20/solid'

interface WorkspaceInfo {
  supported_dim: string[];
  supported_measurement: string[];
  suggested_questions: string[];
}

const WorkspaceInfoPanel: FC<{
  info: WorkspaceInfo;
}> = ({ info }) => {
  const { t } = useTranslation()
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className=" mt-3 bg-indigo-50 rounded-lg overflow-hidden">
      <button
        className="flex justify-between items-center w-full px-4 py-2 text-sm font-medium text-left text-indigo-900 hover:bg-indigo-100 focus:outline-none focus-visible:ring focus-visible:ring-indigo-500 focus-visible:ring-opacity-75"
        onClick={() => setIsOpen(!isOpen)}
      >
        <span className="flex items-center">
          <svg className="mr-2 h-5 w-5 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {t('app.workspace.info')}
        </span>
        {isOpen ? (
          <ChevronUpIcon className="h-5 w-5 text-indigo-500" />
        ) : (
          <ChevronDownIcon className="h-5 w-5 text-indigo-500" />
        )}
      </button>
      {isOpen && (
        <div className="px-4 pt-4 pb-2 text-sm text-gray-500">
          <div className="space-y-4">
            <InfoSection title={t('app.workspace.dimensions')} items={info.supported_dim} />
            <InfoSection title={t('app.workspace.measurements')} items={info.supported_measurement} />
            <SuggestedQuestions questions={info.suggested_questions} />
          </div>
        </div>
      )}
    </div>
  )
}

const InfoSection: FC<{ title: string; items: string[] }> = ({ title, items }) => (
  <div>
    <h3 className="font-medium text-gray-900">{title}</h3>
    <div className="mt-2 flex flex-wrap gap-2">
      {items.map(item => (
        <span key={item} className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs">
          {item}
        </span>
      ))}
    </div>
  </div>
)

const SuggestedQuestions: FC<{ questions: string[] }> = ({ questions }) => {
  const { t } = useTranslation()
  return (
    <div>
      <h3 className="font-medium text-gray-900">{t('app.workspace.suggestedQuestions')}</h3>
      <div className="mt-2 flex flex-wrap gap-2">
        {questions.map((question, index) => (
          <span key={index} className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs cursor-pointer hover:bg-indigo-200">
            {question}
          </span>
        ))}
      </div>
    </div>
  )
}

export default React.memo(WorkspaceInfoPanel)