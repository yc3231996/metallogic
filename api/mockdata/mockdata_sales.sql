CREATE TABLE SalesData (
    amount DECIMAL(10, 2) NOT NULL,
    product VARCHAR(255) NOT NULL,
    productType VARCHAR(255) NOT NULL,
    store VARCHAR(255) NOT NULL,
    province VARCHAR(255) NOT NULL,
    area VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    salesMan VARCHAR(255) NOT NULL,
    manager VARCHAR(255) NOT NULL,
    orderNumber VARCHAR(255) NOT NULL,
    PRIMARY KEY (orderNumber)
);

COMMENT ON COLUMN SalesData.amount IS '销售金额';
COMMENT ON COLUMN SalesData.product IS '产品名称';
COMMENT ON COLUMN SalesData.productType IS '产品类型';
COMMENT ON COLUMN SalesData.store IS '商店名称';
COMMENT ON COLUMN SalesData.province IS '省份';
COMMENT ON COLUMN SalesData.area IS '区域';
COMMENT ON COLUMN SalesData.date IS '交易日期';
COMMENT ON COLUMN SalesData.salesMan IS '销售人员姓名';
COMMENT ON COLUMN SalesData.manager IS '经理姓名';
COMMENT ON COLUMN SalesData.orderNumber IS '订单号';



