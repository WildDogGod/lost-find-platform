package com.zzhx.lostfound.model.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

/**
 * 分类实体
 */
@Data
@TableName("category")
public class Category {

    /** 主键 ID */
    @TableId(type = IdType.AUTO)
    private Long id;

    /** 分类名称 */
    private String name;

    /** 图标标识 */
    private String icon;

    /** 排序值，越小越靠前 */
    private Integer sort;
}
