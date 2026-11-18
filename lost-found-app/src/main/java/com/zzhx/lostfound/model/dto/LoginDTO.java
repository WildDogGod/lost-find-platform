package com.zzhx.lostfound.model.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * 登录请求
 */
@Data
public class LoginDTO {

    /** 登录账号 */
    @NotBlank(message = "账号不能为空")
    private String username;

    /** 登录密码，明文传输后由后端与哈希比对 */
    @NotBlank(message = "密码不能为空")
    private String password;
}
