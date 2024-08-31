-- 创建表结构
CREATE TABLE ad_campaign_performance (
    campaign_id VARCHAR(50) PRIMARY KEY,
    platform VARCHAR(50),
    campaign_name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    budget DECIMAL(10,2),
    total_spend DECIMAL(10,2),
    impressions INTEGER,
    clicks INTEGER,
    conversions INTEGER,
    revenue DECIMAL(10,2),
    ctr DECIMAL(5,4),
    cpc DECIMAL(5,2),
    cpa DECIMAL(7,2),
    roas DECIMAL(5,2),
    target_audience VARCHAR(100),
    creative_id VARCHAR(50),
    influencer_id VARCHAR(50)
);
COMMENT ON TABLE ad_campaign_performance IS '广告活动性能表。记录每个广告活动的详细表现数据。';
COMMENT ON COLUMN ad_campaign_performance.campaign_id IS '广告活动唯一标识符，主键';
COMMENT ON COLUMN ad_campaign_performance.platform IS '广告投放平台名称';
COMMENT ON COLUMN ad_campaign_performance.campaign_name IS '广告活动名称';
COMMENT ON COLUMN ad_campaign_performance.start_date IS '广告活动开始日期';
COMMENT ON COLUMN ad_campaign_performance.end_date IS '广告活动结束日期';
COMMENT ON COLUMN ad_campaign_performance.budget IS '广告活动预算';
COMMENT ON COLUMN ad_campaign_performance.total_spend IS '广告活动实际支出';
COMMENT ON COLUMN ad_campaign_performance.impressions IS '广告展示次数';
COMMENT ON COLUMN ad_campaign_performance.clicks IS '广告点击次数';
COMMENT ON COLUMN ad_campaign_performance.conversions IS '广告转化次数';
COMMENT ON COLUMN ad_campaign_performance.revenue IS '广告活动产生的收入';
COMMENT ON COLUMN ad_campaign_performance.ctr IS '点击率（Click-Through Rate）';
COMMENT ON COLUMN ad_campaign_performance.cpc IS '每次点击成本（Cost Per Click）';
COMMENT ON COLUMN ad_campaign_performance.cpa IS '每次获客成本（Cost Per Acquisition）';
COMMENT ON COLUMN ad_campaign_performance.roas IS '广告支出回报率（Return On Ad Spend）';
COMMENT ON COLUMN ad_campaign_performance.target_audience IS '目标受众描述';
COMMENT ON COLUMN ad_campaign_performance.creative_id IS '关联的创意素材ID';
COMMENT ON COLUMN ad_campaign_performance.influencer_id IS '关联的影响者ID';


CREATE TABLE ad_creative_performance (
    creative_id VARCHAR(50) PRIMARY KEY,
    creative_type VARCHAR(50),
    creative_url VARCHAR(200),
    impressions INTEGER,
    clicks INTEGER,
    conversions INTEGER,
    engagement_rate DECIMAL(5,4),
    ctr DECIMAL(5,4),
    conversion_rate DECIMAL(5,4),
    performance_score DECIMAL(5,2)
);
COMMENT ON TABLE ad_creative_performance IS '广告创意素材性能表。记录每个创意素材的表现数据。';
COMMENT ON COLUMN ad_creative_performance.creative_id IS '创意素材唯一标识符，主键';
COMMENT ON COLUMN ad_creative_performance.creative_type IS '创意素材类型（如图片、视频等）';
COMMENT ON COLUMN ad_creative_performance.creative_url IS '创意素材的URL链接';
COMMENT ON COLUMN ad_creative_performance.impressions IS '创意素材展示次数';
COMMENT ON COLUMN ad_creative_performance.clicks IS '创意素材点击次数';
COMMENT ON COLUMN ad_creative_performance.conversions IS '创意素材带来的转化次数';
COMMENT ON COLUMN ad_creative_performance.engagement_rate IS '互动率';
COMMENT ON COLUMN ad_creative_performance.ctr IS '点击率（Click-Through Rate）';
COMMENT ON COLUMN ad_creative_performance.conversion_rate IS '转化率';
COMMENT ON COLUMN ad_creative_performance.performance_score IS '综合表现评分';


