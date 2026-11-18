package com.zzhx.lostfound.admin.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.zzhx.lostfound.common.result.Result;
import com.zzhx.lostfound.model.entity.Favorite;
import com.zzhx.lostfound.system.service.FavoriteService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * 收藏接口：收藏/取消、列表、状态
 */
@RestController
@RequestMapping("/favorites")
public class FavoriteController {

    private final FavoriteService favoriteService;

    public FavoriteController(FavoriteService favoriteService) {
        this.favoriteService = favoriteService;
    }

    /**
     * 收藏 / 取消收藏，同一接口按当前状态切换
     */
    @PostMapping("/{itemId}/toggle")
    public Result<Void> toggle(@PathVariable Long itemId, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        favoriteService.toggle(itemId, userId);
        return Result.success();
    }

    /**
     * 分页查询当前用户的收藏列表
     */
    @GetMapping
    public Result<Page<Favorite>> page(
            @RequestParam(defaultValue = "1") Long current,
            @RequestParam(defaultValue = "10") Long size,
            HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return Result.success(favoriteService.pageQuery(current, size, userId));
    }

    /**
     * 查询当前用户是否已收藏某物品，用于详情页按钮状态
     */
    @GetMapping("/{itemId}/status")
    public Result<Map<String, Object>> status(@PathVariable Long itemId, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return Result.success(Map.of("favorited", favoriteService.isFavorited(itemId, userId)));
    }
}
