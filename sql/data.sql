-- ============================================================
-- 校园失物招领平台 测试数据脚本
-- 库：lost_found
-- 说明：建议在干净的测试库执行；如需重复执行，可先放开下面的清理语句
-- ============================================================

USE lost_found;
SET NAMES utf8mb4;

-- ---------- 可选：清理旧测试数据（会清空物品/认领/消息/收藏，谨慎使用）----------
-- DELETE FROM favorite;
-- DELETE FROM message;
-- DELETE FROM claim;
-- DELETE FROM item;
-- DELETE FROM `user` WHERE id BETWEEN 1 AND 5;

-- ============================================================
-- 一、用户：1 个管理员 + 4 个学生
-- 管理员 admin / admin123；学生密码均为 123456（BCrypt 加密）
-- ============================================================
INSERT INTO `user` (id, username, password, real_name, student_no, college, phone, email, avatar, verify_status, role, status, create_time, update_time) VALUES
(1, 'admin',    '$2a$10$u98FK30Qi.AjAkhwNQQnvudGubENOQ/K2QNjTgXRQmU4rYk2shdJ.', '系统管理员', NULL,        '信息科学与工程学院', '13800000000', 'admin@campus.edu',    NULL, 1, 'ADMIN', 0, NOW(), NOW()),
(2, 'zhangsan', '$2a$10$ymi/5o3hNGtfGRh8yCngmuXGMaOX6GI.V1ulGdya1Dz6dXZyQdZBu', '张三', '2022010101', '信息科学与工程学院', '13800001111', 'zhangsan@campus.edu', NULL, 1, 'USER',  0, NOW(), NOW()),
(3, 'lisi',     '$2a$10$ymi/5o3hNGtfGRh8yCngmuXGMaOX6GI.V1ulGdya1Dz6dXZyQdZBu', '李四', '2022010202', '机械工程学院',       '13800002222', 'lisi@campus.edu',     NULL, 1, 'USER',  0, NOW(), NOW()),
(4, 'wangwu',   '$2a$10$ymi/5o3hNGtfGRh8yCngmuXGMaOX6GI.V1ulGdya1Dz6dXZyQdZBu', '王五', '2022010303', '经济管理学院',       '13800003333', 'wangwu@campus.edu',   NULL, 0, 'USER',  0, NOW(), NOW()),
(5, 'zhaoliu',  '$2a$10$ymi/5o3hNGtfGRh8yCngmuXGMaOX6GI.V1ulGdya1Dz6dXZyQdZBu', '赵六', '2022010404', '外国语学院',         '13800004444', 'zhaoliu@campus.edu',  NULL, 1, 'USER',  0, NOW(), NOW());