CREATE TABLE influencer_performance (
    influencer_id VARCHAR(50) PRIMARY KEY,
    influencer_name VARCHAR(100),
    platform VARCHAR(50),
    followers INTEGER,
    engagement_rate DECIMAL(5,4),
    total_campaigns INTEGER,
    total_revenue_generated DECIMAL(10,2),
    average_roas DECIMAL(5,2),
    performance_score DECIMAL(5,2)
);
COMMENT ON TABLE influencer_performance IS '影响者表现表。记录每个影响者的整体表现数据。';
COMMENT ON COLUMN influencer_performance.influencer_id IS '影响者唯一标识符，主键';
COMMENT ON COLUMN influencer_performance.influencer_name IS '影响者名称';
COMMENT ON COLUMN influencer_performance.platform IS '影响者主要活动的平台';
COMMENT ON COLUMN influencer_performance.followers IS '影响者的粉丝数量';
COMMENT ON COLUMN influencer_performance.engagement_rate IS '影响者的平均互动率';
COMMENT ON COLUMN influencer_performance.total_campaigns IS '影响者参与的广告活动总数';
COMMENT ON COLUMN influencer_performance.total_revenue_generated IS '影响者产生的总收入';
COMMENT ON COLUMN influencer_performance.average_roas IS '影响者的平均广告支出回报率';
COMMENT ON COLUMN influencer_performance.performance_score IS '影响者的综合表现评分';


CREATE TABLE pre_campaign_estimation (
    estimation_id VARCHAR(50) PRIMARY KEY,
    campaign_id VARCHAR(50),
    estimated_impressions INTEGER,
    estimated_clicks INTEGER,
    estimated_conversions INTEGER,
    estimated_revenue DECIMAL(10,2),
    estimated_roas DECIMAL(5,2),
    actual_impressions INTEGER,
    actual_clicks INTEGER,
    actual_conversions INTEGER,
    actual_revenue DECIMAL(10,2),
    actual_roas DECIMAL(5,2),
    estimation_accuracy DECIMAL(5,4)
);
COMMENT ON TABLE pre_campaign_estimation IS '广告活动预估表。记录每个广告活动的预估数据和实际结果。';
COMMENT ON COLUMN pre_campaign_estimation.estimation_id IS '预估记录唯一标识符，主键';
COMMENT ON COLUMN pre_campaign_estimation.campaign_id IS '关联的广告活动ID';
COMMENT ON COLUMN pre_campaign_estimation.estimated_impressions IS '预估展示次数';
COMMENT ON COLUMN pre_campaign_estimation.estimated_clicks IS '预估点击次数';
COMMENT ON COLUMN pre_campaign_estimation.estimated_conversions IS '预估转化次数';
COMMENT ON COLUMN pre_campaign_estimation.estimated_revenue IS '预估收入';
COMMENT ON COLUMN pre_campaign_estimation.estimated_roas IS '预估广告支出回报率';
COMMENT ON COLUMN pre_campaign_estimation.actual_impressions IS '实际展示次数';
COMMENT ON COLUMN pre_campaign_estimation.actual_clicks IS '实际点击次数';
COMMENT ON COLUMN pre_campaign_estimation.actual_conversions IS '实际转化次数';
COMMENT ON COLUMN pre_campaign_estimation.actual_revenue IS '实际收入';
COMMENT ON COLUMN pre_campaign_estimation.actual_roas IS '实际广告支出回报率';
COMMENT ON COLUMN pre_campaign_estimation.estimation_accuracy IS '预估准确度';


CREATE TABLE dim_platform (
    platform_id VARCHAR(50) PRIMARY KEY,
    platform_name VARCHAR(50),
    api_endpoint VARCHAR(200),
    rate_limits JSON,
    supported_ad_formats JSON
);
COMMENT ON TABLE dim_platform IS '平台维度表。存储各广告平台的详细信息。';
COMMENT ON COLUMN dim_platform.platform_id IS '平台唯一标识符，主键';
COMMENT ON COLUMN dim_platform.platform_name IS '平台名称';
COMMENT ON COLUMN dim_platform.api_endpoint IS '平台API端点URL';
COMMENT ON COLUMN dim_platform.rate_limits IS 'API速率限制信息（JSON格式）';
COMMENT ON COLUMN dim_platform.supported_ad_formats IS '支持的广告格式（JSON格式）';