INSERT INTO SalesData (amount, product, productType, store, province, area, date, salesMan, manager, orderNumber)
VALUES
    (123.45, 'product-1', '类别1', '上海浦东陆家嘴店', '上海', '华中', '2024-05-01', '销售员1', '经理1', 'order-00001'),
    (234.56, 'product-2', '类别2', '北京王府井店', '北京', '华北', '2024-05-02', '销售员2', '经理2', 'order-00002'),
    (99.99, 'product-3', '类别3', '广州天河城店', '广东省', '华南', '2024-05-03', '销售员3', '经理3', 'order-00003'),
    (150.75, 'product-4', '类别1', '河北省石家庄店', '河北省', '华北', '2024-05-04', '销售员4', '经理4', 'order-00004'),
    (278.30, 'product-5', '类别2', '湖南省长沙店', '湖南省', '华南', '2024-05-05', '销售员5', '经理5', 'order-00005'),
    (89.60, 'product-6', '类别3', '四川省成都春熙路店', '四川省', '华南', '2024-05-06', '销售员6', '经理6', 'order-00006'),
    (130.50, 'product-7', '类别1', '贵州省贵阳花果园店', '贵州省', '华南', '2024-05-07', '销售员7', '经理7', 'order-00007'),
    (210.40, 'product-8', '类别2', '北京中关村店', '北京', '华北', '2024-05-08', '销售员8', '经理2', 'order-00008'),
    (300.00, 'product-9', '类别3', '上海南京东路店', '上海', '华中', '2024-05-09', '销售员1', '经理1', 'order-00009'),
    (176.70, 'product-10', '类别1', '广东省深圳罗湖店', '广东省', '华南', '2024-05-10', '销售员9', '经理9', 'order-00010'),
    (50.25, 'product-1', '类别1', '河北省保定店', '河北省', '华北', '2024-05-11', '销售员10', '经理4', 'order-00011'),
    (200.15, 'product-2', '类别2', '湖南省株洲店', '湖南省', '华南', '2024-05-12', '销售员11', '经理5', 'order-00012'),
    (180.80, 'product-3', '类别3', '四川省重庆解放碑店', '四川省', '华南', '2024-05-13', '销售员12', '经理6', 'order-00013'),
    (215.00, 'product-4', '类别1', '贵州省安顺店', '贵州省', '华南', '2024-05-14', '销售员13', '经理7', 'order-00014'),
    (55.70, 'product-5', '类别2', '北京朝阳大悦城店', '北京', '华北', '2024-05-15', '销售员14', '经理2', 'order-00015'),
    (290.90, 'product-6', '类别3', '上海徐家汇店', '上海', '华中', '2024-05-16', '销售员1', '经理1', 'order-00016'),
    (175.55, 'product-7', '类别1', '广东省佛山顺德店', '广东省', '华南', '2024-05-17', '销售员15', '经理9', 'order-00017'),
    (120.35, 'product-8', '类别2', '河北省唐山店', '河北省', '华北', '2024-05-18', '销售员16', '经理4', 'order-00018'),
    (300.00, 'product-9', '类别3', '湖南省衡阳店', '湖南省', '华南', '2024-05-19', '销售员17', '经理5', 'order-00019'),
    (67.80, 'product-10', '类别1', '四川省乐山店', '四川省', '华南', '2024-05-20', '销售员18', '经理6', 'order-00020'),
    (245.25, 'product-1', '类别1', '贵州省遵义店', '贵州省', '华南', '2024-05-21', '销售员19', '经理7', 'order-00021'),
    (99.00, 'product-2', '类别2', '北京西单大悦城店', '北京', '华北', '2024-05-22', '销售员20', '经理2', 'order-00022'),
    (199.75, 'product-3', '类别3', '上海静安寺店', '上海', '华中', '2024-05-23', '销售员1', '经理1', 'order-00023'),
    (150.00, 'product-4', '类别1', '广东省东莞长安店', '广东省', '华南', '2024-05-24', '销售员21', '经理9', 'order-00024'),
    (185.50, 'product-5', '类别2', '河北省廊坊店', '河北省', '华北', '2024-05-25', '销售员22', '经理4', 'order-00025'),
    (230.60, 'product-6', '类别3', '湖南省岳阳店', '湖南省', '华南', '2024-05-26', '销售员23', '经理5', 'order-00026'),
    (110.80, 'product-7', '类别1', '四川省南充店', '四川省', '华南', '2024-05-27', '销售员24', '经理6', 'order-00027'),
    (199.99, 'product-8', '类别2', '贵州省毕节店', '贵州省', '华南', '2024-05-28', '销售员25', '经理7', 'order-00028'),
    (135.45, 'product-9', '类别3', '北京顺义店', '北京', '华北', '2024-05-29', '销售员26', '经理2', 'order-00029'),
    (88.95, 'product-10', '类别1', '上海宝山店', '上海', '华中', '2024-05-30', '销售员1', '经理1', 'order-00030'),
    (275.25, 'product-1', '类别1', '广东省珠海香洲店', '广东省', '华南', '2024-05-31', '销售员27', '经理9', 'order-00031'),
    (240.85, 'product-2', '类别2', '河北省邯郸店', '河北省', '华北', '2024-06-01', '销售员28', '经理4', 'order-00032'),
    (95.60, 'product-3', '类别3', '湖南省常德店', '湖南省', '华南', '2024-06-02', '销售员29', '经理5', 'order-00033'),
    (140.75, 'product-4', '类别1', '四川省泸州店', '四川省', '华南', '2024-06-03', '销售员30', '经理6', 'order-00034'),
    (210.90, 'product-5', '类别2', '贵州省六盘水店', '贵州省', '华南', '2024-06-04', '销售员31', '经理7', 'order-00035'),
    (160.25, 'product-6', '类别3', '北京海淀店', '北京', '华北', '2024-06-05', '销售员32', '经理2', 'order-00036'),
    (190.50, 'product-7', '类别1', '上海闵行店', '上海', '华中', '2024-06-06', '销售员1', '经理1', 'order-00037'),
    (175.00, 'product-8', '类别2', '广东省汕头店', '广东省', '华南', '2024-06-07', '销售员33', '经理9', 'order-00038'),
    (123.45, 'product-9', '类别3', '河北省秦皇岛店', '河北省', '华北', '2024-06-08', '销售员34', '经理4', 'order-00039'),
    (234.56, 'product-10', '类别1', '湖南省永州店', '湖南省', '华南', '2024-06-09', '销售员35', '经理5', 'order-00040'),
    (99.99, 'product-1', '类别1', '四川省雅安店', '四川省', '华南', '2024-06-10', '销售员36', '经理6', 'order-00041'),
    (150.75, 'product-2', '类别2', '贵州省安顺店', '贵州省', '华南', '2024-06-11', '销售员37', '经理7', 'order-00042'),
    (278.30, 'product-3', '类别3', '北京通州店', '北京', '华北', '2024-06-12', '销售员38', '经理2', 'order-00043'),
    (89.60, 'product-4', '类别1', '上海虹桥店', '上海', '华中', '2024-06-13', '销售员1', '经理1', 'order-00044'),
    (130.50, 'product-5', '类别2', '广东省中山店', '广东省', '华南', '2024-06-14', '销售员39', '经理9', 'order-00045'),
    (210.40, 'product-6', '类别3', '河北省沧州店', '河北省', '华北', '2024-06-15', '销售员40', '经理4', 'order-00046'),
    (300.00, 'product-7', '类别1', '湖南省邵阳店', '湖南省', '华南', '2024-06-16', '销售员41', '经理5', 'order-00047'),
    (176.70, 'product-8', '类别2', '四川省宜宾店', '四川省', '华南', '2024-06-17', '销售员42', '经理6', 'order-00048'),
    (50.25, 'product-9', '类别3', '贵州省凯里店', '贵州省', '华南', '2024-06-18', '销售员43', '经理7', 'order-00049'),
    (200.15, 'product-10', '类别1', '北京丰台店', '北京', '华北', '2024-06-19', '销售员44', '经理2', 'order-00050');




