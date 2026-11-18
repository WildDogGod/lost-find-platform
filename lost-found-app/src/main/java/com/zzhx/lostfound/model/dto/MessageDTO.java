package com.zzhx.lostfound.model.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

/**
 * 发送留言请求
 */
@Data
public class MessageDTO {

    /** 接收者 ID */
    @NotNull(message = "接收者不能为空")
    private Long toUserId;

    /** 关联物品 ID */
    private Long itemId;

    /** 消息内容 */
    @NotBlank(message = "留言内容不能为空")
    private String content;
}
