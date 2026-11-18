package com.zzhx.lostfound.model.vo;

import lombok.Data;

import java.util.List;

/**
 * 数据统计响应
 */
@Data
public class StatsVO {

    /** 注册用户总数 */
    private Long totalUsers;

    /** 物品信息总数 */
    private Long totalItems;

    /** 寻物信息数 */
    private Long lostCount;

    /** 招领信息数 */
    private Long foundCount;

    /** 已完成信息数 */
    private Long completedCount;

    /** 完成率，已完成 / 总信息数 */
    private Double successRate;

    /** 各分类的信息数量分布 */
    private List<CategoryCount> categoryDistribution;

    @Data
    public static class CategoryCount {

        private String categoryName;

        private Long count;
    }
}