--------------------version2-------------------

-- 创建销售大宽表
CREATE TABLE SalesWideTable (
    orderNumber VARCHAR(255) PRIMARY KEY,
    transactionDate TIMESTAMP NOT NULL,
    productID VARCHAR(50) NOT NULL,
    productName VARCHAR(255) NOT NULL,
    productCategory VARCHAR(100) NOT NULL,
    productSubCategory VARCHAR(100) NOT NULL,
    unitPrice DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    totalAmount DECIMAL(10, 2) NOT NULL,
    discountAmount DECIMAL(10, 2) DEFAULT 0,
    netAmount DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    profit DECIMAL(10, 2) NOT NULL,
    storeID VARCHAR(50) NOT NULL,
    storeName VARCHAR(255) NOT NULL,
    storeType VARCHAR(50) NOT NULL,
    storeSize DECIMAL(10, 2) NOT NULL,
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    salesChannelID VARCHAR(50) NOT NULL,
    salesChannel VARCHAR(100) NOT NULL,
    paymentMethod VARCHAR(50) NOT NULL,
    customerID VARCHAR(50),
    customerType VARCHAR(50),
    salesmanID VARCHAR(50) NOT NULL,
    salesmanName VARCHAR(255) NOT NULL,
    promotionID VARCHAR(50),
    promotionName VARCHAR(255),
    seasonality VARCHAR(50),
    weekday VARCHAR(20),
    isHoliday BOOLEAN
);

