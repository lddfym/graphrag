import pandas as pd
import numpy as np
from typing import Any


def println(title: str | None = None, data: Any | None = None,):
    if title is not None:
        print(f"---------{title}---------")
    if data is not None:
        print(data)
    print('\n')


def test_group_agg():
    data = {
        '部门': ['销售', '销售', '技术', '技术', '销售', '技术'],
        '员工': ['张三', '李四', '王五', '赵六', '孙七', '周八'],
        '工资': [3000, 4000, 7000, 8000, 3500, 9000]
    }

    df = pd.DataFrame(data)
    """
       部门  员工    工资
    0  销售  张三  3000
    1  销售  李四  4000
    2  技术  王五  7000
    3  技术  赵六  8000
    4  销售  孙七  3500
    5  技术  周八  9000
    """
    println(title="原始数据", data=df)

    # 获取行的值 for index, row in df.iterrows():
    println(title="获取某一行数据", data=df.loc[0])

    println(title="获取某一列数据", data=df["部门"])
    println(title="获取某一列数据 shape", data=df["部门"].shape)  # (6,)
    println(title="获取某几列数据", data=df[["员工", "工资"]])
    println(title="获取某几列数据 shape", data=df[["员工", "工资"]].shape)  # (6, 2)

    println(title="通过坐标获取单元格的值 [0,0]", data=df.iloc[0, 0])
    println(title="通过标签获取单元格的值 [0, 员工]", data=df.loc[0, "工资"])

    println(title="获取原始数据的 index 列", data=df.index)
    """
    RangeIndex(start=0, stop=6, step=1)
    """

    df.columns = ["部门", "x", "工资"]
    println(title="修改列名", data=df)

    output = df.groupby("部门")
    output_sum = output.sum()
    """
            员工     工资
    部门               
    技术  王五赵六周八  24000
    销售  张三李四孙七  10500
    """
    println(title="按照部门求和", data=output_sum)
    println(title="获取分组求和后的维度", data=output_sum.shape)  # (2,2)
    println(title="取分组求和后的 index 列", data=output_sum.index)
    """
    Index(['技术', '销售'], dtype='object', name='部门')
    """

    output_arry_agg = output.agg(lambda series: [e for e in series])
    println(title="按照部门聚合", data=output_arry_agg)

    output_mean = output.agg({"工资": "mean"})  # 只保留 "工资" 列
    output_mean.rename(columns={"工资": "平均工资"}, inplace=True)
    """
    reset_index 之前: Index(['技术', '销售'], dtype='object', name='部门')
    reset_index 之后: RangeIndex(start=0, stop=2, step=1)
    """
    println(title="reset_index 前的 index 列", data=output_mean.index)
    output_mean.reset_index(inplace=True)
    println(title="reset_index 后的 index 列", data=output_mean.index)
    println(title="按照部门计算平均工资", data=output_mean)

    output_mean["alias"] = ["AB"]
    println(title="对某列赋值相同的 行值", data=output_mean)


def test_init():
    data1 = {
        '部门': ['销售', '销售', '技术', '技术', '销售', '技术'],
        '员工': ['张三', '李四', '王五', '赵六', '孙七', '周八'],
        '工资': [3000, 4000, 7000, 8000, 3500, 9000]
    }

    data2 = [
        {"部门": "销售", "员工": "张三", "工资": 3000},
        {"部门": "技术", "员工": "王五", "工资": 7000},
    ]

    df1 = pd.DataFrame(data1)
    println(title="数据源: 字典", data=df1)
    df2 = pd.DataFrame(data2)
    println(title="数据源: 数组", data=df2)


def test_apply_explode():
    data = {
        '部门': ['销售', '销售', '技术', '技术', '销售', '技术'],
        '员工': ['张三', '李四', '王五', '赵六', '孙七', '周八'],
        '工资': [3000, 4000, 7000, 8000, 3500, np.nan]
    }

    df = pd.DataFrame(data)
    output_apply = df.apply(lambda row: (row["工资"], [100, 10]), axis=1)
    println(title="工资+100", data=output_apply)

    df['工资2'] = output_apply
    println(title="修改/增加 一列的数据", data=df)

    output_exp = df.explode('工资2')
    println(title="展开列: 工资2", data=output_exp)

    # 注意：此处是个 list
    df[['a', 'b']] = pd.DataFrame(df['工资2'].to_list(), df.index)
    println(title="同时赋值多个列", data=df)

    # df['a'] 是一个列向量(一维数组), axis 只能取值 0 (按照行方向 检查每一列)
    # df[['a']] 是多个列向量(二维数组),  axis 可以取值 0(按照行方向 检查每一列)、1(按照列方向 检查每一行)
    # any: 用来判断是否为 True、非空、非零
    output_any = df[['a']].any(axis=1)
    println(title="true", data=output_any)
    println(title="notna", data=df[output_any])


if __name__ == "__main__":
    test_group_agg()
    # test_init()
    # test_apply_explode()
