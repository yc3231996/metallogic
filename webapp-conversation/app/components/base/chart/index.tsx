import React, { useEffect, useRef, useState } from 'react';
import EChartsReact from 'echarts-for-react';

interface ChartComponentProps {
  chartOptions: any;
}

const ChartComponent: React.FC<ChartComponentProps> = ({ chartOptions }) => {
  const chartRef = useRef<EChartsReact>(null);
  const prevOptionsRef = useRef<any>(null);
  const [chartHeight, setChartHeight] = useState<string>('400px');

  useEffect(() => {
    try{
      if (chartRef.current && chartOptions) {
        const chart = chartRef.current.getEchartsInstance();
        if (JSON.stringify(chartOptions) !== JSON.stringify(prevOptionsRef.current)) {
          chart.setOption(chartOptions, true);
          prevOptionsRef.current = chartOptions;
        }
      }
  
      //incase no sufficient data to render chart, set height to 0px
      if (!chartOptions || !chartOptions.series || !chartOptions.series.length) {
        setChartHeight('0px');
      } else {
        setChartHeight('400px');
      }
    }
    catch(err){
      console.error(err);
    }
  }, [chartOptions]);

  return (
    <div className="chart-container">
      <EChartsReact
        ref={chartRef}
        option={chartOptions}
        style={{ height: chartHeight, width: '100%' }}
        opts={{ renderer: 'canvas' }}
        notMerge={true}
        lazyUpdate={true}
      />
    </div>
  );
};

export default React.memo(ChartComponent);