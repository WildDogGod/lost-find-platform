package com.zzhx.lostfound.admin.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.zzhx.lostfound.common.annotation.Log;
import com.zzhx.lostfound.common.result.Result;
import com.zzhx.lostfound.model.dto.ItemDTO;
import com.zzhx.lostfound.model.entity.Item;
import com.zzhx.lostfound.system.service.ItemService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

/**
 * 物品接口：发布、浏览、搜索、详情、状态、匹配
 */
@RestController
@RequestMapping("/items")
public class ItemController {

    private final ItemService itemService;

    public ItemController(ItemService itemService) {
        this.itemService = itemService;
    }

    /**
     * 发布失物 / 招领信息，返回新记录 id
     */
    @Log("发布物品")
    @PostMapping
    public Result<Long> publish(@Valid @RequestBody ItemDTO dto, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return Result.success(itemService.publish(dto, userId));
    }

    /**
     * 分页查询物品列表，支持类型、分类、关键词、地点、状态筛选
     */
    @GetMapping
    public Result<Page<Item>> page(
            @RequestParam(defaultValue = "1") Long current,
            @RequestParam(defaultValue = "10") Long size,
            @RequestParam(required = false) String type,
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) String keyword,
            @RequestParam(required = false) String location,
            @RequestParam(required = false) String status) {
        return Result.success(itemService.pageQuery(current, size, type, categoryId,
                keyword, location, status));
    }

    /**
     * 查询物品详情，隐藏特征字段不返回给前端
     */
    @GetMapping("/{id}")
    public Result<Item> detail(@PathVariable Long id) {
        return Result.success(itemService.getById(id));
    }

    /**
     * 编辑物品信息，仅发布者本人或管理员可操作
     */
    @PutMapping("/{id}")
    public Result<Void> update(@PathVariable Long id, @RequestBody ItemDTO dto,
                               HttpServletRequest request) {
        itemService.updateItem(id, dto, (Long) request.getAttribute("userId"));
        return Result.success();
    }

    /**
     * 删除物品，仅发布者本人或管理员可操作
     */
    @DeleteMapping("/{id}")
    public Result<Void> delete(@PathVariable Long id, HttpServletRequest request) {
        itemService.deleteItem(id, (Long) request.getAttribute("userId"));
        return Result.success();
    }

    /**
     * 更新物品状态，如手动关闭或标记完成
     */
    @PutMapping("/{id}/status")
    public Result<Void> updateStatus(@PathVariable Long id, @RequestBody Map<String, String> body,
                                     HttpServletRequest request) {
        itemService.updateStatus(id, body.get("status"), (Long) request.getAttribute("userId"));
        return Result.success();
    }

    /**
     * 分页查询我发布的物品
     */
    @GetMapping("/mine")
    public Result<Page<Item>> mine(
            @RequestParam(defaultValue = "1") Long current,
            @RequestParam(defaultValue = "10") Long size,
            @RequestParam(required = false) String type,
            HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return Result.success(itemService.mine(current, size, type, userId));
    }

    /**
     * 智能匹配：查找类型相反、同分类且仍有效的物品
     */
    @GetMapping("/{id}/matches")
    public Result<List<Item>> matches(@PathVariable Long id) {
        return Result.success(itemService.matches(id));
    }
}
