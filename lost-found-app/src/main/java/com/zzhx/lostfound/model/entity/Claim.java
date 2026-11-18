package com.zzhx.lostfound.model.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 认领记录实体
 */
@Data
@TableName("claim")
public class Claim {

    /** 主键 ID */
    @TableId(type = IdType.AUTO)
    private Long id;

    /** 物品 ID */
    private Long itemId;

    /** 申请人 ID */
    private Long applicantId;

    /** 认领凭证描述 */
    private String claimDesc;

    /** PENDING / APPROVED / REJECTED */
    private String status;

    /** 审核备注 */
    private String reviewRemark;

    /** 审核人 ID */
    private Long reviewerId;

    /** 创建时间 */
    private LocalDateTime createTime;

    /** 审核时间 */
    private LocalDateTime reviewTime;
}
