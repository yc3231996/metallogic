-- mock data for MES system

-- 生产计划表 (ProductionPlan)
CREATE TABLE ProductionPlan (
    PlanID INT PRIMARY KEY,
    OrderNumber VARCHAR(50),
    ProductModel VARCHAR(50),
    PlannedStartTime TIMESTAMP,
    PlannedEndTime TIMESTAMP,
    Quantity INT
);

COMMENT ON TABLE ProductionPlan IS '生产计划表。PlanID为主键。';
COMMENT ON COLUMN ProductionPlan.OrderNumber IS '订单号';
COMMENT ON COLUMN ProductionPlan.ProductModel IS '产品型号';
COMMENT ON COLUMN ProductionPlan.PlannedStartTime IS '计划开始时间';
COMMENT ON COLUMN ProductionPlan.PlannedEndTime IS '计划结束时间';
COMMENT ON COLUMN ProductionPlan.Quantity IS '计划生产数量';

-- 生产进度表 (ProductionProgress)
CREATE TABLE ProductionProgress (
    ProgressID INT PRIMARY KEY,
    PlanID INT,
    ProcessStep VARCHAR(50),
    Status VARCHAR(20),
    CompletionTime TIMESTAMP,
    ProgressPercentage DECIMAL(5,2)
);

COMMENT ON TABLE ProductionProgress IS '生产进度表。ProgressID为主键，PlanID为外键。';
COMMENT ON COLUMN ProductionProgress.PlanID IS '生产计划ID，关联ProductionPlan表的PlanID';
COMMENT ON COLUMN ProductionProgress.ProcessStep IS '工序步骤';
COMMENT ON COLUMN ProductionProgress.Status IS '工序状态';
COMMENT ON COLUMN ProductionProgress.CompletionTime IS '完成时间';
COMMENT ON COLUMN ProductionProgress.ProgressPercentage IS '完成百分比';

-- 生产效率表 (ProductionEfficiency)
CREATE TABLE ProductionEfficiency (
    EfficiencyID INT PRIMARY KEY,
    PlanID INT,
    Output INT,
    EfficiencyRate DECIMAL(5,2),
    ProductionTime DECIMAL(10,2)
);

COMMENT ON TABLE ProductionEfficiency IS '生产效率表。EfficiencyID为主键，PlanID为外键。';
COMMENT ON COLUMN ProductionEfficiency.PlanID IS '生产计划ID，关联ProductionPlan表的PlanID';
COMMENT ON COLUMN ProductionEfficiency.Output IS '实际产量';
COMMENT ON COLUMN ProductionEfficiency.EfficiencyRate IS '生产效率';
COMMENT ON COLUMN ProductionEfficiency.ProductionTime IS '实际生产时间（小时）';

-- 不良品分析表 (DefectAnalysis)
CREATE TABLE DefectAnalysis (
    AnalysisID INT PRIMARY KEY,
    PlanID INT,
    DefectType VARCHAR(50),
    DefectCount INT,
    AnalysisTime TIMESTAMP,
    Cause VARCHAR(255),
    UNIQUE (PlanID, DefectType)
);

COMMENT ON TABLE DefectAnalysis IS '不良品分析表。AnalysisID为主键，PlanID为外键。';
COMMENT ON COLUMN DefectAnalysis.PlanID IS '生产计划ID，关联ProductionPlan表的PlanID';
COMMENT ON COLUMN DefectAnalysis.DefectType IS '不良品类型';
COMMENT ON COLUMN DefectAnalysis.DefectCount IS '不良品数量';
COMMENT ON COLUMN DefectAnalysis.AnalysisTime IS '分析时间';
COMMENT ON COLUMN DefectAnalysis.Cause IS '不良品产生原因';

-- 原材料库存表 (RawMaterialInventory)
CREATE TABLE RawMaterialInventory (
    MaterialID INT PRIMARY KEY,
    MaterialNumber VARCHAR(50),
    MaterialName VARCHAR(50),
    Supplier VARCHAR(50),
    Quantity INT,
    StorageTime TIMESTAMP,
    ConsumptionRate DECIMAL(10,2),
    UNIQUE (MaterialNumber, StorageTime)
);

COMMENT ON TABLE RawMaterialInventory IS '原材料库存表。MaterialID为主键，MaterialNumber为外键。';
COMMENT ON COLUMN RawMaterialInventory.MaterialNumber IS '物料编号';
COMMENT ON COLUMN RawMaterialInventory.MaterialName IS '物料名称';
COMMENT ON COLUMN RawMaterialInventory.Supplier IS '供应商';
COMMENT ON COLUMN RawMaterialInventory.Quantity IS '当前库存数量';
COMMENT ON COLUMN RawMaterialInventory.StorageTime IS '入库时间';
COMMENT ON COLUMN RawMaterialInventory.ConsumptionRate IS '消耗速率';

-- 成品库存表 (FinishedGoodsInventory)
CREATE TABLE FinishedGoodsInventory (
    ProductID INT PRIMARY KEY,
    ProductNumber VARCHAR(50),
    ProductName VARCHAR(50),
    Quantity INT,
    StorageTime TIMESTAMP,
    OutboundTime TIMESTAMP,
    UNIQUE (ProductNumber, StorageTime)
);

COMMENT ON TABLE FinishedGoodsInventory IS '成品库存表。ProductID为主键，ProductNumber为外键。';
COMMENT ON COLUMN FinishedGoodsInventory.ProductNumber IS '成品编号';
COMMENT ON COLUMN FinishedGoodsInventory.ProductName IS '成品名称';
COMMENT ON COLUMN FinishedGoodsInventory.Quantity IS '当前库存数量';
COMMENT ON COLUMN FinishedGoodsInventory.StorageTime IS '入库时间';
COMMENT ON COLUMN FinishedGoodsInventory.OutboundTime IS '出库时间';

