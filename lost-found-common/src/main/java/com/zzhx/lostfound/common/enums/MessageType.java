package com.zzhx.lostfound.common.enums;

import lombok.Getter;

/**
 * 消息类型
 */
@Getter
public enum MessageType {

    SYSTEM("系统"),
    CLAIM("认领"),
    CHAT("留言");

    private final String desc;

    MessageType(String desc) {
        this.desc = desc;
    }
}
