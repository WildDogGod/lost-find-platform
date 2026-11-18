package com.zzhx.lostfound.model.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 物品实体（失物 / 招领）
 */
@Data
@TableName("item")
public class Item {

    /** 主键 ID */
    @TableId(type = IdType.AUTO)
    private Long id;

    /** LOST 失物 / FOUND 招领 */
    private String type;

    /** 物品标题 */
    private String title;

    /** 分类 ID */
    private Long categoryId;

    /** 详细描述 */
    private String description;

    /** 图片地址，多个逗号分隔 */
    private String images;

    /** 丢失 / 拾取时间 */
    private LocalDateTime eventTime;

    /** 丢失 / 拾取地点 */
    private String location;

    /** 隐藏特征，用于认领核验，不对外公开 */
    @JsonIgnore
    private String secretFeature;

    /** 联系人 */
    private String contactName;

    /** 联系电话 */
    private String contactPhone;

    /** PENDING / ACTIVE / PROCESSING / COMPLETED / CLOSED */
    private String status;

    /** 管理员审核备注 */
    private String auditRemark;

    /** 发布者 ID */
    private Long userId;

    /** 创建时间 */
    private LocalDateTime createTime;

    /** 更新时间 */
    private LocalDateTime updateTime;
}
