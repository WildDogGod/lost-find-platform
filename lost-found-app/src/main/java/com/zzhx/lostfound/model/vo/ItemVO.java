package com.zzhx.lostfound.model.vo;

import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 物品详情响应
 */
@Data
public class ItemVO {

    /** 主键 ID */
    private Long id;

    /** 类型：LOST 失物 / FOUND 招领 */
    private String type;

    /** 物品标题 */
    private String title;

    /** 分类 ID */
    private Long categoryId;

    /** 分类名称 */
    private String categoryName;

    /** 详细描述 */
    private String description;

    /** 图片地址列表 */
    private List<String> images;

    /** 丢失 / 拾取时间 */
    private LocalDateTime eventTime;

    /** 丢失 / 拾取地点 */
    private String location;

    /** 联系人 */
    private String contactName;

    /** 联系电话 */
    private String contactPhone;

    /** 状态 */
    private String status;

    /** 用户 ID */
    private Long userId;

    /** 发布者名称 */
    private String publisherName;

    /** 创建时间 */
    private LocalDateTime createTime;
}
