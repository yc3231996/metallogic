# SQL COT
query: 帮我查询ROI最高的几条广告
thinking:
1. 需要查询ROI最高的广告信息，可以理解为从明细表Yingkou_ADS.tt_ad_report_day中，按照广告ID(ad_id)为粒度进行ROI计算和排名。
2. ROI的计算规则为：ROI=GMV/消耗，即ROI = total_onsite_shopping_value / spend。
3. 只筛选消耗(spend)>0的数据，避免分母为零。
4. 取ROI最高的前几条，默认给出TOP 10，如果需要具体条数可以补充说明。
5. 为结果展示广告ID、产品名、消耗、GMV、ROI等关键信息。





# Planning COT