-- 质量检查表 (QualityCheck)
CREATE TABLE QualityCheck (
    CheckID INT PRIMARY KEY,
    PlanID INT,
    ProcessStep VARCHAR(50),
    CheckTime TIMESTAMP,
    Passed BOOLEAN,
    DefectType VARCHAR(50)
);

COMMENT ON TABLE QualityCheck IS '质量检查表。CheckID为主键，PlanID为外键。';
COMMENT ON COLUMN QualityCheck.PlanID IS '生产计划ID，关联ProductionPlan表的PlanID';
COMMENT ON COLUMN QualityCheck.ProcessStep IS '工序步骤';
COMMENT ON COLUMN QualityCheck.CheckTime IS '检查时间';
COMMENT ON COLUMN QualityCheck.Passed IS '是否合格';
COMMENT ON COLUMN QualityCheck.DefectType IS '不合格类型';

-- 设备使用情况表 (EquipmentUsage)
CREATE TABLE EquipmentUsage (
    UsageID INT PRIMARY KEY,
    EquipmentID INT,
    UsageStartTime TIMESTAMP,
    UsageEndTime TIMESTAMP,
    Uptime DECIMAL(10,2),
    Downtime DECIMAL(10,2)
);

COMMENT ON TABLE EquipmentUsage IS '设备使用情况表。UsageID为主键。';
COMMENT ON COLUMN EquipmentUsage.EquipmentID IS '设备ID';
COMMENT ON COLUMN EquipmentUsage.UsageStartTime IS '设备使用开始时间';
COMMENT ON COLUMN EquipmentUsage.UsageEndTime IS '设备使用结束时间';
COMMENT ON COLUMN EquipmentUsage.Uptime IS '开机时间（小时）';
COMMENT ON COLUMN EquipmentUsage.Downtime IS '停机时间（小时）';

-- 设备维护表 (EquipmentMaintenance)
CREATE TABLE EquipmentMaintenance (
    MaintenanceID INT PRIMARY KEY,
    EquipmentID INT,
    MaintenanceTime TIMESTAMP,
    MaintenanceDetails VARCHAR(255),
    MaintenancePersonnel VARCHAR(50)
);

COMMENT ON TABLE EquipmentMaintenance IS '设备维护表。MaintenanceID为主键。';
COMMENT ON COLUMN EquipmentMaintenance.EquipmentID IS '设备ID';
COMMENT ON COLUMN EquipmentMaintenance.MaintenanceTime IS '维护时间';
COMMENT ON COLUMN EquipmentMaintenance.MaintenanceDetails IS '维护内容';
COMMENT ON COLUMN EquipmentMaintenance.MaintenancePersonnel IS '维护人员';

-- 设备故障分析表 (EquipmentFailureAnalysis)
CREATE TABLE EquipmentFailureAnalysis (
    FailureID INT PRIMARY KEY,
    EquipmentID INT,
    FailureTime TIMESTAMP,
    FailureReason VARCHAR(255),
    RepairTime DECIMAL(10,2)
);

COMMENT ON TABLE EquipmentFailureAnalysis IS '设备故障分析表。FailureID为主键。';
COMMENT ON COLUMN EquipmentFailureAnalysis.EquipmentID IS '设备ID';
COMMENT ON COLUMN EquipmentFailureAnalysis.FailureTime IS '故障时间';
COMMENT ON COLUMN EquipmentFailureAnalysis.FailureReason IS '故障原因';
COMMENT ON COLUMN EquipmentFailureAnalysis.RepairTime IS '修复时间（小时）';



------ mock data generation------

-- 清空现有数据
TRUNCATE TABLE ProductionPlan, ProductionProgress, ProductionEfficiency, DefectAnalysis, 
             RawMaterialInventory, FinishedGoodsInventory, QualityCheck, EquipmentUsage, 
             EquipmentMaintenance, EquipmentFailureAnalysis;

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

-- 插入生产计划数据
INSERT INTO ProductionPlan (PlanID, OrderNumber, ProductModel, PlannedStartTime, PlannedEndTime, Quantity)
SELECT
    generate_series,
    'ORD-' || LPAD(CAST(generate_series AS VARCHAR), 5, '0'),
    (ARRAY['Model-A', 'Model-B', 'Model-C', 'Model-D', 'Model-E'])[random_between(1, 5)],
    NOW() - INTERVAL '30 days' + (random() * INTERVAL '60 days'),
    NOW() - INTERVAL '30 days' + (random() * INTERVAL '60 days') + INTERVAL '2 days',
    random_between(100, 1000)
FROM generate_series(1, 1000);

-- 更新PlannedEndTime确保在PlannedStartTime之后
UPDATE ProductionPlan
SET PlannedEndTime = PlannedStartTime + (random() * INTERVAL '5 days')
WHERE PlannedEndTime <= PlannedStartTime;

-- 插入生产进度数据
INSERT INTO ProductionProgress (ProgressID, PlanID, ProcessStep, Status, CompletionTime, ProgressPercentage)
SELECT
    ROW_NUMBER() OVER () AS ProgressID,
    PlanID,
    (ARRAY['Cutting', 'Welding', 'Assembly', 'Painting', 'Testing'])[random_between(1, 5)],
    (ARRAY['In Progress', 'Completed', 'Delayed'])[random_between(1, 3)],
    CASE 
        WHEN random() < 0.8 THEN PlannedStartTime + (random() * (PlannedEndTime - PlannedStartTime))
        ELSE NULL
    END,
    CASE 
        WHEN random() < 0.8 THEN random() * 100
        ELSE NULL
    END
