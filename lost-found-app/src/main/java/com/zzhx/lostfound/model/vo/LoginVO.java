package com.zzhx.lostfound.model.vo;

import lombok.Data;

/**
 * 登录响应
 */
@Data
public class LoginVO {

    /** 登录令牌 JWT，后续请求放在 Authorization 头 */
    private String token;

    /** 当前登录用户信息 */
    private UserVO userInfo;
}
