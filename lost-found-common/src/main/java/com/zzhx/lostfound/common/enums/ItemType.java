package com.zzhx.lostfound.common.enums;

import lombok.Getter;

/**
 * 物品类型
 */
@Getter
public enum ItemType {

    LOST("失物"),
    FOUND("招领");

    private final String desc;

    ItemType(String desc) {
        this.desc = desc;
    }
}