FROM ProductionPlan
CROSS JOIN generate_series(1, 3);

-- 插入生产效率数据
INSERT INTO ProductionEfficiency (EfficiencyID, PlanID, Output, EfficiencyRate, ProductionTime)
SELECT
    ROW_NUMBER() OVER () AS EfficiencyID,
    PlanID,
    FLOOR(Quantity * random()),
    60 + (random() * 40),
    EXTRACT(EPOCH FROM (PlannedEndTime - PlannedStartTime)) / 3600
FROM ProductionPlan;

-- 插入不良品分析数据
INSERT INTO DefectAnalysis (AnalysisID, PlanID, DefectType, DefectCount, AnalysisTime, Cause)
SELECT
    ROW_NUMBER() OVER () AS AnalysisID,
    PlanID,
    (ARRAY['Scratch', 'Dent', 'Color Mismatch', 'Size Error', 'Functionality Issue'])[random_between(1, 5)],
    random_between(1, 50),
    PlannedEndTime + (random() * INTERVAL '1 day'),
    (ARRAY['Material Defect', 'Machine Malfunction', 'Human Error', 'Process Issue', 'Unknown'])[random_between(1, 5)]
FROM ProductionPlan
CROSS JOIN generate_series(1, 2)
ON CONFLICT (PlanID, DefectType) DO NOTHING;

-- 插入原材料库存数据
INSERT INTO RawMaterialInventory (MaterialID, MaterialNumber, MaterialName, Supplier, Quantity, StorageTime, ConsumptionRate)
SELECT
    generate_series,
    'MAT-' || LPAD(CAST(generate_series AS VARCHAR), 4, '0'),
    (ARRAY['Steel', 'Plastic', 'Copper', 'Aluminum', 'Rubber'])[random_between(1, 5)],
    (ARRAY['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D', 'Supplier E'])[random_between(1, 5)],
    random_between(1000, 10000),
    NOW() - (random() * INTERVAL '90 days'),
    random_between(10, 100)
FROM generate_series(1, 100);

-- 插入成品库存数据
INSERT INTO FinishedGoodsInventory (ProductID, ProductNumber, ProductName, Quantity, StorageTime, OutboundTime)
SELECT
    generate_series,
    'PROD-' || LPAD(CAST(generate_series AS VARCHAR), 4, '0'),
    (ARRAY['Product A', 'Product B', 'Product C', 'Product D', 'Product E'])[random_between(1, 5)],
    random_between(100, 1000),
    NOW() - (random() * INTERVAL '30 days'),
    CASE 
        WHEN random() < 0.5 THEN NOW() - (random() * INTERVAL '15 days')
        ELSE NULL
    END
FROM generate_series(1, 500);

-- 插入质量检查数据
INSERT INTO QualityCheck (CheckID, PlanID, ProcessStep, CheckTime, Passed, DefectType)
SELECT
    ROW_NUMBER() OVER () AS CheckID,
    PlanID,
    (ARRAY['Cutting', 'Welding', 'Assembly', 'Painting', 'Testing'])[random_between(1, 5)],
    PlannedStartTime + (random() * (PlannedEndTime - PlannedStartTime)),
    CASE WHEN random() < 0.9 THEN TRUE ELSE FALSE END,
    CASE 
        WHEN random() >= 0.9 THEN (ARRAY['Scratch', 'Dent', 'Color Mismatch', 'Size Error', 'Functionality Issue'])[random_between(1, 5)]
        ELSE NULL
    END
FROM ProductionPlan
CROSS JOIN generate_series(1, 5);

-- 插入设备使用情况数据
INSERT INTO EquipmentUsage (UsageID, EquipmentID, UsageStartTime, UsageEndTime, Uptime, Downtime)
SELECT
    ROW_NUMBER() OVER () AS UsageID,
    random_between(1, 20),
    NOW() - INTERVAL '30 days' + (random() * INTERVAL '30 days'),
    NOW() - INTERVAL '30 days' + (random() * INTERVAL '30 days') + INTERVAL '1 day',
    random() * 24,
    random() * 2
FROM generate_series(1, 1000);

-- 更新UsageEndTime确保在UsageStartTime之后
UPDATE EquipmentUsage
SET UsageEndTime = UsageStartTime + INTERVAL '1 day' * (Uptime + Downtime) / 24
WHERE UsageEndTime <= UsageStartTime;

-- 插入设备维护数据
INSERT INTO EquipmentMaintenance (MaintenanceID, EquipmentID, MaintenanceTime, MaintenanceDetails, MaintenancePersonnel)
SELECT
    ROW_NUMBER() OVER () AS MaintenanceID,
    random_between(1, 20),
    NOW() - (random() * INTERVAL '90 days'),
    (ARRAY['Routine Check', 'Oil Change', 'Parts Replacement', 'Calibration', 'Software Update'])[random_between(1, 5)],
    (ARRAY['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'])[random_between(1, 5)]
FROM generate_series(1, 200);

-- 插入设备故障分析数据
INSERT INTO EquipmentFailureAnalysis (FailureID, EquipmentID, FailureTime, FailureReason, RepairTime)
SELECT
    ROW_NUMBER() OVER () AS FailureID,
    random_between(1, 20),
    NOW() - (random() * INTERVAL '90 days'),
    (ARRAY['Wear and Tear', 'Electrical Failure', 'Software Glitch', 'Operator Error', 'Unknown'])[random_between(1, 5)],
    random_between(1, 48)
FROM generate_series(1, 100);

