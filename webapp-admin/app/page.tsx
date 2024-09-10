import React from 'react';

const HomePage = () => {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">欢迎来到观心万象-Admin</h1>
      <p>在Workspace建模区域，您可以用自然语言描述表和字段含义，让大模型理解您的数据资产</p>
      <p>在模型训练区域，您可以通过提供“问题-SQL”，以及专业数据知识，来强化模型能力，如需对模型进行定制化fine tuning请联系我们</p>
    </div>
  );
};

export default HomePage;