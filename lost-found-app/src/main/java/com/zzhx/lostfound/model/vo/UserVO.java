package com.zzhx.lostfound.model.vo;

import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.zzhx.lostfound.support.NullToEmptyStringSerializer;
import lombok.Data;

/**
 * 用户信息响应
 */
@Data
public class UserVO {

    /** 主键 ID */
    private Long id;

    /** 登录账号（唯一） */
    private String username;

    /** 真实姓名 */
    private String realName;

    /** 学号 */
    private String studentNo;

    /** 学院 */
    private String college;

    /** 手机号 */
    private String phone;

    /** 邮箱 */
    private String email;

    /** 头像地址：数据库可空，但接口契约要求始终返回字符串 */
    @JsonSerialize(nullsUsing = NullToEmptyStringSerializer.class)
    private String avatar;

    /** 实名认证状态：0 未认证，1 已认证 */
    private Integer verifyStatus;

    /** 角色：USER / ADMIN */
    private String role;
}
