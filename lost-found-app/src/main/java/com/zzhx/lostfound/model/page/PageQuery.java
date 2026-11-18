package com.zzhx.lostfound.model.page;

import lombok.Data;

/**
 * 分页查询基础参数
 */
@Data
public class PageQuery {

    private Long current = 1L;

    private Long size = 10L;
}