-- 更新统计信息
ANALYZE ProductionPlan, ProductionProgress, ProductionEfficiency, DefectAnalysis, 
        RawMaterialInventory, FinishedGoodsInventory, QualityCheck, EquipmentUsage, 
        EquipmentMaintenance, EquipmentFailureAnalysis;




-------------------------- old data --------------------------

-- Insert data into ProductionPlan table
INSERT INTO ProductionPlan (PlanID, OrderNumber, ProductModel, PlannedStartTime, PlannedEndTime, Quantity)
VALUES
(1, 'ORD-2024-001', 'Model-A', '2024-01-05 08:00:00', '2024-01-10 17:00:00', 500),
(2, 'ORD-2024-002', 'Model-B', '2024-01-15 08:00:00', '2024-01-20 17:00:00', 300),
(3, 'ORD-2024-003', 'Model-C', '2024-02-01 08:00:00', '2024-02-07 17:00:00', 1000),
(4, 'ORD-2024-004', 'Model-A', '2024-02-15 08:00:00', '2024-02-20 17:00:00', 600),
(5, 'ORD-2024-005', 'Model-B', '2024-03-01 08:00:00', '2024-03-05 17:00:00', 400),
(6, 'ORD-2024-006', 'Model-C', '2024-03-15 08:00:00', '2024-03-22 17:00:00', 1200),
(7, 'ORD-2024-007', 'Model-A', '2024-04-01 08:00:00', '2024-04-05 17:00:00', 550),
(8, 'ORD-2024-008', 'Model-B', '2024-04-15 08:00:00', '2024-04-20 17:00:00', 350),
(9, 'ORD-2024-009', 'Model-C', '2024-05-01 08:00:00', '2024-05-08 17:00:00', 1100),
(10, 'ORD-2024-010', 'Model-A', '2024-05-15 08:00:00', '2024-05-20 17:00:00', 580),
(11, 'ORD-2024-011', 'Model-B', '2024-06-01 08:00:00', '2024-06-05 17:00:00', 420),
(12, 'ORD-2024-012', 'Model-C', '2024-06-15 08:00:00', '2024-06-22 17:00:00', 1300),
(13, 'ORD-2024-013', 'Model-A', '2024-07-01 08:00:00', '2024-07-05 17:00:00', 530),
(14, 'ORD-2024-014', 'Model-B', '2024-07-15 08:00:00', '2024-07-20 17:00:00', 380),
(15, 'ORD-2024-015', 'Model-C', '2024-08-01 08:00:00', '2024-08-08 17:00:00', 1150),
(16, 'ORD-2024-016', 'Model-A', '2024-08-15 08:00:00', '2024-08-20 17:00:00', 610),
(17, 'ORD-2024-017', 'Model-B', '2024-09-01 08:00:00', '2024-09-05 17:00:00', 440),
(18, 'ORD-2024-018', 'Model-C', '2024-09-15 08:00:00', '2024-09-22 17:00:00', 1250),
(19, 'ORD-2024-019', 'Model-A', '2024-10-01 08:00:00', '2024-10-05 17:00:00', 570),
(20, 'ORD-2024-020', 'Model-B', '2024-10-15 08:00:00', '2024-10-20 17:00:00', 330),
(21, 'ORD-2024-021', 'Model-C', '2024-11-01 08:00:00', '2024-11-08 17:00:00', 1050),
(22, 'ORD-2024-022', 'Model-A', '2024-11-15 08:00:00', '2024-11-20 17:00:00', 590),
(23, 'ORD-2024-023', 'Model-B', '2024-12-01 08:00:00', '2024-12-05 17:00:00', 410),
(24, 'ORD-2024-024', 'Model-C', '2024-12-15 08:00:00', '2024-12-22 17:00:00', 1350),
(25, 'ORD-2024-025', 'Model-A', '2024-01-20 08:00:00', '2024-01-25 17:00:00', 520),
(26, 'ORD-2024-026', 'Model-B', '2024-02-10 08:00:00', '2024-02-15 17:00:00', 360),
(27, 'ORD-2024-027', 'Model-C', '2024-03-10 08:00:00', '2024-03-17 17:00:00', 1180),
(28, 'ORD-2024-028', 'Model-A', '2024-04-10 08:00:00', '2024-04-15 17:00:00', 540),
(29, 'ORD-2024-029', 'Model-B', '2024-05-10 08:00:00', '2024-05-15 17:00:00', 390),
(30, 'ORD-2024-030', 'Model-C', '2024-06-10 08:00:00', '2024-06-17 17:00:00', 1220);

-- Insert data into ProductionProgress table
INSERT INTO ProductionProgress (ProgressID, PlanID, ProcessStep, Status, CompletionTime, ProgressPercentage)
VALUES
(1, 1, 'Assembly', 'Completed', '2024-01-08 15:30:00', 100.00),
(2, 1, 'Quality Check', 'Completed', '2024-01-09 10:45:00', 100.00),
(3, 1, 'Packaging', 'Completed', '2024-01-10 14:20:00', 100.00),
(4, 2, 'Assembly', 'Completed', '2024-01-18 16:00:00', 100.00),
(5, 2, 'Quality Check', 'Completed', '2024-01-19 11:30:00', 100.00),
(6, 2, 'Packaging', 'In Progress', '2024-01-20 09:00:00', 75.50),
(7, 3, 'Assembly', 'In Progress', '2024-02-05 12:00:00', 80.00),
(8, 4, 'Assembly', 'Not Started', NULL, 0.00),
(9, 5, 'Assembly', 'Not Started', NULL, 0.00),
(10, 6, 'Assembly', 'Not Started', NULL, 0.00);

