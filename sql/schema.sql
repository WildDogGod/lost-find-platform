-- ============================================================
-- 校园失物招领平台 建库建表脚本
-- ============================================================

CREATE DATABASE IF NOT EXISTS lost_found
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE lost_found;

DROP TABLE IF EXISTS favorite;
DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS claim;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS `user`;

-- 用户表
CREATE TABLE `user` (
    id            BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    username      VARCHAR(50)  NOT NULL COMMENT '登录账号',
    password      VARCHAR(100) NOT NULL COMMENT '加密密码',
    real_name     VARCHAR(50)  COMMENT '真实姓名',
    student_no    VARCHAR(20)  COMMENT '学号',
    college       VARCHAR(100) COMMENT '学院',
    phone         VARCHAR(20)  COMMENT '手机号',
    email         VARCHAR(100) COMMENT '邮箱',
    avatar        VARCHAR(255) COMMENT '头像地址',
    verify_status TINYINT      DEFAULT 0 COMMENT '认证状态：0未认证 1已认证',
    role          VARCHAR(20)  DEFAULT 'USER' COMMENT '角色：USER/ADMIN',
    status        TINYINT      DEFAULT 0 COMMENT '状态：0正常 1封禁',
    create_time   DATETIME COMMENT '创建时间',
    update_time   DATETIME COMMENT '更新时间',
    UNIQUE KEY uk_username (username)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT '用户表';

-- 分类表
CREATE TABLE category (
    id    BIGINT PRIMARY KEY AUTO_INCREMENT,
    name  VARCHAR(50)  NOT NULL COMMENT '分类名称',
    icon  VARCHAR(255) COMMENT '图标',
    sort  INT          DEFAULT 0 COMMENT '排序'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT '分类表';

-- 物品表
CREATE TABLE item (
    id             BIGINT PRIMARY KEY AUTO_INCREMENT,
    type           VARCHAR(10)  NOT NULL COMMENT 'LOST失物/FOUND招领',
    title          VARCHAR(100) NOT NULL COMMENT '物品标题',
    category_id    BIGINT       COMMENT '分类ID',
    description    TEXT         COMMENT '详细描述',
    images         VARCHAR(1000) COMMENT '图片地址，多个逗号分隔',
    event_time     DATETIME     COMMENT '丢失/拾取时间',
    location       VARCHAR(100) COMMENT '地点',
    secret_feature VARCHAR(255) COMMENT '隐藏特征（招领核验，不公开）',
    contact_name   VARCHAR(50)  COMMENT '联系人',
    contact_phone  VARCHAR(20)  COMMENT '联系电话',
    status         VARCHAR(20)  DEFAULT 'PENDING' COMMENT 'PENDING/ACTIVE/PROCESSING/COMPLETED/CLOSED',
    audit_remark   VARCHAR(255) COMMENT '审核备注',
    user_id        BIGINT       COMMENT '发布者ID',
    create_time    DATETIME     COMMENT '创建时间',
    update_time    DATETIME     COMMENT '更新时间'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT '物品表';

-- 认领记录表
CREATE TABLE claim (
    id            BIGINT PRIMARY KEY AUTO_INCREMENT,
    item_id       BIGINT       COMMENT '物品ID',
    applicant_id  BIGINT       COMMENT '申请人ID',
    claim_desc    VARCHAR(500) COMMENT '认领凭证描述',
    status        VARCHAR(20)  DEFAULT 'PENDING' COMMENT 'PENDING/APPROVED/REJECTED',
    review_remark VARCHAR(255) COMMENT '审核备注',
    reviewer_id   BIGINT       COMMENT '审核人ID',
    create_time   DATETIME     COMMENT '申请时间',
    review_time   DATETIME     COMMENT '审核时间'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT '认领记录表';

-- 消息表
CREATE TABLE message (
    id           BIGINT PRIMARY KEY AUTO_INCREMENT,
    from_user_id BIGINT       COMMENT '发送者ID（系统为0）',
    to_user_id   BIGINT       COMMENT '接收者ID',
    item_id      BIGINT       COMMENT '关联物品ID',
    type         VARCHAR(20)  COMMENT 'SYSTEM/CLAIM/CHAT',
    content      VARCHAR(500) COMMENT '消息内容',
    is_read      TINYINT      DEFAULT 0 COMMENT '是否已读：0否 1是',
    create_time  DATETIME     COMMENT '创建时间'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT '消息表';

-- 收藏表
CREATE TABLE favorite (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id     BIGINT COMMENT '用户ID',
    item_id     BIGINT COMMENT '物品ID',
    create_time DATETIME COMMENT '收藏时间',
    UNIQUE KEY uk_user_item (user_id, item_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT '收藏表';

-- 初始化分类数据
INSERT INTO category (name, icon, sort) VALUES
    ('证件卡片', 'card',  1),
    ('钥匙',     'key',   2),
    ('电子设备', 'phone', 3),
    ('书籍文具', 'book',  4),
    ('其他',     'more',  5);
