


def buttons_message():
    message = TemplateMessage(
        alt_text='挑選高殖利率個股',
        template=ButtonsTemplate(
            text='請選擇以下功能',
            actions=[
                MessageAction(
                    label="請輸入最小市值 (億)",
                    text="市值
                ),
                MessageAction(
                    label="請輸入最小日交易量 (億)",
                    text="交易量"
                ),
                MessageAction(
                    label="前一年是否獲利(Y/N)?",
                    text="Y/N"
                ),
                MessageAction(
                    label="是否連續三年發放現金股利(Y/N)?",
                    text="Y/N"
                ),
                MessageAction(
                    label="請輸入最小現金殖利率 (%)",
                    text="最小現金殖利率"
                )
            ]
        )
    )
    return message