-- 为表字段添加注释
COMMENT ON COLUMN SalesWideTable.orderNumber IS '订单号，唯一标识一笔交易';
COMMENT ON COLUMN SalesWideTable.transactionDate IS '交易日期和时间';
COMMENT ON COLUMN SalesWideTable.productID IS '产品ID';
COMMENT ON COLUMN SalesWideTable.productName IS '产品名称';
COMMENT ON COLUMN SalesWideTable.productCategory IS '产品大类';
COMMENT ON COLUMN SalesWideTable.productSubCategory IS '产品子类';
COMMENT ON COLUMN SalesWideTable.unitPrice IS '产品单价';
COMMENT ON COLUMN SalesWideTable.quantity IS '购买数量';
COMMENT ON COLUMN SalesWideTable.totalAmount IS '交易总金额（未扣除折扣）';
COMMENT ON COLUMN SalesWideTable.discountAmount IS '折扣金额';
COMMENT ON COLUMN SalesWideTable.netAmount IS '实际交易金额（已扣除折扣）';
COMMENT ON COLUMN SalesWideTable.cost IS '产品成本';
COMMENT ON COLUMN SalesWideTable.profit IS '利润（实际交易金额 - 成本）';
COMMENT ON COLUMN SalesWideTable.storeID IS '门店ID';
COMMENT ON COLUMN SalesWideTable.storeName IS '门店名称';
COMMENT ON COLUMN SalesWideTable.storeType IS '门店类型（如：旗舰店、标准店、小型店等）';
COMMENT ON COLUMN SalesWideTable.storeSize IS '门店面积（平方米）';
COMMENT ON COLUMN SalesWideTable.city IS '门店所在城市';
COMMENT ON COLUMN SalesWideTable.province IS '门店所在省份';
COMMENT ON COLUMN SalesWideTable.region IS '门店所在区域（如：华东、华北等）';
COMMENT ON COLUMN SalesWideTable.salesChannelID IS '销售渠道ID';
COMMENT ON COLUMN SalesWideTable.salesChannel IS '销售渠道名称（如：实体店、官网、第三方平台等）';
COMMENT ON COLUMN SalesWideTable.paymentMethod IS '支付方式（如：现金、信用卡、微信支付等）';
COMMENT ON COLUMN SalesWideTable.customerID IS '客户ID（如果有会员系统）';
COMMENT ON COLUMN SalesWideTable.customerType IS '客户类型（如：新客户、老客户、VIP等）';
COMMENT ON COLUMN SalesWideTable.salesmanID IS '销售人员ID';
COMMENT ON COLUMN SalesWideTable.salesmanName IS '销售人员姓名';
COMMENT ON COLUMN SalesWideTable.promotionID IS '促销活动ID（如果适用）';
COMMENT ON COLUMN SalesWideTable.promotionName IS '促销活动名称（如果适用）';
COMMENT ON COLUMN SalesWideTable.seasonality IS '季节性标记（如：春季、夏季、节日等）';
COMMENT ON COLUMN SalesWideTable.weekday IS '星期几（如：周一、周二等）';
COMMENT ON COLUMN SalesWideTable.isHoliday IS '是否为法定假日';

-- 创建索引
CREATE INDEX idx_transactionDate ON SalesWideTable(transactionDate);
CREATE INDEX idx_productID ON SalesWideTable(productID);
CREATE INDEX idx_storeID ON SalesWideTable(storeID);
CREATE INDEX idx_salesmanID ON SalesWideTable(salesmanID);
CREATE INDEX idx_customerID ON SalesWideTable(customerID);


-- create mock data
-- 清空现有数据
TRUNCATE TABLE SalesWideTable;

-- 设置随机种子
SELECT setseed(0.5);

-- 创建辅助函数
CREATE OR REPLACE FUNCTION random_between(low INT, high INT) 
   RETURNS INT AS
$$
BEGIN
   RETURN floor(random()* (high-low + 1) + low);
END;
$$ language 'plpgsql' STRICT;

