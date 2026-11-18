package com.zzhx.lostfound.model.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.zzhx.lostfound.support.NullToEmptyStringSerializer;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 用户实体
 */
@Data
@TableName("user")
public class User {

    /** 主键 ID */
    @TableId(type = IdType.AUTO)
    private Long id;

    /** 登录账号（唯一） */
    private String username;

    /** BCrypt 加密后的密码，不返回给前端 */
    @JsonIgnore
    private String password;

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

    /** 角色：USER 普通用户 / ADMIN 管理员 */
    private String role;

    /** 账号状态：0 正常，1 封禁 */
    private Integer status;

    /** 创建时间 */
    private LocalDateTime createTime;

    /** 更新时间 */
    private LocalDateTime updateTime;
}
