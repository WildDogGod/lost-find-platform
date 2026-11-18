package com.zzhx.lostfound.common.constant;

/**
 * 系统常量
 */
public interface Constants {

    /** 请求头中的 token 标识 */
    String TOKEN_HEADER = "Authorization";

    /** token 前缀 */
    String TOKEN_PREFIX = "Bearer ";

    /** 默认分页大小 */
    long DEFAULT_PAGE_SIZE = 10L;

    /** 系统消息发送者 ID */
    long SYSTEM_USER_ID = 0L;

    /** 用户角色：普通用户 */
    String ROLE_USER = "USER";

    /** 用户角色：管理员 */
    String ROLE_ADMIN = "ADMIN";
}