-------------插入数据-----------------
--4个广告平台（Facebook、TikTok、Instagram 和 YouTube）
--每个平台3个广告活动，总共12个活动
--12个对应的创意素材
--5个影响者
--每个广告活动的预估和实际性能数据
--这些数据涵盖了2024年6月1日到8月9日的时间范围
----------------------------------------

-- 清空现有数据
TRUNCATE TABLE ad_campaign_performance;
TRUNCATE TABLE ad_creative_performance;
TRUNCATE TABLE influencer_performance;
TRUNCATE TABLE pre_campaign_estimation;
TRUNCATE TABLE dim_platform;

-- 插入平台数据
INSERT INTO dim_platform (platform_id, platform_name, api_endpoint, rate_limits, supported_ad_formats)
VALUES
('FB001', 'Facebook', 'https://api.facebook.com', '{"requests_per_hour": 1000, "requests_per_day": 20000}', '["image", "video", "carousel"]'),
('TT001', 'TikTok', 'https://api.tiktok.com', '{"requests_per_hour": 500, "requests_per_day": 10000}', '["video", "topview"]'),
('IG001', 'Instagram', 'https://api.instagram.com', '{"requests_per_hour": 800, "requests_per_day": 15000}', '["image", "story", "reels"]'),
('YT001', 'YouTube', 'https://api.youtube.com', '{"requests_per_hour": 600, "requests_per_day": 12000}', '["video", "masthead"]');

-- 插入影响者数据
INSERT INTO influencer_performance (influencer_id, influencer_name, platform, followers, engagement_rate, total_campaigns, total_revenue_generated, average_roas, performance_score)
VALUES
('INF001', 'TechGuru', 'Facebook', 500000, 0.0350, 15, 75000.00, 2.8, 8.7),
('INF002', 'FashionIcon', 'Instagram', 1000000, 0.0450, 20, 100000.00, 3.2, 9.1),
('INF003', 'GamingPro', 'TikTok', 2000000, 0.0550, 12, 150000.00, 3.7, 9.5),
('INF004', 'FitnessFanatic', 'YouTube', 750000, 0.0400, 10, 80000.00, 3.0, 8.9),
('INF005', 'FoodieExplorer', 'Instagram', 300000, 0.0600, 8, 40000.00, 2.5, 8.3);

-- 生成更多的广告活动数据
INSERT INTO ad_campaign_performance (campaign_id, platform, campaign_name, start_date, end_date, budget, total_spend, impressions, clicks, conversions, revenue, ctr, cpc, cpa, roas, target_audience, creative_id, influencer_id)
VALUES
-- Facebook Campaigns
('FB_CAMP_001', 'Facebook', 'Summer Tech Sale', '2024-06-01', '2024-06-15', 5000.00, 4800.00, 500000, 25000, 1000, 15000.00, 0.0500, 0.19, 4.80, 3.13, 'Age 25-40, Tech Enthusiasts', 'FB_CREA_001', 'INF001'),
('FB_CAMP_002', 'Facebook', 'Back to School', '2024-07-15', '2024-07-31', 6000.00, 5900.00, 600000, 30000, 1200, 18000.00, 0.0500, 0.20, 4.92, 3.05, 'Parents, Age 30-50', 'FB_CREA_002', NULL),
('FB_CAMP_003', 'Facebook', 'Fitness Challenge', '2024-08-01', '2024-08-15', 4500.00, 4400.00, 450000, 22500, 900, 13500.00, 0.0500, 0.20, 4.89, 3.07, 'Fitness Enthusiasts, Age 20-40', 'FB_CREA_003', 'INF004'),

