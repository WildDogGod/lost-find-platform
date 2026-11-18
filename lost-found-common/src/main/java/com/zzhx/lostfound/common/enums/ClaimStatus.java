package com.zzhx.lostfound.common.enums;

import lombok.Getter;

/**
 * 认领状态
 */
@Getter
public enum ClaimStatus {

    PENDING("待审核"),
    APPROVED("已通过"),
    REJECTED("已驳回");

    private final String desc;

    ClaimStatus(String desc) {
        this.desc = desc;
    }
}
