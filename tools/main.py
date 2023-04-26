from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# @app.get(f"/items/dh")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}


#
# if __name__ == '__main__':
#     read_root()
#     # read_item()



f = \
    {
        # 流程配置
        "releaseApproveType": "SELF",  # 发布审批方式,默认自审批【WFL：工作流审批，SELF：自审批】
        "resultApproveType": "SELF",  # 结果审批方式【WFL：工作流审批，SELF：自审批】，默认自审批
        "qualificationType": "NONE",  # 资格审查【无需资格审查："NONE",资格预审:"PRE"】
        "expertScoreType": "NONE",  # 专家评分,默认无需专家评分【无需专家评分："NONE",线上专家评分:"ONLINE"】
        "bidRuleType": "NONE",  # 标书规则：不区分：NONE，分商务/技术：DIFF
        "openBidOrder": "SYNC",  # 评标步制:[同步评标"SYNC",先商务后技术："BUSINESS_FIRST",先技术后商务:"TECH_FIRST"],默认同步评标
        "initialReview": "NONE",  # 符合性检查[无需符合性检查:"NONE",符合性检查:"NEED"],默认为NONE
        "sourceStage": "COMMON",  # 寻源阶段[常规:"COMMON",两阶段:"DOUBLE"]
        "bargainRule": "NONE",  # 议价规则【不允许发起议价："NONE",评审阶段发起议价:"SCORE",核价阶段发起议价:"CHECK",均允许发起议价:"ALL"】
        "bargainOfflineFlag": 0,  # 是否允许线下议价标志[不允许线下议价：0，允许线下议价：1]
        "roundQuotationRule": "NONE",  # 发起多轮报价规则,【不允许发起多轮报价："NONE",核价阶段发起多轮报价:"CHECK",评审阶段发起多轮报价:"SCORE",
        # 自动发起多轮报价：“AUTO”,自动+核价手动发起多轮报价:"AUTO_CHECK",自动+评审手动发起多轮报价:"AUTO_SCORE"】
        "roundQuotationRankRule": "TAX_PRICE",  # 多轮报价排名规则,[非多轮：None,按基准价:BASE_PRICE,按含税单价：TAX_PRICE，按未税单价：UNIT_PRICE]
        "roundQuotationRankFlag": 0,  # 多轮报价排名标志[不勾选为：0，勾选为1]
        "quotationRounds": None,  # 自动多轮报价轮次 [允许多轮：输入轮次；不允许为None]
        # 寻源规则配置
        "maxVendorQuantity": None,  # 最多邀请供应商数量，默认为None,非必填
        "minVendorNumber": 1,  # 最少邀请供应商数量,默认输入1
        "matchRestrictFlag": 0,  # 供应商能力匹配限制，1：勾选限制，0：不勾选不限制；默认”不限制“
        "quotationEndDateFlag": 1,  # 设置报价截止时间标志，默认为勾选【设置：1，不设置：0】
        "openerFlag": 0,  # 启用开标人标志，，默认不启用，【不启用：0，启用：1】
        "validDateInputType": "NOT_REQUIRED",  # 报价有效期，默认”非必输“ 【非必输:"NOT_REQUIRED";必输:"REQUIRED",只读:"READONLY"】
        "taxChangeFlag": 0,  # 允许供应商修改税率标志，1允许，0不允许，默认不允许
        "quantityChangeFlag": 0,  # 允许供应商修改可供数量，1是允许，0是不允许，默认不允许
        "diyLadderQuotationFlag": 0,  # 允许供方自定义阶梯报价，1是允许，0是不允许，默认不允许
        "multiCurrencyFlag": 0,  # 是否允许多币种报价【不允许：0，允许：1】
        "freightUpdatableFlag": 1,  # 允许供应商修改运费标识，1是允许，0是不允许，默认为允许
        "tenderFeeFlag": 0,  # 招标文件费管控，1是允许，0是不允许，默认为不允许
        "openEliminateFlag": 0,  # 启用逐轮淘汰标志：0是不启用，1是启用
        "bidBondFlag": 0,  # 保证金管控，1管控，0不管控，默认不管控
        "minQuotedSupplier": 1,  # 最少报价供应商数，默认未1
        "leaderNoScoreFlag": 0,  # 允许评分负责人不参与打分，0允许，1不允许
        "templateScoreType": "SCORE",  # 评分方式, 分值法：SCORE，权重法：WEIGHT,默认分值法
        "continuousQuotationFlag": 0,  # 允许供应商连续报价标志，【0：不连续，1允许供应商连续报价】，默认不连续
        "budgetControlRule": "NO_CONTROL",  # 预算控制规则,默认不管控   【不管控：NO_CONTROL强管控成交金额小于预算金额：STRONG_CONTROL，成交金额超预算时仅提示：WEAK_CONTROL，】
        # 缺省值配置
        "sourceMethod": "OPEN",  # 寻源方式,默认合作伙伴公开 [邀请:"INVITE",合作伙伴公开:OPEN,全平台公开:ALL_OPEN]
        "quotationScope": "ALL_QUOTATION",  # 报价范围,默认全部报价，[全部报价:ALL_QUOTATION,部分报价:PART_QUOTATION]
        "quotationType": "ONLINE",  # 报价方式【线上报价：ONLINE，线下报价：OFFLINE，线上线下并行：ON_OFF】
        "auctionDirection": "REVERSE",  # 报价方向：默认荷兰式 英式：FORWARD，荷兰式："REVERSE"
        "detailPriceControlRule": "NONE",  # 报价明细管控【强控单价小于或等于报价明细总价：STRONG，弱控单价小于或等于报价明细总价：WEAK，不管控：NONE，强控单价等于报价明细总价：EQUAL_STRONG，弱控单价等于报价明细总价：EQUAL_WEAK】
        "quotationChange": "ORDER_ITEM",  # 供应商升降价设置,默认”整单或按物料行升降价均可“ [仅允许整单升降价:ORDER,整单或按物料行升降价均可:ORDER_ITEM]
        "passwordFlag": 0,  # 是否启用开标密码标志【不启用：0，启用：1】,默认为0
        "freightIncludedFlag": 0,  # 是否含运费标志【不包含：0，包含：1】默认为0
        "sealedQuotationFlag": 0,  # 是否密封报价，0：非密封，1：密封，默认非密封
        "taxCode": None,  # 税率编码，默认不含税
        "selectionStrategy": "RELEASE",  # 选择策略,默认取消询价 [推荐供应商:RECOMMENDATION,取消询价:RELEASE,完成询价:CANCEL]
        "onlyAllowAllWinBids": 0,  # 仅允许整单中标，勾选为1，不勾选为0，默认不勾选
        "minExpertNum": 1,  # 最小专家组人数
    }