-- TikTok Campaigns
('TT_CAMP_001', 'TikTok', 'Dance Challenge', '2024-06-15', '2024-06-30', 8000.00, 7800.00, 1000000, 50000, 2000, 30000.00, 0.0500, 0.16, 3.90, 3.85, 'Age 16-25, Music Lovers', 'TT_CREA_001', 'INF003'),
('TT_CAMP_002', 'TikTok', 'Food Recipe Series', '2024-07-01', '2024-07-15', 7000.00, 6800.00, 900000, 45000, 1800, 27000.00, 0.0500, 0.15, 3.78, 3.97, 'Food Enthusiasts, Age 18-35', 'TT_CREA_002', 'INF005'),
('TT_CAMP_003', 'TikTok', 'Gaming Tournament', '2024-08-01', '2024-08-15', 9000.00, 8800.00, 1100000, 55000, 2200, 33000.00, 0.0500, 0.16, 4.00, 3.75, 'Gamers, Age 18-30', 'TT_CREA_003', 'INF003'),

-- Instagram Campaigns
('IG_CAMP_001', 'Instagram', 'Summer Fashion Collection', '2024-06-01', '2024-06-15', 6000.00, 5800.00, 750000, 37500, 1500, 22500.00, 0.0500, 0.15, 3.87, 3.88, 'Fashion Enthusiasts, Age 18-35', 'IG_CREA_001', 'INF002'),
('IG_CAMP_002', 'Instagram', 'Travel Inspiration', '2024-07-15', '2024-07-31', 5500.00, 5300.00, 700000, 35000, 1400, 21000.00, 0.0500, 0.15, 3.79, 3.96, 'Travel Lovers, Age 25-45', 'IG_CREA_002', NULL),
('IG_CAMP_003', 'Instagram', 'Wellness Week', '2024-08-01', '2024-08-15', 5000.00, 4900.00, 650000, 32500, 1300, 19500.00, 0.0500, 0.15, 3.77, 3.98, 'Health Conscious, Age 25-50', 'IG_CREA_003', 'INF004'),

-- YouTube Campaigns
('YT_CAMP_001', 'YouTube', 'Tech Review Series', '2024-06-15', '2024-06-30', 7000.00, 6800.00, 800000, 40000, 1600, 24000.00, 0.0500, 0.17, 4.25, 3.53, 'Tech Enthusiasts, Age 20-45', 'YT_CREA_001', 'INF001'),
('YT_CAMP_002', 'YouTube', 'Cooking Masterclass', '2024-07-01', '2024-07-15', 6500.00, 6300.00, 750000, 37500, 1500, 22500.00, 0.0500, 0.17, 4.20, 3.57, 'Cooking Enthusiasts, Age 25-55', 'YT_CREA_002', 'INF005'),
('YT_CAMP_003', 'YouTube', 'Fitness Transformation', '2024-08-01', '2024-08-15', 7500.00, 7300.00, 850000, 42500, 1700, 25500.00, 0.0500, 0.17, 4.29, 3.49, 'Fitness Enthusiasts, Age 20-40', 'YT_CREA_003', 'INF004');

-- 生成更多的创意素材数据
INSERT INTO ad_creative_performance (creative_id, creative_type, creative_url, impressions, clicks, conversions, engagement_rate, ctr, conversion_rate, performance_score)
VALUES
-- Facebook Creatives
('FB_CREA_001', 'Image', 'https://example.com/fb_image_001.jpg', 500000, 25000, 1000, 0.0600, 0.0500, 0.0400, 8.5),
('FB_CREA_002', 'Carousel', 'https://example.com/fb_carousel_002', 600000, 30000, 1200, 0.0650, 0.0500, 0.0400, 8.7),
('FB_CREA_003', 'Video', 'https://example.com/fb_video_003.mp4', 450000, 22500, 900, 0.0700, 0.0500, 0.0400, 8.9),