-- Insert data into ProductionEfficiency table
INSERT INTO ProductionEfficiency (EfficiencyID, PlanID, Output, EfficiencyRate, ProductionTime)
VALUES
(1, 1, 495, 99.00, 39.5),
(2, 2, 298, 99.33, 38.2),
(3, 3, 985, 98.50, 118.5),
(4, 4, 590, 98.33, 47.8),
(5, 5, 395, 98.75, 31.6);

-- Insert data into DefectAnalysis table
INSERT INTO DefectAnalysis (AnalysisID, PlanID, DefectType, DefectCount, AnalysisTime, Cause)
VALUES
(1, 1, 'Scratches', 3, '2024-01-10 16:30:00', 'Improper handling during assembly'),
(2, 1, 'Color mismatch', 2, '2024-01-10 16:45:00', 'Inconsistent paint batch'),
(3, 2, 'Loose connections', 2, '2024-01-19 14:00:00', 'Insufficient tightening during assembly'),
(4, 3, 'Component failure', 8, '2024-02-06 10:30:00', 'Faulty batch of capacitors'),
(5, 3, 'Packaging damage', 7, '2024-02-07 15:00:00', 'Packaging machine misalignment');

-- Insert data into RawMaterialInventory table
INSERT INTO RawMaterialInventory (MaterialID, MaterialNumber, MaterialName, Supplier, Quantity, StorageTime, ConsumptionRate)
VALUES
(1, 'RM-001', 'Aluminum Sheet', 'MetalCo', 5000, '2024-01-01 09:00:00', 100.5),
(2, 'RM-002', 'Copper Wire', 'WireTech', 10000, '2024-01-02 10:30:00', 50.25),
(3, 'RM-003', 'Plastic Resin', 'PolymerInc', 2000, '2024-01-03 11:45:00', 75.8),
(4, 'RM-004', 'LED Lights', 'LightingCorp', 20000, '2024-01-04 14:00:00', 200.0),
(5, 'RM-005', 'Screws', 'FastenerTech', 100000, '2024-01-05 15:30:00', 500.0);

-- Insert data into FinishedGoodsInventory table
INSERT INTO FinishedGoodsInventory (ProductID, ProductNumber, ProductName, Quantity, StorageTime, OutboundTime)
VALUES
(1, 'FG-001', 'Smart Thermostat', 1000, '2024-01-11 10:00:00', '2024-01-15 09:00:00'),
(2, 'FG-002', 'LED Bulb Pack', 5000, '2024-01-21 11:30:00', '2024-01-25 10:30:00'),
(3, 'FG-003', 'Wireless Speaker', 2000, '2024-02-08 14:00:00', '2024-02-12 13:00:00'),
(4, 'FG-004', 'Smart Lock', 1500, '2024-02-21 15:30:00', '2024-02-25 14:30:00'),
(5, 'FG-005', 'Robot Vacuum', 800, '2024-03-06 16:45:00', '2024-03-10 15:45:00');

-- Insert data into QualityCheck table
INSERT INTO QualityCheck (CheckID, PlanID, ProcessStep, CheckTime, Passed, DefectType)
VALUES
(1, 1, 'Assembly', '2024-01-08 16:00:00', TRUE, NULL),
(2, 1, 'Final Inspection', '2024-01-09 11:30:00', TRUE, NULL),
(3, 2, 'Assembly', '2024-01-18 16:30:00', FALSE, 'Loose connections'),
(4, 2, 'Assembly', '2024-01-19 09:00:00', TRUE, NULL),
(5, 2, 'Final Inspection', '2024-01-19 14:30:00', TRUE, NULL),
(6, 3, 'Assembly', '2024-02-05 15:00:00', FALSE, 'Component failure'),
(7, 3, 'Assembly', '2024-02-06 10:00:00', TRUE, NULL),
(8, 3, 'Final Inspection', '2024-02-07 11:00:00', FALSE, 'Packaging damage'),
(9, 3, 'Final Inspection', '2024-02-07 16:00:00', TRUE, NULL),
(10, 4, 'Assembly', '2024-02-17 14:00:00', TRUE, NULL);

-- Insert data into EquipmentUsage table
INSERT INTO EquipmentUsage (UsageID, EquipmentID, UsageStartTime, UsageEndTime, Uptime, Downtime)
VALUES
(1, 101, '2024-01-05 08:00:00', '2024-01-10 17:00:00', 39.5, 0.5),
(2, 102, '2024-01-15 08:00:00', '2024-01-20 17:00:00', 38.2, 1.8),
(3, 103, '2024-02-01 08:00:00', '2024-02-07 17:00:00', 118.5, 1.5),
(4, 101, '2024-02-15 08:00:00', '2024-02-20 17:00:00', 47.8, 0.2),
(5, 102, '2024-03-01 08:00:00', '2024-03-05 17:00:00', 31.6, 0.4);

-- Insert data into EquipmentMaintenance table
INSERT INTO EquipmentMaintenance (MaintenanceID, EquipmentID, MaintenanceTime, MaintenanceDetails, MaintenancePersonnel)
VALUES
(1, 101, '2024-01-11 09:00:00', 'Routine inspection and lubrication', 'John Doe'),
(2, 102, '2024-01-21 10:00:00', 'Belt replacement and calibration', 'Jane Smith'),
(3, 103, '2024-02-08 11:00:00', 'Software update and sensor cleaning', 'Mike Johnson'),
(4, 101, '2024-02-21 13:00:00', 'Emergency repair - motor replacement', 'Sarah Brown'),
(5, 102, '2024-03-06 14:00:00', 'Annual comprehensive maintenance', 'Tom Wilson');

