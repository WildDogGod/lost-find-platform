package com.zzhx.lostfound.model.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 收藏实体
 */
@Data
@TableName("favorite")
public class Favorite {

    /** 主键 ID */
    @TableId(type = IdType.AUTO)
    private Long id;

    /** 收藏人 ID */
    private Long userId;

    /** 被收藏的物品 ID */
    private Long itemId;

    /** 创建时间 */
    private LocalDateTime createTime;
}
