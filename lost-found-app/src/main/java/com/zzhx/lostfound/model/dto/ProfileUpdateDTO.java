package com.zzhx.lostfound.model.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * 个人信息修改请求。
 *
 * <p>只允许修改这些展示字段；role、status、verifyStatus、username 等
 * 安全相关字段一律不允许由客户端提交。</p>
 */
@Data
public class ProfileUpdateDTO {

    /** 真实姓名 */
    @Size(max = 50, message = "真实姓名不能超过 50 个字符")
    private String realName;

    /** 手机号 */
    @Size(max = 20, message = "手机号不能超过 20 个字符")
    private String phone;

    /** 邮箱 */
    @Email(message = "邮箱格式不正确")
    @Size(max = 100, message = "邮箱不能超过 100 个字符")
    private String email;

    /** 头像地址 */
    @Size(max = 255, message = "头像地址过长")
    private String avatar;
}
