package com.zzhx.lostfound.system.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.zzhx.lostfound.model.entity.Category;

import java.util.List;

/**
 * 分类 Service
 */
public interface CategoryService extends IService<Category> {

    /** 查询全部分类（按 sort 升序） */
    List<Category> listAll();
}
