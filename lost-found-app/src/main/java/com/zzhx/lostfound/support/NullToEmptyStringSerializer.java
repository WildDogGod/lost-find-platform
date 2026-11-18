package com.zzhx.lostfound.support;

import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.SerializerProvider;

import java.io.IOException;

/**
 * null 值序列化器：把 {@code null} 输出成空串。
 * <p>
 * 配合 {@code @JsonSerialize(nullsUsing = NullToEmptyStringSerializer.class)} 使用，
 * 用于那些数据库可空、但接口契约要求必须是字符串的字段（如 avatar），
 * 避免响应里出现 {@code null} 导致契约校验失败。
 */
public class NullToEmptyStringSerializer extends JsonSerializer<Object> {

    /**
     * 序列化时把 null 转成空字符串，避免前端拿到 null 后判空出错
     */
    @Override
    public void serialize(Object value, JsonGenerator gen, SerializerProvider serializers) throws IOException {
        gen.writeString(value == null ? "" : String.valueOf(value));
    }
}
