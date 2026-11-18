package com.zzhx.lostfound.model.vo;

import lombok.Data;

import java.time.LocalDateTime;

/**
 * 认领记录响应
 */
@Data
public class ClaimVO {

    /** 认领记录 ID */
    private Long id;

    /** 物品 ID */
    private Long itemId;

    /** 申请人 ID */
    private Long applicantId;

    /** 申请人姓名 */
    private String applicantName;

    /** 认领凭证描述 */
    private String claimDesc;

    /** 认领状态：PENDING / APPROVED / REJECTED */
    private String status;

    /** 审核备注 */
    private String reviewRemark;

    /** 创建时间 */
    private LocalDateTime createTime;
}
