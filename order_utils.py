import asyncio

import time

lot_size = 1
def place_order_schema(client, _price, _quantity=1, transaction_type="B"):
    order = client.place_order(
        exchange_segment="mcx_fo",
        product="NRML",
        price=_price,                    # Limit price (must be valid)
        order_type="L",               # AMO must be LIMIT
        quantity=str(_quantity*lot_size),
        validity="DAY",               # DAY validity is required
        trading_symbol="CRUDEOILM14JAN265100CE",
        transaction_type="B",
        amo="NO",                    # 🔑 IMPORTANT: Enable AMO
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
    return order

def modify_order_schema(client, order_id, _price, _quantity=1):
    return client.modify_order(
        order_id = order_id,
        price = _price,
        quantity = str(_quantity*lot_size),
        disclosed_quantity = "0",
        trigger_price = "0",
        validity = "DAY",
        order_type='L'
    )

def wait_for_execution(client,order_id, timeout=30):
    start = time.time()

    while time.time() - start < timeout:
        res = client.order_history(order_id=order_id)
        history = res["data"]

        history.sort(key=lambda x: x["boeSec"])
        state = history[-1]["ordSt"].lower()

        if state in ("complete", "traded"):
            return "EXECUTED"

        if state in ("cancelled", "rejected"):
            return "FAILED"

        time.sleep(0.5)

    raise TimeoutError("Order stuck in non-terminal state")

def cancel_open_orders(client):
    orders = client.order_report()

    for order in orders.get("data", []):
        order_status = order.get("ordSt", "").lower()
        order_id = order.get("nOrdNo")  # THIS is the order_id
    if order_status in ["open", "trigger pending"]:
        client.cancel_order(order_id=order_id)
        print(f"Cancelled: {order_id}")

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