-- TikTok Creatives
('TT_CREA_001', 'Video', 'https://example.com/tt_video_001.mp4', 1000000, 50000, 2000, 0.0800, 0.0500, 0.0400, 9.2),
('TT_CREA_002', 'TopView', 'https://example.com/tt_topview_002', 900000, 45000, 1800, 0.0750, 0.0500, 0.0400, 9.0),
('TT_CREA_003', 'Video', 'https://example.com/tt_video_003.mp4', 1100000, 55000, 2200, 0.0820, 0.0500, 0.0400, 9.3),

-- Instagram Creatives
('IG_CREA_001', 'Image', 'https://example.com/ig_image_001.jpg', 750000, 37500, 1500, 0.0680, 0.0500, 0.0400, 8.8),
('IG_CREA_002', 'Story', 'https://example.com/ig_story_002', 700000, 35000, 1400, 0.0700, 0.0500, 0.0400, 8.9),
('IG_CREA_003', 'Reels', 'https://example.com/ig_reels_003', 650000, 32500, 1300, 0.0720, 0.0500, 0.0400, 9.0),

-- YouTube Creatives
('YT_CREA_001', 'Video', 'https://example.com/yt_video_001.mp4', 800000, 40000, 1600, 0.0650, 0.0500, 0.0400, 8.7),
('YT_CREA_002', 'Video', 'https://example.com/yt_video_002.mp4', 750000, 37500, 1500, 0.0670, 0.0500, 0.0400, 8.8),
('YT_CREA_003', 'Masthead', 'https://example.com/yt_masthead_003', 850000, 42500, 1700, 0.0700, 0.0500, 0.0400, 9.1);

-- 生成更多的预估数据
INSERT INTO pre_campaign_estimation (estimation_id, campaign_id, estimated_impressions, estimated_clicks, estimated_conversions, estimated_revenue, estimated_roas, actual_impressions, actual_clicks, actual_conversions, actual_revenue, actual_roas, estimation_accuracy)
VALUES
-- Facebook Estimations
('EST_FB_001', 'FB_CAMP_001', 480000, 24000, 960, 14400.00, 3.00, 500000, 25000, 1000, 15000.00, 3.13, 0.9600),
('EST_FB_002', 'FB_CAMP_002', 580000, 29000, 1160, 17400.00, 2.95, 600000, 30000, 1200, 18000.00, 3.05, 0.9667),
('EST_FB_003', 'FB_CAMP_003', 430000, 21500, 860, 12900.00, 2.93, 450000, 22500, 900, 13500.00, 3.07, 0.9556),

-- TikTok Estimations
('EST_TT_001', 'TT_CAMP_001', 950000, 47500, 1900, 28500.00, 3.65, 1000000, 50000, 2000, 30000.00, 3.85, 0.9500),
('EST_TT_002', 'TT_CAMP_002', 870000, 43500, 1740, 26100.00, 3.84, 900000, 45000, 1800, 27000.00, 3.97, 0.9667),
('EST_TT_003', 'TT_CAMP_003', 1050000, 52500, 2100, 31500.00, 3.58, 1100000, 55000, 2200, 33000.00, 3.75, 0.9545),

-- Instagram Estimations
('EST_IG_001', 'IG_CAMP_001', 720000, 36000, 1440, 21600.00, 3.72, 750000, 37500, 1500, 22500.00, 3.88, 0.9600),
('EST_IG_002', 'IG_CAMP_002', 680000, 34000, 1360, 20400.00, 3.85, 700000, 35000, 1400, 21000.00, 3.96, 0.9714),
('EST_IG_003', 'IG_CAMP_003', 630000, 31500, 1260, 18900.00, 3.86, 650000, 32500, 1300, 19500.00, 3.98, 0.9692),

-- YouTube Estimations
('EST_YT_001', 'YT_CAMP_001', 770000, 38500, 1540, 23100.00, 3.40, 800000, 40000, 1600, 24000.00, 3.53, 0.9625),
('EST_YT_002', 'YT_CAMP_002', 720000, 36000, 1440, 21600.00, 3.43, 750000, 37500, 1500, 22500.00, 3.57, 0.9600),
('EST_YT_003', 'YT_CAMP_003', 820000, 41000, 1640, 24600.00, 3.37, 850000, 42500, 1700, 25500.00, 3.49, 0.9647);