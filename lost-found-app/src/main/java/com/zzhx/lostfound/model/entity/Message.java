package com.zzhx.lostfound.model.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 消息实体
 */
@Data
@TableName("message")
public class Message {

    /** 主键 ID */
    @TableId(type = IdType.AUTO)
    private Long id;

    /** 发送者 ID，系统消息固定为 0 */
    private Long fromUserId;

    /** 接收者 ID */
    private Long toUserId;

    /** 物品 ID */
    private Long itemId;

    /** SYSTEM / CLAIM / CHAT */
    private String type;

    /** 消息内容 */
    private String content;

    /** 是否已读：0 未读，1 已读 */
    private Integer isRead;

    /** 创建时间 */
    private LocalDateTime createTime;
}
