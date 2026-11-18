package com.zzhx.lostfound.system.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.zzhx.lostfound.model.entity.Favorite;

/**
 * 收藏 Service
 */
public interface FavoriteService extends IService<Favorite> {

    /** 收藏 / 取消收藏（切换） */
    void toggle(Long itemId, Long userId);

    /** 我的收藏分页 */
    Page<Favorite> pageQuery(Long current, Long size, Long userId);

    /** 是否已收藏 */
    boolean isFavorited(Long itemId, Long userId);
}
