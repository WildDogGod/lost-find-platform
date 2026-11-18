package com.zzhx.lostfound.system.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.zzhx.lostfound.model.entity.Category;
import com.zzhx.lostfound.system.mapper.CategoryMapper;
import com.zzhx.lostfound.system.service.CategoryService;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 分类 Service 实现
 */
@Service
public class CategoryServiceImpl extends ServiceImpl<CategoryMapper, Category> implements CategoryService {

    @Override
    public List<Category> listAll() {
        return list(new LambdaQueryWrapper<Category>().orderByAsc(Category::getSort));
    }
}
