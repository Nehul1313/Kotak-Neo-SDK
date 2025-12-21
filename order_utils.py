import asyncio

async def manage_order(client, amo="NO"):
    try:
        order = client.place_order(
            exchange_segment="nse_cm",
            product="NRML",
            price="1",                    # Limit price (must be valid)
            order_type="L",               # AMO must be LIMIT
            quantity="1",
            validity="DAY",               # DAY validity is required
            trading_symbol="ITBEES-EQ",
            transaction_type="B",
            amo=amo,                    # 🔑 IMPORTANT: Enable AMO
            disclosed_quantity="0",
            market_protection="0",
            pf="N",
            trigger_price="0",
            tag=None,             # Optional but recommended
            scrip_token=None,
            square_off_type=None,
            stop_loss_type=None,
            stop_loss_value=None,
            square_off_value=None,
            last_traded_price=None,
            trailing_stop_loss=None,
            trailing_sl_value=None,
        )
        print(f"Order Placed please check For the Price")
        await asyncio.sleep(2)
        order_no = order['nOrdNo']
        client.modify_order(order_id = order_no, price = "2.0", quantity = "1", disclosed_quantity = "0", trigger_price = "0", validity = "DAY", order_type='L')
        await asyncio.sleep(2)
        print(f"Order Modification In Place please check and update")
        client.modify_order(order_id = order_no, price = "3.0", quantity = "1", disclosed_quantity = "0", trigger_price = "0", validity = "DAY", order_type='L')
        await asyncio.sleep(2)
        print(f"Order Modification In Place please check and update")
        client.cancel_order(order_id = order_no,amo = amo, isVerify=True)

        print(f"Order Cancelled Successfully please check and update")
        return "Success"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Failure"