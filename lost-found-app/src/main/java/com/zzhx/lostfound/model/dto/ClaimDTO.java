package com.zzhx.lostfound.model.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

/**
 * 认领申请请求
 */
@Data
public class ClaimDTO {

    /** 要认领的物品 ID */
    @NotNull(message = "物品 ID 不能为空")
    private Long itemId;

    /** 认领凭证描述，如物品特征、丢失时间 */
    @NotBlank(message = "请描述物品特征凭证")
    private String claimDesc;
}
