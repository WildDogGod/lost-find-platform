package com.zzhx.lostfound.admin.exception;

import com.zzhx.lostfound.common.exception.BusinessException;
import com.zzhx.lostfound.common.result.Result;
import com.zzhx.lostfound.common.result.ResultCode;
import jakarta.validation.ConstraintViolationException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.validation.BindException;
import org.springframework.validation.FieldError;
import org.springframework.web.HttpMediaTypeNotSupportedException;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * 全局异常处理
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public Result<Void> handleBusinessException(BusinessException e) {
        log.warn("业务异常：{}", e.getMessage());
        return Result.error(e.getCode(), e.getMessage());
    }

    /**
     * @RequestBody 参数校验失败，返回 400 与首个字段错误提示
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Result<Void> handleMethodArgumentNotValid(MethodArgumentNotValidException e) {
        FieldError fieldError = e.getBindingResult().getFieldError();
        String message = fieldError != null ? fieldError.getDefaultMessage() : ResultCode.PARAM_ERROR.getMessage();
        return Result.error(ResultCode.PARAM_ERROR.getCode(), message);
    }

    /**
     * 表单或查询参数绑定失败，返回 400
     */
    @ExceptionHandler(BindException.class)
    public Result<Void> handleBindException(BindException e) {
        FieldError fieldError = e.getBindingResult().getFieldError();
        String message = fieldError != null ? fieldError.getDefaultMessage() : ResultCode.PARAM_ERROR.getMessage();
        return Result.error(ResultCode.PARAM_ERROR.getCode(), message);
    }

    /**
     * 路径、参数上的约束校验失败，返回 400
     */
    @ExceptionHandler(ConstraintViolationException.class)
    public Result<Void> handleConstraintViolation(ConstraintViolationException e) {
        return Result.error(ResultCode.PARAM_ERROR.getCode(), e.getMessage());
    }

    /** 请求体缺失或 JSON 格式错误（如没选 JSON、Body 为空、括号不配对） */
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public Result<Void> handleHttpMessageNotReadable(HttpMessageNotReadableException e) {
        log.warn("请求体解析失败：{}", e.getMessage());
        return Result.error(ResultCode.PARAM_ERROR.getCode(),
                "请求体缺失或不是合法 JSON，请在 Body 中选择 JSON 并填写正确的 JSON 数据");
    }

    /** Content-Type 不支持，如 @RequestBody 接口用了 form-data */
    @ExceptionHandler(HttpMediaTypeNotSupportedException.class)
    public Result<Void> handleHttpMediaTypeNotSupported(HttpMediaTypeNotSupportedException e) {
        log.warn("请求类型不支持：{}", e.getMessage());
        return Result.error(ResultCode.PARAM_ERROR.getCode(),
                "请求类型不支持，请设置请求头 Content-Type: application/json");
    }

    /** 请求方法不支持，如接口要求 POST 却用了 GET */
    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    public Result<Void> handleMethodNotSupported(HttpRequestMethodNotSupportedException e) {
        log.warn("请求方法不支持：{}", e.getMessage());
        return Result.error(ResultCode.PARAM_ERROR.getCode(),
                "请求方法不支持：" + e.getMethod());
    }

    /** 缺少必需的请求参数 */
    @ExceptionHandler(MissingServletRequestParameterException.class)
    public Result<Void> handleMissingParam(MissingServletRequestParameterException e) {
        return Result.error(ResultCode.PARAM_ERROR.getCode(),
                "缺少必需参数：" + e.getParameterName());
    }

    /**
     * 兜底异常处理：记录日志并返回 500，避免向前端暴露堆栈
     */
    @ExceptionHandler(Exception.class)
    public Result<Void> handleException(Exception e) {
        log.error("系统异常：", e);
        return Result.error(ResultCode.ERROR);
    }
}