-- ============================================================
-- 二、物品：4 条失物 + 4 条招领，覆盖不同分类与状态
-- 分类：1证件卡片 2钥匙 3电子设备 4书籍文具 5其他
-- ============================================================
INSERT INTO item (id, type, title, category_id, description, images, event_time, location, secret_feature, contact_name, contact_phone, status, audit_remark, user_id, create_time, update_time) VALUES
-- 失物 LOST
(1, 'LOST', '黑色钱包（内有校园卡）', 1, '今天下午在校园内丢失一个黑色皮质钱包，内有本人校园卡和少量现金，拾到者请联系，必有酬谢。', NULL, DATE_SUB(NOW(), INTERVAL 1 DAY),  '一食堂',   NULL, '张三', '13800001111', 'PENDING',    NULL,                 2, NOW(), NOW()),
(2, 'LOST', '一串钥匙（带蓝色挂件）', 2, '丢失一串钥匙，约 3 把，挂着一个蓝色小熊挂件，可能在篮球场附近。',                       NULL, DATE_SUB(NOW(), INTERVAL 2 DAY),  '篮球场',   NULL, '李四', '13800002222', 'ACTIVE',     '信息完整，同意发布', 3, NOW(), NOW()),
(3, 'LOST', 'iPhone 15 黑色 256G',   3, '昨晚在图书馆自习后遗失一部黑色 iPhone 15，256G，黑色手机壳，锁屏为风景照。',           NULL, DATE_SUB(NOW(), INTERVAL 3 DAY),  '图书馆',   NULL, '王五', '13800003333', 'PROCESSING', '信息完整，同意发布', 4, NOW(), NOW()),
(4, 'LOST', '高等数学教材（第七版）', 4, '丢失一本《高等数学》上册（同济大学第七版），扉页有名字，对我很重要。',                  NULL, DATE_SUB(NOW(), INTERVAL 4 DAY),  '教学楼A',  NULL, '赵六', '13800004444', 'ACTIVE',     '信息完整，同意发布', 5, NOW(), NOW()),
-- 招领 FOUND
(5, 'FOUND', '图书馆捡到一张身份证', 1, '在图书馆三楼自习区捡到一张身份证，已交由服务台，失主请联系核对信息。',                  NULL, DATE_SUB(NOW(), INTERVAL 2 DAY),  '图书馆',   '身份证背面有轻微划痕', '张三', '13800001111', 'ACTIVE',     '信息完整，同意发布', 2, NOW(), NOW()),
(6, 'FOUND', '食堂捡到一串钥匙',     2, '中午在二食堂捡到一串钥匙，共 4 把，带一个金属牌，请失主描述钥匙特征认领。',            NULL, DATE_SUB(NOW(), INTERVAL 1 DAY),  '二食堂',   '金属牌上刻有数字 8',  '李四', '13800002222', 'ACTIVE',     '信息完整，同意发布', 3, NOW(), NOW()),
(7, 'FOUND', '操场捡到 AirPods 耳机', 3, '在操场看台捡到一副白色 AirPods（第三代），已确认并归还失主。',                          NULL, DATE_SUB(NOW(), INTERVAL 5 DAY),  '操场',     '充电盒背面有刻字',    '王五', '13800003333', 'COMPLETED',  '信息完整，同意发布', 4, NOW(), NOW()),
(8, 'FOUND', '二教捡到黑色保温杯',   5, '在第二教学楼 203 教室捡到一个黑色保温杯，杯底有贴纸，失主请联系。',                    NULL, DATE_SUB(NOW(), INTERVAL 1 DAY),  '二教203',  '杯底贴有卡通贴纸',    '赵六', '13800004444', 'ACTIVE',     '信息完整，同意发布', 5, NOW(), NOW());

-- ============================================================
-- 三、认领记录：待审核 / 已通过 / 已驳回
-- ============================================================
INSERT INTO claim (id, item_id, applicant_id, claim_desc, status, review_remark, reviewer_id, create_time, review_time) VALUES
(1, 3, 5, '该手机是我在图书馆遗失的，黑色 256G，锁屏是海边风景照，手机壳内有一张公交卡。', 'PENDING',  NULL,                 NULL, NOW(), NULL),
(2, 7, 2, '我在操场丢失的 AirPods，充电盒背面刻有我的名字缩写 ZS。',                       'APPROVED', '特征核对一致，同意认领', 1, NOW(), NOW()),
(3, 5, 4, '身份证应该是我的，姓名王某。',                                                    'REJECTED', '身份证信息与申请人不符', 1, NOW(), NOW());

-- ============================================================
-- 四、消息：系统通知 + 一条聊天
-- ============================================================
INSERT INTO message (id, from_user_id, to_user_id, item_id, type, content, is_read, create_time) VALUES
(1, 0, 4, 3, 'SYSTEM', '您发布的「iPhone 15 黑色 256G」收到一条新的认领申请，请及时处理。', 0, NOW()),
(2, 0, 2, 7, 'SYSTEM', '您对「操场捡到 AirPods 耳机」的认领申请已通过，请联系发布者领取。', 1, NOW()),
(3, 0, 4, 5, 'SYSTEM', '您对「图书馆捡到一张身份证」的认领申请未通过，原因：身份证信息与申请人不符。', 1, NOW()),
(4, 5, 4, 3, 'CHAT',   '你好，我看到你发布的 iPhone 招领信息，想再确认一下丢失时间。',         0, NOW());

-- ============================================================
-- 五、收藏
-- ============================================================
INSERT INTO favorite (id, user_id, item_id, create_time) VALUES
(1, 2, 3, NOW()),
(2, 2, 7, NOW()),
(3, 5, 6, NOW()),
(4, 3, 1, NOW());