-- Insert data into EquipmentFailureAnalysis table
INSERT INTO EquipmentFailureAnalysis (FailureID, EquipmentID, FailureTime, FailureReason, RepairTime)
VALUES
(1, 101, '2024-01-10 15:30:00', 'Worn out belt', 0.5),
(2, 102, '2024-01-20 14:45:00', 'Software glitch', 1.8),
(3, 103, '2024-02-07 16:00:00', 'Sensor malfunction', 1.5),
(4, 101, '2024-02-20 11:30:00', 'Power supply failure', 0.2),
(5, 102, '2024-03-05 13:15:00', 'Mechanical jam', 0.4);

-- Add more data to ProductionProgress table
INSERT INTO ProductionProgress (ProgressID, PlanID, ProcessStep, Status, CompletionTime, ProgressPercentage)
VALUES
(11, 7, 'Assembly', 'In Progress', '2024-04-03 14:00:00', 60.00),
(12, 8, 'Assembly', 'Completed', '2024-04-18 16:30:00', 100.00),
(13, 8, 'Quality Check', 'In Progress', '2024-04-19 10:00:00', 50.00),
(14, 9, 'Assembly', 'Not Started', NULL, 0.00),
(15, 10, 'Assembly', 'Completed', '2024-05-18 15:00:00', 100.00),
(16, 10, 'Quality Check', 'Completed', '2024-05-19 11:30:00', 100.00),
(17, 10, 'Packaging', 'In Progress', '2024-05-20 09:00:00', 80.00),
(18, 11, 'Assembly', 'In Progress', '2024-06-03 14:00:00', 70.00),
(19, 12, 'Assembly', 'Not Started', NULL, 0.00),
(20, 13, 'Assembly', 'Not Started', NULL, 0.00);

-- Add more data to ProductionEfficiency table
INSERT INTO ProductionEfficiency (EfficiencyID, PlanID, Output, EfficiencyRate, ProductionTime)
VALUES
(6, 6, 1190, 99.17, 140.5),
(7, 7, 540, 98.18, 43.2),
(8, 8, 345, 98.57, 37.8),
(9, 9, 1080, 98.18, 130.5),
(10, 10, 575, 99.14, 46.8);

-- Add more data to DefectAnalysis table
INSERT INTO DefectAnalysis (AnalysisID, PlanID, DefectType, DefectCount, AnalysisTime, Cause)
VALUES
(6, 4, 'Scratches', 5, '2024-02-20 16:00:00', 'Rough handling during transportation'),
(7, 5, 'Component failure', 3, '2024-03-05 14:30:00', 'Faulty batch of resistors'),
(8, 6, 'Software glitch', 6, '2024-03-22 15:00:00', 'Outdated firmware version'),
(9, 7, 'Loose connections', 4, '2024-04-05 11:30:00', 'Insufficient tightening during assembly'),
(10, 8, 'Color mismatch', 3, '2024-04-20 13:45:00', 'Inconsistent paint batch');

-- Add more data to RawMaterialInventory table
INSERT INTO RawMaterialInventory (MaterialID, MaterialNumber, MaterialName, Supplier, Quantity, StorageTime, ConsumptionRate)
VALUES
(6, 'RM-006', 'Circuit Boards', 'ElectroTech', 5000, '2024-02-01 09:30:00', 150.75),
(7, 'RM-007', 'Capacitors', 'ComponentCo', 50000, '2024-02-15 11:00:00', 1000.0),
(8, 'RM-008', 'Power Adapters', 'PowerSolutions', 3000, '2024-03-01 13:30:00', 100.0),
(9, 'RM-009', 'Rubber Gaskets', 'SealMasters', 20000, '2024-03-15 15:00:00', 300.5),
(10, 'RM-010', 'LCD Screens', 'DisplayTech', 2000, '2024-04-01 10:30:00', 80.25);

-- Add more data to FinishedGoodsInventory table
INSERT INTO FinishedGoodsInventory (ProductID, ProductNumber, ProductName, Quantity, StorageTime, OutboundTime)
VALUES
(6, 'FG-006', 'Smart Doorbell', 1200, '2024-03-25 14:00:00', '2024-03-30 10:00:00'),
(7, 'FG-007', 'Wireless Earbuds', 3000, '2024-04-10 11:30:00', '2024-04-15 09:30:00'),
(8, 'FG-008', 'Smart Scale', 1800, '2024-04-25 15:00:00', '2024-04-30 14:00:00'),
(9, 'FG-009', 'Air Purifier', 1000, '2024-05-10 16:30:00', '2024-05-15 15:30:00'),
(10, 'FG-010', 'Fitness Tracker', 2500, '2024-05-25 13:45:00', '2024-05-30 12:45:00');

-- Add more data to QualityCheck table
INSERT INTO QualityCheck (CheckID, PlanID, ProcessStep, CheckTime, Passed, DefectType)
VALUES
(11, 4, 'Final Inspection', '2024-02-19 15:00:00', TRUE, NULL),
(12, 5, 'Assembly', '2024-03-03 14:30:00', FALSE, 'Component failure'),
(13, 5, 'Assembly', '2024-03-04 10:00:00', TRUE, NULL),
(14, 5, 'Final Inspection', '2024-03-05 11:30:00', TRUE, NULL),
(15, 6, 'Assembly', '2024-03-19 16:00:00', FALSE, 'Software glitch'),
(16, 6, 'Assembly', '2024-03-20 09:30:00', TRUE, NULL),
(17, 6, 'Final Inspection', '2024-03-21 14:00:00', TRUE, NULL),
(18, 7, 'Assembly', '2024-04-03 15:30:00', FALSE, 'Loose connections'),
(19, 7, 'Assembly', '2024-04-04 10:30:00', TRUE, NULL),
(20, 8, 'Assembly', '2024-04-18 17:00:00', TRUE, NULL);

