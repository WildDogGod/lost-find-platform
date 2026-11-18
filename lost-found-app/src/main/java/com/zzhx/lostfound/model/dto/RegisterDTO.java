package com.zzhx.lostfound.model.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * 注册请求
 */
@Data
public class RegisterDTO {

    /** 登录账号（唯一） */
    @NotBlank(message = "账号不能为空")
    @Size(min = 4, max = 20, message = "账号长度需在 4-20 位之间")
    private String username;

    /** 登录密码 */
    @NotBlank(message = "密码不能为空")
    @Size(min = 6, max = 20, message = "密码长度需在 6-20 位之间")
    private String password;

    /** 真实姓名 */
    @NotBlank(message = "真实姓名不能为空")
    private String realName;

    /** 学号 */
    private String studentNo;

    /** 手机号 */
    private String phone;
}
