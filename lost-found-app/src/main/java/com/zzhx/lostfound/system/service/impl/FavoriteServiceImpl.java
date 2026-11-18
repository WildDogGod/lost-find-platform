package com.zzhx.lostfound.system.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.zzhx.lostfound.model.entity.Favorite;
import com.zzhx.lostfound.system.mapper.FavoriteMapper;
import com.zzhx.lostfound.system.service.FavoriteService;
import org.springframework.stereotype.Service;

/**
 * 收藏 Service 实现
 */
@Service
public class FavoriteServiceImpl extends ServiceImpl<FavoriteMapper, Favorite> implements FavoriteService {

    @Override
    public void toggle(Long itemId, Long userId) {
        Favorite existing = getOne(new LambdaQueryWrapper<Favorite>()
                .eq(Favorite::getUserId, userId)
                .eq(Favorite::getItemId, itemId));
        if (existing != null) {
            removeById(existing.getId());
        } else {
            Favorite favorite = new Favorite();
            favorite.setUserId(userId);
            favorite.setItemId(itemId);
            save(favorite);
        }
    }

    /**
     * 分页查询我的收藏，并补全物品展示信息
     */
    @Override
    public Page<Favorite> pageQuery(Long current, Long size, Long userId) {
        return page(new Page<>(current, size),
                new LambdaQueryWrapper<Favorite>()
                        .eq(Favorite::getUserId, userId)
                        .orderByDesc(Favorite::getCreateTime));
    }

    /**
     * 判断当前用户是否收藏了该物品
     */
    @Override
    public boolean isFavorited(Long itemId, Long userId) {
        return count(new LambdaQueryWrapper<Favorite>()
                .eq(Favorite::getUserId, userId)
                .eq(Favorite::getItemId, itemId)) > 0;
    }
}