-- Add more data to EquipmentUsage table
INSERT INTO EquipmentUsage (UsageID, EquipmentID, UsageStartTime, UsageEndTime, Uptime, Downtime)
VALUES
(6, 103, '2024-03-15 08:00:00', '2024-03-22 17:00:00', 140.5, 1.5),
(7, 101, '2024-04-01 08:00:00', '2024-04-05 17:00:00', 43.2, 0.8),
(8, 102, '2024-04-15 08:00:00', '2024-04-20 17:00:00', 37.8, 2.2),
(9, 103, '2024-05-01 08:00:00', '2024-05-08 17:00:00', 130.5, 1.5),
(10, 101, '2024-05-15 08:00:00', '2024-05-20 17:00:00', 46.8, 1.2);

-- Add more data to EquipmentMaintenance table
INSERT INTO EquipmentMaintenance (MaintenanceID, EquipmentID, MaintenanceTime, MaintenanceDetails, MaintenancePersonnel)
VALUES
(6, 103, '2024-03-23 09:30:00', 'Calibration and software update', 'Emily Chen'),
(7, 101, '2024-04-06 10:30:00', 'Lubrication and belt inspection', 'John Doe'),
(8, 102, '2024-04-21 11:30:00', 'Sensor cleaning and alignment', 'Jane Smith'),
(9, 103, '2024-05-09 13:30:00', 'Annual comprehensive maintenance', 'Mike Johnson'),
(10, 101, '2024-05-21 14:30:00', 'Emergency repair - control panel replacement', 'Sarah Brown');

-- Add more data to EquipmentFailureAnalysis table
INSERT INTO EquipmentFailureAnalysis (FailureID, EquipmentID, FailureTime, FailureReason, RepairTime)
VALUES
(6, 103, '2024-03-21 16:30:00', 'Control system malfunction', 1.5),
(7, 101, '2024-04-05 14:00:00', 'Coolant leak', 0.8),
(8, 102, '2024-04-20 15:45:00', 'Electrical short circuit', 2.2),
(9, 103, '2024-05-08 11:00:00', 'Bearing failure', 1.5),
(10, 101, '2024-05-20 10:30:00', 'Control panel malfunction', 1.2);

-- 添加更多 ProductionPlan 数据
INSERT INTO ProductionPlan (PlanID, OrderNumber, ProductModel, PlannedStartTime, PlannedEndTime, Quantity)
VALUES
(31, 'ORD-2024-031', 'Model-A', '2024-07-05 08:00:00', '2024-07-10 17:00:00', 600),
(32, 'ORD-2024-032', 'Model-B', '2024-07-15 08:00:00', '2024-07-20 17:00:00', 450),
(33, 'ORD-2024-033', 'Model-C', '2024-08-01 08:00:00', '2024-08-08 17:00:00', 1100),
(34, 'ORD-2024-034', 'Model-A', '2024-08-15 08:00:00', '2024-08-20 17:00:00', 580),
(35, 'ORD-2024-035', 'Model-B', '2024-09-01 08:00:00', '2024-09-05 17:00:00', 420),
(36, 'ORD-2024-036', 'Model-C', '2024-09-15 08:00:00', '2024-09-22 17:00:00', 1300),
(37, 'ORD-2024-037', 'Model-A', '2024-10-01 08:00:00', '2024-10-05 17:00:00', 550),
(38, 'ORD-2024-038', 'Model-B', '2024-10-15 08:00:00', '2024-10-20 17:00:00', 400),
(39, 'ORD-2024-039', 'Model-C', '2024-11-01 08:00:00', '2024-11-08 17:00:00', 1200),
(40, 'ORD-2024-040', 'Model-A', '2024-11-15 08:00:00', '2024-11-20 17:00:00', 590);

-- 添加更多 ProductionProgress 数据
INSERT INTO ProductionProgress (ProgressID, PlanID, ProcessStep, Status, CompletionTime, ProgressPercentage)
VALUES
(21, 14, 'Assembly', 'Completed', '2024-07-18 16:00:00', 100.00),
(22, 14, 'Quality Check', 'Completed', '2024-07-19 11:30:00', 100.00),
(23, 14, 'Packaging', 'In Progress', '2024-07-20 09:00:00', 85.00),
(24, 15, 'Assembly', 'In Progress', '2024-08-03 14:00:00', 70.00),
(25, 16, 'Assembly', 'Not Started', NULL, 0.00),
(26, 17, 'Assembly', 'Completed', '2024-09-03 15:30:00', 100.00),
(27, 17, 'Quality Check', 'In Progress', '2024-09-04 10:00:00', 60.00),
(28, 18, 'Assembly', 'In Progress', '2024-09-18 14:00:00', 40.00),
(29, 19, 'Assembly', 'Not Started', NULL, 0.00),
(30, 20, 'Assembly', 'Not Started', NULL, 0.00);

-- 添加更多 ProductionEfficiency 数据
INSERT INTO ProductionEfficiency (EfficiencyID, PlanID, Output, EfficiencyRate, ProductionTime)
VALUES
(11, 11, 415, 98.81, 33.2),
(12, 12, 1285, 98.85, 142.5),
(13, 13, 525, 99.06, 41.8),
(14, 14, 375, 98.68, 39.5),
(15, 15, 1140, 99.13, 132.0);