-- 插入测试数据
INSERT INTO SalesWideTable (
    orderNumber, transactionDate, productID, productName, productCategory, productSubCategory,
    unitPrice, quantity, totalAmount, discountAmount, netAmount, cost, profit,
    storeID, storeName, storeType, storeSize, city, province, region,
    salesChannelID, salesChannel, paymentMethod, customerID, customerType,
    salesmanID, salesmanName, promotionID, promotionName, seasonality, weekday, isHoliday
)
SELECT
    'ORD-' || LPAD(CAST(generate_series AS VARCHAR), 8, '0') AS orderNumber,
    timestamp '2022-01-01 00:00:00' +
       random() * (timestamp '2024-01-01 00:00:00' -
                   timestamp '2022-01-01 00:00:00') AS transactionDate,
    'PROD-' || LPAD(CAST(random_between(1, 100) AS VARCHAR), 3, '0') AS productID,
    (ARRAY['T-shirt', 'Jeans', 'Dress', 'Shoes', 'Hat', 'Bag', 'Watch', 'Sunglasses', 'Scarf', 'Jacket'])[random_between(1, 10)] AS productName,
    (ARRAY['Clothing', 'Accessories', 'Footwear'])[random_between(1, 3)] AS productCategory,
    (ARRAY['Tops', 'Bottoms', 'Dresses', 'Shoes', 'Headwear', 'Bags', 'Jewelry', 'Eyewear', 'Neckwear', 'Outerwear'])[random_between(1, 10)] AS productSubCategory,
    random_between(20, 200)::DECIMAL AS unitPrice,
    random_between(1, 5) AS quantity,
    0 AS totalAmount, -- Will be calculated later
    random_between(0, 20)::DECIMAL AS discountAmount,
    0 AS netAmount, -- Will be calculated later
    random_between(10, 100)::DECIMAL AS cost,
    0 AS profit, -- Will be calculated later
    'ST-' || LPAD(CAST(random_between(1, 50) AS VARCHAR), 3, '0') AS storeID,
    'Store ' || random_between(1, 50) AS storeName,
    (ARRAY['Flagship', 'Standard', 'Small'])[random_between(1, 3)] AS storeType,
    (CASE 
        WHEN (ARRAY['Flagship', 'Standard', 'Small'])[random_between(1, 3)] = 'Flagship' THEN random_between(1000, 2000)
        WHEN (ARRAY['Flagship', 'Standard', 'Small'])[random_between(1, 3)] = 'Standard' THEN random_between(500, 1000)
        ELSE random_between(100, 500)
     END)::DECIMAL AS storeSize,
    (ARRAY['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Chengdu', 'Hangzhou', 'Wuhan', 'Xian', 'Chongqing', 'Nanjing'])[random_between(1, 10)] AS city,
    (ARRAY['Beijing', 'Shanghai', 'Guangdong', 'Guangdong', 'Sichuan', 'Zhejiang', 'Hubei', 'Shaanxi', 'Chongqing', 'Jiangsu'])[random_between(1, 10)] AS province,
    (ARRAY['North', 'East', 'South', 'West', 'Central'])[random_between(1, 5)] AS region,
    'CH-' || LPAD(CAST(random_between(1, 5) AS VARCHAR), 2, '0') AS salesChannelID,
    (ARRAY['In-store', 'Online', 'Mobile App', 'Phone', 'Partner'])[random_between(1, 5)] AS salesChannel,
    (ARRAY['Cash', 'Credit Card', 'Debit Card', 'Mobile Payment', 'Online Transfer'])[random_between(1, 5)] AS paymentMethod,
    CASE WHEN random() < 0.8 THEN 'CUST-' || LPAD(CAST(random_between(1, 1000) AS VARCHAR), 5, '0') ELSE NULL END AS customerID,
    (ARRAY['New', 'Regular', 'VIP'])[random_between(1, 3)] AS customerType,
    'EMP-' || LPAD(CAST(random_between(1, 100) AS VARCHAR), 3, '0') AS salesmanID,
    'Salesperson ' || random_between(1, 100) AS salesmanName,
    CASE WHEN random() < 0.3 THEN 'PROMO-' || LPAD(CAST(random_between(1, 20) AS VARCHAR), 3, '0') ELSE NULL END AS promotionID,
    CASE WHEN random() < 0.3 THEN 'Promotion ' || random_between(1, 20) ELSE NULL END AS promotionName,
    (ARRAY['Spring', 'Summer', 'Autumn', 'Winter'])[random_between(1, 4)] AS seasonality,
    (ARRAY['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])[random_between(1, 7)] AS weekday,
    CASE WHEN random() < 0.05 THEN TRUE ELSE FALSE END AS isHoliday
FROM generate_series(1, 100000);

-- 更新计算字段
UPDATE SalesWideTable
SET totalAmount = unitPrice * quantity,
    netAmount = (unitPrice * quantity) - discountAmount,
    profit = netAmount - (cost * quantity);

-- 创建一些特定的促销活动
UPDATE SalesWideTable
SET promotionID = 'PROMO-SUMMER',
    promotionName = 'Summer Sale',
    discountAmount = netAmount * 0.2,
    netAmount = netAmount * 0.8,
    profit = netAmount - (cost * quantity)
WHERE seasonality = 'Summer' AND random() < 0.5;

UPDATE SalesWideTable
SET promotionID = 'PROMO-WINTER',
    promotionName = 'Winter Clearance',
    discountAmount = netAmount * 0.3,
    netAmount = netAmount * 0.7,
    profit = netAmount - (cost * quantity)
WHERE seasonality = 'Winter' AND random() < 0.5;

-- 为节假日设置更高的销售量
UPDATE SalesWideTable
SET quantity = quantity * 2,
    totalAmount = unitPrice * (quantity * 2),
    netAmount = (unitPrice * (quantity * 2)) - discountAmount,
    profit = netAmount - (cost * (quantity * 2))
WHERE isHoliday = TRUE;

-- 添加一些畅销产品
UPDATE SalesWideTable
SET quantity = quantity * 3,
    totalAmount = unitPrice * (quantity * 3),
    netAmount = (unitPrice * (quantity * 3)) - discountAmount,
    profit = netAmount - (cost * (quantity * 3))
WHERE productName IN ('T-shirt', 'Jeans', 'Dress') AND random() < 0.3;

-- 为VIP客户提供更多折扣
UPDATE SalesWideTable
SET discountAmount = netAmount * 0.1,
    netAmount = netAmount * 0.9,
    profit = netAmount - (cost * quantity)
WHERE customerType = 'VIP';

-- 为一些低销量产品设置更高的利润率
UPDATE SalesWideTable
SET unitPrice = unitPrice * 1.5,
    totalAmount = (unitPrice * 1.5) * quantity,
    netAmount = ((unitPrice * 1.5) * quantity) - discountAmount,
    profit = netAmount - (cost * quantity)
WHERE productName IN ('Scarf', 'Hat') AND random() < 0.5;

-- 模拟一些产品的季节性波动
UPDATE SalesWideTable
SET quantity = CASE 
    WHEN seasonality = 'Summer' AND productName IN ('T-shirt', 'Sunglasses', 'Hat') THEN quantity * 2
    WHEN seasonality = 'Winter' AND productName IN ('Jacket', 'Scarf') THEN quantity * 2
    ELSE quantity
END,
totalAmount = unitPrice * CASE 
    WHEN seasonality = 'Summer' AND productName IN ('T-shirt', 'Sunglasses', 'Hat') THEN quantity * 2
    WHEN seasonality = 'Winter' AND productName IN ('Jacket', 'Scarf') THEN quantity * 2
    ELSE quantity
END,
netAmount = (unitPrice * CASE 
    WHEN seasonality = 'Summer' AND productName IN ('T-shirt', 'Sunglasses', 'Hat') THEN quantity * 2
    WHEN seasonality = 'Winter' AND productName IN ('Jacket', 'Scarf') THEN quantity * 2
    ELSE quantity
END) - discountAmount,
profit = (unitPrice * CASE 
    WHEN seasonality = 'Summer' AND productName IN ('T-shirt', 'Sunglasses', 'Hat') THEN quantity * 2
    WHEN seasonality = 'Winter' AND productName IN ('Jacket', 'Scarf') THEN quantity * 2
    ELSE quantity
END) - discountAmount - (cost * CASE 
    WHEN seasonality = 'Summer' AND productName IN ('T-shirt', 'Sunglasses', 'Hat') THEN quantity * 2
    WHEN seasonality = 'Winter' AND productName IN ('Jacket', 'Scarf') THEN quantity * 2
    ELSE quantity
END);

-- 为销售渠道设置一些特征
UPDATE SalesWideTable
SET quantity = quantity * 1.2,
    totalAmount = unitPrice * (quantity * 1.2),
    netAmount = (unitPrice * (quantity * 1.2)) - discountAmount,
    profit = netAmount - (cost * (quantity * 1.2))
WHERE salesChannel = 'Online' AND random() < 0.6;

-- 更新统计信息
ANALYZE SalesWideTable;
