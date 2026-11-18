package com.zzhx.lostfound.common.enums;

import lombok.Getter;

/**
 * 物品状态
 */
@Getter
public enum ItemStatus {

    PENDING("待审核"),
    ACTIVE("进行中"),
    PROCESSING("认领中"),
    COMPLETED("已完成"),
    CLOSED("已关闭");

    private final String desc;

    ItemStatus(String desc) {
        this.desc = desc;
    }
}