-- 添加更多 DefectAnalysis 数据
INSERT INTO DefectAnalysis (AnalysisID, PlanID, DefectType, DefectCount, AnalysisTime, Cause)
VALUES
(11, 9, 'Packaging damage', 6, '2024-05-08 15:30:00', 'Faulty packaging machine'),
(12, 10, 'Software glitch', 4, '2024-05-20 14:00:00', 'Incompatible firmware version'),
(13, 11, 'Component failure', 3, '2024-06-05 16:15:00', 'Substandard capacitor batch'),
(14, 12, 'Scratches', 8, '2024-06-22 11:30:00', 'Rough handling during assembly'),
(15, 13, 'Color mismatch', 3, '2024-07-05 13:45:00', 'Incorrect paint mixture ratio');

-- 添加更多 RawMaterialInventory 数据
INSERT INTO RawMaterialInventory (MaterialID, MaterialNumber, MaterialName, Supplier, Quantity, StorageTime, ConsumptionRate)
VALUES
(11, 'RM-011', 'Microcontrollers', 'ChipMakers', 10000, '2024-04-15 09:30:00', 200.5),
(12, 'RM-012', 'Thermal Paste', 'CoolTech', 5000, '2024-05-01 11:00:00', 50.0),
(13, 'RM-013', 'HDMI Cables', 'ConnectPro', 8000, '2024-05-15 13:30:00', 150.75),
(14, 'RM-014', 'Cooling Fans', 'AirFlow Inc', 3000, '2024-06-01 15:00:00', 100.25),
(15, 'RM-015', 'Lithium Batteries', 'PowerCell', 15000, '2024-06-15 10:30:00', 300.0);

-- 添加更多 FinishedGoodsInventory 数据
INSERT INTO FinishedGoodsInventory (ProductID, ProductNumber, ProductName, Quantity, StorageTime, OutboundTime)
VALUES
(11, 'FG-011', 'Smart Power Strip', 2000, '2024-06-10 14:00:00', '2024-06-15 10:00:00'),
(12, 'FG-012', 'Bluetooth Speaker', 3500, '2024-06-25 11:30:00', '2024-06-30 09:30:00'),
(13, 'FG-013', 'Wi-Fi Extender', 1500, '2024-07-10 15:00:00', '2024-07-15 14:00:00'),
(14, 'FG-014', 'Smart Smoke Detector', 2200, '2024-07-25 16:30:00', '2024-07-30 15:30:00'),
(15, 'FG-015', 'Robot Lawn Mower', 800, '2024-08-10 13:45:00', '2024-08-15 12:45:00');

-- 添加更多 QualityCheck 数据
INSERT INTO QualityCheck (CheckID, PlanID, ProcessStep, CheckTime, Passed, DefectType)
VALUES
(21, 9, 'Assembly', '2024-05-05 14:30:00', TRUE, NULL),
(22, 9, 'Final Inspection', '2024-05-07 16:00:00', FALSE, 'Packaging damage'),
(23, 9, 'Final Inspection', '2024-05-08 10:30:00', TRUE, NULL),
(24, 10, 'Assembly', '2024-05-18 15:00:00', FALSE, 'Software glitch'),
(25, 10, 'Assembly', '2024-05-19 09:30:00', TRUE, NULL),
(26, 10, 'Final Inspection', '2024-05-20 11:00:00', TRUE, NULL),
(27, 11, 'Assembly', '2024-06-03 14:30:00', FALSE, 'Component failure'),
(28, 11, 'Assembly', '2024-06-04 10:00:00', TRUE, NULL),
(29, 11, 'Final Inspection', '2024-06-05 15:30:00', TRUE, NULL),
(30, 12, 'Assembly', '2024-06-20 16:00:00', FALSE, 'Scratches');

-- 添加更多 EquipmentUsage 数据
INSERT INTO EquipmentUsage (UsageID, EquipmentID, UsageStartTime, UsageEndTime, Uptime, Downtime)
VALUES
(11, 102, '2024-06-01 08:00:00', '2024-06-05 17:00:00', 33.2, 6.8),
(12, 103, '2024-06-15 08:00:00', '2024-06-22 17:00:00', 142.5, 1.5),
(13, 101, '2024-07-01 08:00:00', '2024-07-05 17:00:00', 41.8, 2.2),
(14, 102, '2024-07-15 08:00:00', '2024-07-20 17:00:00', 39.5, 4.5),
(15, 103, '2024-08-01 08:00:00', '2024-08-08 17:00:00', 132.0, 4.0);

-- 添加更多 EquipmentMaintenance 数据
INSERT INTO EquipmentMaintenance (MaintenanceID, EquipmentID, MaintenanceTime, MaintenanceDetails, MaintenancePersonnel)
VALUES
(11, 102, '2024-06-06 09:00:00', 'Lubrication and belt replacement', 'Tom Wilson'),
(12, 103, '2024-06-23 10:00:00', 'Software update and calibration', 'Emily Chen'),
(13, 101, '2024-07-06 11:00:00', 'Sensor cleaning and alignment', 'John Doe'),
(14, 102, '2024-07-21 13:00:00', 'Emergency repair - motor replacement', 'Jane Smith'),
(15, 103, '2024-08-09 14:00:00', 'Annual comprehensive maintenance', 'Mike Johnson');

-- 添加更多 EquipmentFailureAnalysis 数据
INSERT INTO EquipmentFailureAnalysis (FailureID, EquipmentID, FailureTime, FailureReason, RepairTime)
VALUES
(11, 102, '2024-06-05 15:30:00', 'Belt snapped', 6.8),
(12, 103, '2024-06-22 16:45:00', 'Software crash', 1.5),
(13, 101, '2024-07-05 14:15:00', 'Sensor misalignment', 2.2),
(14, 102, '2024-07-20 11:00:00', 'Motor burnout', 4.5),
(15, 103, '2024-08-08 13:30:00', 'Control panel malfunction', 4.0);