import React from 'react';

type MetricsAndDimensionsProps = {
  metrics: any
};

const MetricsAndDimensions: React.FC<MetricsAndDimensionsProps> = ({ metrics }) => {
  return (
    <div className="bg-yellow-100 p-4 rounded-lg">
      <h2 className="text-xl font-bold mb-2">Workspace Metadata</h2>
      <pre className="whitespace-pre-wrap break-words">
        {JSON.stringify(metrics, null, 2)}
      </pre>
    </div>
  );
};

export default MetricsAndDimensions;