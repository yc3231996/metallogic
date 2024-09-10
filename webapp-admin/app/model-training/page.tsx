'use client';

import React from 'react';
import QuestionSqlTrainer from '@/components/QuestionSqlTrainer';

export default function ModelTrainingPage() {
  return (
    <main className="flex min-h-screen p-8 bg-gray-100">
      <div className="w-full max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">模型训练</h1>
        <QuestionSqlTrainer />
      </div>
    </main>
  );
}