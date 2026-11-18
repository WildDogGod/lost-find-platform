package com.zzhx.lostfound.model.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 发布物品请求
 */
@Data
public class ItemDTO {

    /** 类型：LOST 失物 / FOUND 招领 */
    @NotBlank(message = "物品类型不能为空")
    private String type;

    /** 物品标题 */
    @NotBlank(message = "物品标题不能为空")
    private String title;

    /** 分类 ID */
    @NotNull(message = "物品分类不能为空")
    private Long categoryId;

    /** 详细描述 */
    @NotBlank(message = "详细描述不能为空")
    private String description;

    /** 图片地址，多个用逗号分隔 */
    private String images;

    /** 丢失 / 拾取时间 */
    @NotNull(message = "丢失/拾取时间不能为空")
    private LocalDateTime eventTime;

    /** 丢失 / 拾取地点 */
    @NotBlank(message = "地点不能为空")
    private String location;

    /** 隐藏特征（招领用于核验） */
    private String secretFeature;

    /** 联系人 */
    @NotBlank(message = "联系人不能为空")
    private String contactName;

    /** 联系电话 */
    @NotBlank(message = "联系电话不能为空")
    private String contactPhone;
}
